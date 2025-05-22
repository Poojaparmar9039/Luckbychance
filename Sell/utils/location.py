import requests

def get_location_from_ip(ip, token='52c7f0de10c562'):
    try:
        url = f"https://ipinfo.io/{ip}?token={token}"
        response = requests.get(url)
        data = response.json()
        return data.get("city", "") + ", " + data.get("region", "")  # e.g., "Mumbai, Maharashtra"
    except Exception:
        return ""
