import requests

TELEGRAM_TOKEN = "7536406194:AAFtiqqiAH-mh0ZLS3IzxfId3b2jFVqe89s"
CHAT_ID = "8200636968"
MIN_MAGNITUDE = 4.5

def send(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

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

        msg = f"⚠️ Earthquake Alert\nMagnitude: {mag}\nLocation: {place}"
        send(msg)

if __name__ == "__main__":
    check_quakes()
