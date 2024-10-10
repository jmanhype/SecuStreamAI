import ipaddress
import requests

def is_valid_ip(ip: str) -> bool:
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def get_ip_geolocation(ip: str) -> dict:
    response = requests.get(f"https://ipapi.co/{ip}/json/")
    return response.json()