import requests

def get_weather(destination: str, days: int) -> str:
    """Fetch weather forecast for a destination using Open-Meteo."""

    # Step 1 — Geocode: convert city name to lat/lon
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    geo_res = requests.get(geo_url, params={"name": destination, "count": 1})
    geo_data = geo_res.json()

    if not geo_data.get("results"):
        return f"Could not find location data for {destination}."

    location = geo_data["results"][0]
    lat = location["latitude"]
    lon = location["longitude"]
    city_name = location["name"]
    country = location.get("country", "")

    # Step 2 — Fetch forecast: daily max temp + rain sum
    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_res = requests.get(weather_url, params={
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,rain_sum",
        "timezone": "auto",
        "forecast_days": min(days, 7)  # Open-Meteo max is 16, we cap at 7
    })
    weather_data = weather_res.json()

    daily = weather_data.get("daily", {})
    dates = daily.get("time", [])
    temps = daily.get("temperature_2m_max", [])
    rains = daily.get("rain_sum", [])

    # Step 3 — Format as readable text for the agent
    lines = [f"Weather forecast for {city_name}, {country}:"]
    for i in range(len(dates)):
        lines.append(
            f"  {dates[i]}: Max Temp {temps[i]}°C, Rain {rains[i]}mm"
        )

    return "\n".join(lines)

