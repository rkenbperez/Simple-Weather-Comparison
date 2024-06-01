import python_weather
import asyncio
import os
import matplotlib.pyplot as plt

city1 = input("Insert a City to get the weather: ")
city2 = input("Insert a second City to get the weather: ")

async def getweather(city):
    async with python_weather.Client(unit=python_weather.METRIC) as client:
        weather = await client.get(city)

    dates = []
    high_temps = []
    avg_temps = []

    for daily in weather.daily_forecasts:
        dates.append(daily.date.strftime('%Y-%m-%d'))
        high_temps.append(daily.highest_temperature)
        avg_temps.append(daily.temperature)

        print(city)
        print(f"Date: {daily.date}")
        print(f"Highest Temp: {daily.highest_temperature}°C")
        print(f"Temperature: {daily.temperature}°C")
        for hourly in daily.hourly_forecasts:
            print(f"  Time: {hourly.time.strftime('%I:%M %p')} - Temperature: {hourly.temperature}°C, Condition: {hourly.sky_text if hasattr(hourly, 'sky_text') else 'N/A'}")
        print("-" * 40 + "\n")

    return dates, high_temps, avg_temps

def plot_weather(dates1, high_temps1, avg_temps1, dates2, high_temps2, avg_temps2):
    plt.figure(figsize=(12, 6))

    plt.plot(dates1, high_temps1, label=f'{city1} Highest Temp (°C)', marker='o', linestyle='-')
    plt.plot(dates1, avg_temps1, label=f'{city1} Average Temp (°C)', marker='o', linestyle='--')
    plt.plot(dates2, high_temps2, label=f'{city2} Highest Temp (°C)', marker='x', linestyle='-')
    plt.plot(dates2, avg_temps2, label=f'{city2} Average Temp (°C)', marker='x', linestyle='--')

    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.title(f'Weather Forecast Comparison: {city1} vs {city2}')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    dates1, high_temps1, avg_temps1 = loop.run_until_complete(getweather(city1))
    dates2, high_temps2, avg_temps2 = loop.run_until_complete(getweather(city2))
    
    plot_weather(dates1, high_temps1, avg_temps1, dates2, high_temps2, avg_temps2)
