import requests, os

BASE_URL = "https://lt-mailgen.onrender.com"
API_KEY = os.getenv("API_KEY")

HEADERS = {
    "X-API-Key": API_KEY,
}


import time

def get_otp(address, sender="facebookmail.com", timeout=120):
    deadline = time.time() + timeout

    while time.time() < deadline:

        response = requests.get(
            f"{BASE_URL}/otp",
            headers=HEADERS,
            params={
                "address": address,
                "sender": sender,
                "method": 1,
                "on_failure": "next",
            },
            timeout=30,
        )

        # -------------------------
        # OTP FOUND
        # -------------------------
        if response.status_code == 200:
            result = response.json()
            return result["data"]["otp"]

        # -------------------------
        # OTP NOT YET
        # -------------------------
        if response.status_code == 404:
            time.sleep(2)
            continue

        # Other API errors
        response.raise_for_status()

    raise TimeoutError("OTP not received within timeout.")