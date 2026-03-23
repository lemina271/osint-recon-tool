from flask import Flask, render_template, request
import socket
import os
import whois
import subprocess

app = Flask(__name__)

def find_subdomains(domain):
    subdomains = ["www", "mail", "ftp", "dev", "test"]
    found = []

    for sub in subdomains:
        url = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(url)
            found.append(f"{url} --> {ip}")
        except:
            pass

    return found

def run_nmap(domain):
    try:
        result = subprocess.check_output(["nmap", "-F", domain], text=True)
        return result
    except:
        return "Nmap scan failed"

def get_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except:
        return None

def get_whois(domain):
    try:
        w = whois.whois(domain)
        return {
            "domain": w.domain_name,
            "registrar": w.registrar
        }
    except:
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    result = {}

    if request.method == "POST":
        domain = request.form.get("domain")

        ip = get_ip(domain)
        whois_data = get_whois(domain)
        nmap_result = run_nmap(domain)
        subdomains = find_subdomains(domain)

        result = {
            "domain": domain,
            "ip": ip,
            "whois": whois_data,
            "nmap": nmap_result,
            "subdomains": subdomains
        }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)