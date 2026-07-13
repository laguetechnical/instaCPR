import requests
import time
import os

BASE_URL = "https://lt-mailgen.onrender.com"
API_KEY = os.getenv("API_KEY")
HEADERS = {"X-API-Key": API_KEY}


def get_otp(address, sender="email.meta.com", timeout=180):
    """
    Patient OTP polling.
    - First tries for `timeout` seconds (recommended: 180 = 3 minutes)
    - Polls every 8-10 seconds
    """
    deadline = time.time() + timeout
    attempt = 0

    print(f"\n[OTP] Starting patient poll for: {address}")
    print(f"[OTP] Max wait: {timeout} seconds | Checking every ~8s\n")

    while time.time() < deadline:
        attempt += 1
        try:
            resp = requests.get(
                f"{BASE_URL}/otp",
                headers=HEADERS,
                params={
                    "address": address,
                    "sender": sender,
                    "method": 1,
                    "on_failure": "next",
                },
                timeout=20,
            )

            if resp.status_code == 200:
                data = resp.json()
                if data.get("success") and data.get("data", {}).get("otp"):
                    otp = data["data"]["otp"]
                    print(f"[+] ✅ OTP RECEIVED on attempt #{attempt}: {otp}\n")
                    return otp
                else:
                    print(f"[OTP] #{attempt} → 200 but no OTP yet")

            elif resp.status_code == 404:
                print(f"[OTP] #{attempt} → 404 (not in inbox yet)")
            else:
                print(f"[OTP] #{attempt} → Status {resp.status_code}")

        except Exception as e:
            print(f"[OTP ERROR] #{attempt} → {e}")

        time.sleep(8)   # ← Check every 8 seconds

    print(f"\n[OTP] ❌ No OTP after {timeout} seconds")
    raise TimeoutError(f"OTP not received within {timeout} seconds for {address}")