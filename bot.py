import requests
from datetime import datetime

TELEGRAM_TOKEN = "7536406194:AAFtiqqiAH-mh0ZLS3IzxfId3b2jFVqe89s"
CHAT_ID = "8200636968"
MIN_MAGNITUDE = 4.5

BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

def send(msg):
    requests.post(
        f"{BASE_URL}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg}
    )

def get_updates(offset=None):
    params = {"timeout": 10}
    if offset:
        params["offset"] = offset
    return requests.get(f"{BASE_URL}/getUpdates", params=params).json()

def latest_quake():
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"
    data = requests.get(url).json()["features"]

    for q in data:
        mag = q["properties"]["mag"]
        place = q["properties"]["place"]
        lon, lat, depth = q["geometry"]["coordinates"]

        if mag and 4 <= lat <= 10 and 118 <= lon <= 126:
            return (
                "🌏 Latest Mindanao Earthquake\n"
                f"Magnitude: {mag}\n"
                f"Location: {place}"
            )

    return "No recent Mindanao earthquakes in the last hour."

def handle_commands():
    updates = get_updates()
    for u in updates.get("result", []):
        text = u["message"].get("text", "")
        update_id = u["update_id"]

        if text == "/help":
            send(
                "🤖 Quake Bot Commands:\n"
                "/status – bot status\n"
                "/latest – latest Mindanao quake\n"
                "/help – show this message"
            )

        elif text == "/status":
            send(
                "✅ Bot is running\n"
                f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )

        elif text == "/latest":
            send(latest_quake())

        # mark update as processed
       
def check_quakes():
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"
    data = requests.get(url).json()["features"]

    for q in data:
        mag = q["properties"]["mag"]
        place = q["properties"]["place"]
        lon, lat, depth = q["geometry"]["coordinates"]

        if not mag or mag < MIN_MAGNITUDE:
            continue

        if not (4 <= lat <= 10 and 118 <= lon <= 126):
            continue

        send(
            "⚠️ EARTHQUAKE ALERT\n"
            f"Magnitude: {mag}\n"
            f"Location: {place}\n\n"
            "DROP, COVER, HOLD.\n"
            "Expect aftershocks."
        )

if __name__ == "__main__":
    handle_commands()
    check_quakes()
#Add Telegram commands

