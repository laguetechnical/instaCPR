import re
import requests
import random, os
BASE_URL = "https://lt-mailgen.onrender.com"
API_KEY = os.getenv("API_KEY")

HEADERS = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json",
}


# def generate_temp_email(full_name, domain="1"):
#     """
#     Generate a temporary email using MailGen API.
#     """

#     username = re.sub(r"[^a-zA-Z0-9]", "", full_name).lower()

#     if not username:
#         username = "user"

#     payload = {
#         "username": username,
#         "domain": domain,
#         "on_taken": "retry",
#         "max_retry": 2,
#     }

#     try:
#         response = requests.post(
#             f"{BASE_URL}/generate",
#             headers=HEADERS,
#             json=payload,
#             timeout=60,
#         )

#         response.raise_for_status()

#         result = response.json()

#         if not result["success"]:
#             raise RuntimeError(result["message"])

#         email = result["data"]["email"]

#         print(f"[+] Generated temporary email: {email}")

#         return email

#     except requests.RequestException as e:
#         raise RuntimeError(f"MailGen API unavailable: {e}") from e

def generate_temp_email(full_name, domain="1"):
    """
    Generate a temporary email using MailGen API.

    - EMAIL_TAKEN  -> generate a new username and retry once
    - RATE_LIMIT   -> stop immediately
    """

    username = re.sub(r"[^a-zA-Z0-9]", "", full_name).lower()

    if not username:
        username = "user"

    retries = 2

    while retries >= 0:

        payload = {
            "username": username,
            "domain": domain,
            "on_taken": "error",
            "max_retry": 0,
        }

        try:
            response = requests.post(
                f"{BASE_URL}/generate",
                headers=HEADERS,
                json=payload,
                timeout=60,
            )

            response.raise_for_status()

            result = response.json()

            # ------------------------
            # Success
            # ------------------------
            if result["success"]:
                email = result["data"]["email"]
                print(f"[+] Generated temporary email: {email}")
                return email

            error = result.get("error")

            # ------------------------
            # Email already taken
            # ------------------------
            if error == "EMAIL_TAKEN":
                print("[!] Email already taken. Retrying...")

                username = (
                    f"{re.sub(r'[^a-zA-Z0-9]', '', full_name).lower()}_"
                    f"{random.randint(1000,9999)}"
                )

                retries -= 1
                continue

            # ------------------------
            # Daily rate limit
            # ------------------------
            if error == "RATE_LIMIT":
                raise RuntimeError(
                    "Rate limit exceeded. Try again tomorrow."
                )

            # ------------------------
            # Unknown MailGen error
            # ------------------------
            raise RuntimeError(
                result.get("message", "Unknown MailGen error")
            )

        except requests.RequestException as e:
            raise RuntimeError(
                f"MailGen API unavailable: {e}"
            ) from e

    raise RuntimeError(
        "Unable to generate a temporary email."
    )

def get_otp(email, timeout=180):
    """
    Wait for an OTP using MailGen API.
    MailGen handles all polling and fallback methods.
    """

    params = {
        "address": email,
        "sender": "instagram",
        "method": 1,
        "on_failure": "next",
    }

    try:
        response = requests.get(
            f"{BASE_URL}/otp",
            headers=HEADERS,
            params=params,
            timeout=timeout + 30,
        )

        response.raise_for_status()

        result = response.json()

        if not result["success"]:
            raise TimeoutError(result["message"])

        otp = result["data"]["otp"]

        print(f"[+] OTP found: {otp}")

        return otp

    except requests.RequestException as e:
        raise RuntimeError(f"MailGen API unavailable: {e}") from e