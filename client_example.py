import hashlib
import os
import platform
import time
import uuid
import requests

SERVER_URL = os.getenv("AUTHGUARD_SERVER_URL", "http://127.0.0.1:8000").rstrip("/")
PROJECT_API_KEY = os.getenv("AUTHGUARD_PROJECT_KEY", "YOUR_PROJECT_API_KEY")


def get_hwid() -> str:
    """Generate a deterministic hardware fingerprint for the current machine."""
    raw_id = f"{platform.node()}-{platform.machine()}-{uuid.getnode()}"
    return hashlib.sha256(raw_id.encode("utf-8")).hexdigest()[:32]


def activate_license(username: str, license_key: str, provider: str, provider_user_id: str, hwid: str) -> dict:
    """Bind a single-use license key to the current machine HWID."""
    payload = {
        "username": username,
        "license_key": license_key,
        "provider": provider,          # "telegram" or "discord"
        "provider_user_id": provider_user_id,
        "hwid": hwid,
    }
    headers = {"X-API-Key": PROJECT_API_KEY}
    response = requests.post(f"{SERVER_URL}/api/v1/activate", json=payload, headers=headers, timeout=15)
    response.raise_for_status()
    return response.json()


def request_2fa_login(username: str, hwid: str) -> dict:
    """Initiate a 2FA challenge via Telegram or Discord and poll for confirmation."""
    headers = {"X-API-Key": PROJECT_API_KEY}
    init_resp = requests.post(
        f"{SERVER_URL}/api/v1/login",
        json={"username": username, "hwid": hwid},
        headers=headers,
        timeout=15,
    )
    init_resp.raise_for_status()
    challenge = init_resp.json()

    challenge_id = challenge["challenge_id"]
    print(f"[2FA] Open your bot and tap the number shown on screen: {challenge['verification_number']}")

    for _ in range(30):
        status_resp = requests.get(
            f"{SERVER_URL}/api/v1/login/status/{challenge_id}",
            headers=headers,
            timeout=10,
        )
        status_resp.raise_for_status()
        data = status_resp.json()

        if data.get("status") == "approved":
            return data
        if data.get("status") in {"rejected", "expired"}:
            raise RuntimeError(f"2FA login {data.get('status')}.")

        time.sleep(2)

    raise TimeoutError("2FA confirmation timed out.")


if __name__ == "__main__":
    device_hwid = get_hwid()
    print(f"Detected HWID: {device_hwid}")
