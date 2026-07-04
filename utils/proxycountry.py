import requests

def get_proxy_country(proxy_host, proxy_user="", proxy_pass=""):
    if proxy_user and proxy_pass:
        proxy_url = f"http://{proxy_user}:{proxy_pass}@{proxy_host}"
    else:
        proxy_url = f"http://{proxy_host}"

    proxies = {
        "http": proxy_url,
        "https": proxy_url,
    }

    try:
        r = requests.get(
            "http://ip-api.com/json/",
            proxies=proxies,
            timeout=10
        )
        data = r.json()

        if data.get("status") == "success":
            return data["country"]

        print("Failed:", data)
        return None

    except Exception as e:
        print("Error:", e)
        return None
