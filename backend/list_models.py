import requests
from config import settings  # this will read GOOGLE_API_KEY from .env

url = "https://generativelanguage.googleapis.com/v1beta/models"

params = {"key": settings.GOOGLE_API_KEY}

resp = requests.get(url, params=params, timeout=60)
resp.raise_for_status()

data = resp.json()

print("Available models for this API key:\n")
for m in data.get("models", []):
    print(m["name"])
