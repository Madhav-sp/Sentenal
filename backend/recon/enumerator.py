import requests
import socket

def get_subdomains(domain):
    try:
        url = f"https://crt.sh/?q=%25.{domain}&output=json"
        r = requests.get(url, timeout=5)
        data = r.json()

        subs = set()
        for entry in data:
            names = entry["name_value"].split("\n")
            for n in names:
                if domain in n:
                    subs.add(n.strip())

        return list(subs)[:15]

    except:
        # fallback demo data
        return [
            f"api.{domain}",
            f"dev.{domain}",
            f"test.{domain}"
        ]


def resolve_ip(subdomain):
    try:
        return socket.gethostbyname(subdomain)
    except:
        return None