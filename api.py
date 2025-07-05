import requests
import datetime
import matplotlib.pyplot as plt
import sys
# API key
def get_api_key():
    return input("Enter your OpenWeatherMap API key: ").strip()
#Detect location by IP
def get_location_by_ip():
    try:
        response = requests.get("http://ip-api.com/json/")
        data = response.json()
        return data["city"]
    except:
        return None
# Step 3: Get coordinates of a city
def get_coordinates(city_name, api_key):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"
    res = requests.get(url)
    data = res.json()
    if data:
        return data[0]["lat"], data[0]["lon"]
    return None, None
# Get current weather
def get_current_weather(lat, lon, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"
    res = requests.get(url)
    return res.json()
# Get 5-day forecast
def get_forecast(lat, lon, api_key):
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={api_key}"
    res = requests.get(url)
    return res.json()
# Plot temperature forecast
def plot_temperature_chart(forecast_data):
    dates = []
    temps = []
    for item in forecast_data["list"]:
        dt = datetime.datetime.fromtimestamp(item["dt"])
        temp = item["main"]["temp"]
        dates.append(dt)
        temps.append(temp)

    plt.figure(figsize=(10, 5))
    plt.plot(dates, temps, marker='o')
    plt.title("5-Day Temperature Forecast")
    plt.xlabel("Date & Time")
    plt.ylabel("Temperature (°C)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
#app
def main():
    print("🌦️  Weather App (with Forecast + Chart)")
    api_key = get_api_key()

    use_auto_location = input("Use auto-detected location? (y/n): ").strip().lower()
    if use_auto_location == 'y':
        city = get_location_by_ip()
        if city:
            print(f"Detected Location: {city}")
        else:
            print("Failed to detect location. Enter manually.")
            city = input("Enter city name: ")
    else:
        city = input("Enter city name: ")

    lat, lon = get_coordinates(city, api_key)
    if lat is None or lon is None:
        print("Could not find location. Try a different city.")
        sys.exit()

    # Current Weather
    current = get_current_weather(lat, lon, api_key)
    print("\n===== Current Weather =====")
    print(f"City: {current['name']}")
    print(f"Weather: {current['weather'][0]['description'].title()}")
    print(f"Temperature: {current['main']['temp']}°C")
    print(f"Humidity: {current['main']['humidity']}%")
    print(f"Wind: {current['wind']['speed']} m/s")

    # Forecast
    forecast = get_forecast(lat, lon, api_key)
    print("\n===== 5-Day Forecast (every 3 hours) =====")
    for item in forecast["list"][:8]:  # Show first 24 hours (8 x 3hr)
        dt = datetime.datetime.fromtimestamp(item["dt"]).strftime("%Y-%m-%d %H:%M")
        temp = item["main"]["temp"]
        desc = item["weather"][0]["description"].title()
        print(f"{dt}: {temp}°C, {desc}")

    # Plot chart
    plot_temperature_chart(forecast)

if __name__ == "__main__":
    main()
