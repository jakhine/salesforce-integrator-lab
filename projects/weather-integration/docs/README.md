# Weather Integration 🌦️

This project demonstrates how to integrate an external Weather API (OpenWeatherMap) with Salesforce.  
It consists of a Python script that fetches weather data, pushes it into Salesforce, and a Lightning Web Component (LWC) to display the data.

---

## 🐍 Python Script: `fetch_weather.py`

### Installation
```bash
cd projects/weather-integration/python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Configuration
Create a `.env` file inside the `config/` folder with your OpenWeatherMap API key:

```env
OPENWEATHERMAP_KEY=your_api_key_here
```

### Run
```bash
python fetch_weather.py "Valencia,ES"
```

Expected output:
```
City: Valencia
Temperature: 35.2 °C
Humidity: 26 %
Description: clear sky
```

---

## 🗄 Salesforce Part

### Custom Object
Create a custom object `Weather__c` with fields:
- `City__c` (Text, 120)
- `Temperature__c` (Number, 3,1)
- `Humidity__c` (Number, 3,0)
- `Description__c` (Text, 255)
- `ObservedAt__c` (Date/Time)

### Apex Controller
`WeatherController.cls` should query the latest record and expose it via `@AuraEnabled` method for LWC.

### LWC Component
`weatherDisplay` fetches data from `WeatherController` and shows it as a simple weather card in Salesforce UI.

---

## 📦 Requirements

All Python dependencies are listed in [`requirements.txt`](../python/requirements.txt):

```
requests
python-dotenv
pyyaml
```

Install with:
```bash
pip install -r requirements.txt
```

---

## 📖 Next Steps
- Add Salesforce authentication to `fetch_weather.py` (POST to REST API).  
- Build `WeatherController.cls` and `WeatherControllerTest.cls`.  
- Deploy `weatherDisplay` LWC.  
