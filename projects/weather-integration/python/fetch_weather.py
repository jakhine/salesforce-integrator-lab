import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[3]  # 3 уровня вверх до корня репо
sys.path.append(str(ROOT))
from tools.python.load_config import APP, get_env
import requests

API_KEY = get_env("OPENWEATHERMAP_KEY", required=True)
city = APP.get("default_city", "Valencia,ES")
baseURL = APP["weather"]["api_base"]
units = APP["weather"].get("units", "metric")
params={"q": city, "appid": API_KEY, "units": units}
def fetch_weather():
    try:
        r = requests.get(baseURL, params=params, timeout=10)
        r.raise_for_status()
    except requests.HTTPError:
        print("Response body:", r.text, file=sys.stderr)
        raise
    except requests.RequestException as e:
        fail(f"Network error: {e}")

    data = r.json()
    return {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"],
    }

if __name__ == "__main__":
    w = fetch_weather()
    print("City:", w["city"])
    print("Temperature:", w["temperature"])
    print("Humidity:", w["humidity"])
    print("Description:", w["description"])
