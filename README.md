# AuthGuard — Python Client Example (HWID Licensing & 2FA)

Lightweight Python client example demonstrating how to integrate desktop apps or CLI tools with **AuthGuard** — a self-hosted FastAPI licensing server featuring hardware fingerprint (HWID) binding and interactive 2FA push approvals via **Telegram** and **Discord**.

> **Full Self-Hosted Server Package (FastAPI + Admin Dashboard + Discord/Telegram Bots + Docker):**  
> Available on Whop: **[Get AuthGuard v2.0](https://whop.com/aironsaid)**

---

## Key Features

- **Hardware Fingerprint (HWID) Locking:** Binds a license key to a specific machine (1 key = 1 PC) with admin revocation support.
- **Interactive 2FA via Telegram & Discord:** Sends a login challenge with number-matching verification directly to the user's Telegram or Discord bot before issuing an access session.
- **Zero Recurring SaaS Fees:** Runs on your own VPS or Docker container with full control over your SQLite/PostgreSQL database.
- **Simple REST Integration:** Activate keys, trigger 2FA challenges, and verify active sessions in a few lines of Python.

---

## Screenshots

### Admin Dashboard (License Generation & HWID Revocation)
![Admin Dashboard](assets/admin.png)

### Desktop Client (2FA Provider Selection & Activation)
![Desktop Client](assets/client.png)

### Telegram Bot (Number-Matching 2FA Push Prompt)
![Telegram 2FA Prompt](assets/telegram.png)

---

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
