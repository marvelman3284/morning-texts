import requests
from datetime import datetime

def get_weather(api_key: str, lat: float, lon: float) -> list[str]:
    week_weather: list[str] = []

    complete_url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=imperial&appid={api_key}"
     
    response = requests.get(complete_url).json()
     
    for i in response['daily']:
        ts = i['dt']
        date = datetime.utcfromtimestamp(ts).strftime('%a %b %d')
        final = f"{date}: {i['temp']['day']}, low: {i['temp']['min']}, high: {i['temp']['max']}"
        week_weather.append(final)


    return week_weather

