import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def post_to_username(url: str) -> str | None:
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    tag = soup.find("meta", property="og:url")

    if not tag:
        return None

    return tag["content"].rstrip("/").split("/")[3]


if __name__ == "__main__":
    url = input("URL: ").strip()
    print(post_to_username(url))