#!/usr/bin/env python3
import os, sys, time, json
import requests, jwt
from pathlib import Path

# --- make repo root importable (so we can import tools/... and projects/...) ---
THIS = Path(__file__).resolve()
REPO_ROOT = THIS.parents[3]  # .../salesforce-integrator-lab
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Shared config loader (env + app.yaml)
from tools.python.load_config import APP, get_env
# Weather fetcher that returns a dict
# Добавляем папку с fetch_weather.py в sys.path (так как в имени есть "-")
WEATHER_PY_DIR = REPO_ROOT / "projects" / "weather-integration" / "python"
if str(WEATHER_PY_DIR) not in sys.path:
    sys.path.insert(0, str(WEATHER_PY_DIR))

import fetch_weather as weather_mod
# ---- Config (all via shared loader) ----
SF_LOGIN_URL = get_env("SF_LOGIN_URL", "https://login.salesforce.com")  # sandbox: https://test.salesforce.com
SF_CLIENT_ID = get_env("SF_CLIENT_ID", required=True)                  # Connected App → Consumer Key
SF_USERNAME  = get_env("SF_USERNAME",  required=True)                  # Integration user login
KEY_PATH     = get_env("SF_PRIVATE_KEY_PATH", "server.key")            # Path to private key (PEM)

API_VERSION  = APP.get("salesforce", {}).get("api_version", "61.0")    # from config/app.yaml

def get_access_token():
    """JWT Bearer Flow → returns (access_token, instance_url)"""
    if not Path(KEY_PATH).exists():
        raise FileNotFoundError(f"Private key not found: {KEY_PATH}")

    private_key = Path(KEY_PATH).read_bytes()
    now = int(time.time())
    payload = {
        "iss": SF_CLIENT_ID,         # Consumer Key
        "sub": SF_USERNAME,          # user to impersonate
        "aud": SF_LOGIN_URL,         # login or test
        "exp": now + 300             # 5 minutes
    }

    assertion = jwt.encode(payload, private_key, algorithm="RS256")
    r = requests.post(
        f"{SF_LOGIN_URL}/services/oauth2/token",
        data={
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": assertion
        },
        timeout=20
    )
    try:
        r.raise_for_status()
    except requests.HTTPError:
        # полезно увидеть тело ошибки от SF
        print("Salesforce token response:", r.status_code, r.text, file=sys.stderr)
        raise

    data = r.json()
    return data["access_token"], data["instance_url"]

def insert_weather_record(record: dict) -> dict:
    access_token, instance_url = get_access_token()
    url = f"{instance_url}/services/data/v{API_VERSION}/sobjects/Weather__c"
    r = requests.post(
        url,
        headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"},
        data=json.dumps(record),
        timeout=20
    )
    print("[SFDC]", r.status_code, r.text)
    r.raise_for_status()
    return r.json()

def main():
    w = weather_mod.fetch_weather() # expects: {city, temperature, humidity, description}
    record = {
        "City__c":        w["city"],
        "Temperature__c": w["temperature"],
        "Humidity__c":    w["humidity"],
        "Description__c": w["description"],
        "ObservedAt__c":  time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    res = insert_weather_record(record)
    print("Inserted Weather__c:", res)

if __name__ == "__main__":
    main()