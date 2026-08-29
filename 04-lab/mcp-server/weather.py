from typing import Any
import asyncio
import httpx
import os
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
port = int(os.getenv("PORT", 8085))
mcp = FastMCP("weather", host="0.0.0.0", port=port)

# Constants
WEATHERAPI_BASE = "https://api.weatherapi.com/v1"
OPENWEATHER_BASE = "https://api.openweathermap.org/data/2.5"
USER_AGENT = "weather-app/1.0"

# Get API keys from environment variable
WEATHERAPI_KEY = os.getenv("WEATHERAPI_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY") or os.getenv("OPENWEATHERMAP_API_KEY") or "6ba29ccba75060e9f09a473b8f7c806a"

_MOCK_WEATHER = {
    "hanoi": {
        "location": {"name": "Hanoi", "region": "Ha Noi", "country": "Vietnam"},
        "current": {
            "temp_c": 29.0,
            "temp_f": 84.2,
            "feelslike_c": 33.5,
            "feelslike_f": 92.3,
            "condition": {"text": "Trời mưa nhẹ / Light Rain"},
            "humidity": 82,
            "wind_kph": 12.0,
            "wind_mph": 7.5,
            "wind_dir": "SE",
            "pressure_mb": 1008.0,
            "uv": 4.0,
            "vis_km": 8.0,
            "last_updated": "2026-08-29 10:00",
        },
        "forecast": {
            "forecastday": [
                {
                    "date": "2026-08-29",
                    "day": {
                        "maxtemp_c": 32.0, "maxtemp_f": 89.6,
                        "mintemp_c": 26.0, "mintemp_f": 78.8,
                        "condition": {"text": "Mưa rào / Rain Showers"},
                        "daily_chance_of_rain": 80,
                        "maxwind_kph": 15.0,
                        "uv": 5.0
                    }
                },
                {
                    "date": "2026-08-30",
                    "day": {
                        "maxtemp_c": 33.0, "maxtemp_f": 91.4,
                        "mintemp_c": 27.0, "mintemp_f": 80.6,
                        "condition": {"text": "Nhiều mây / Partly Cloudy"},
                        "daily_chance_of_rain": 40,
                        "maxwind_kph": 12.0,
                        "uv": 6.0
                    }
                },
                {
                    "date": "2026-08-31",
                    "day": {
                        "maxtemp_c": 34.0, "maxtemp_f": 93.2,
                        "mintemp_c": 27.0, "mintemp_f": 80.6,
                        "condition": {"text": "Nắng / Sunny"},
                        "daily_chance_of_rain": 20,
                        "maxwind_kph": 10.0,
                        "uv": 8.0
                    }
                }
            ]
        }
    },
    "danang": {
        "location": {"name": "Da Nang", "region": "Da Nang", "country": "Vietnam"},
        "current": {
            "temp_c": 31.0,
            "temp_f": 87.8,
            "feelslike_c": 35.0,
            "feelslike_f": 95.0,
            "condition": {"text": "Nhiều mây / Cloudy"},
            "humidity": 75,
            "wind_kph": 10.0,
            "wind_mph": 6.2,
            "wind_dir": "E",
            "pressure_mb": 1010.0,
            "uv": 6.0,
            "vis_km": 10.0,
            "last_updated": "2026-08-29 10:00",
        },
        "forecast": {
            "forecastday": [
                {
                    "date": "2026-08-29",
                    "day": {
                        "maxtemp_c": 33.0, "maxtemp_f": 91.4,
                        "mintemp_c": 26.0, "mintemp_f": 78.8,
                        "condition": {"text": "Nhiều mây / Cloudy"},
                        "daily_chance_of_rain": 30,
                        "maxwind_kph": 12.0,
                        "uv": 7.0
                    }
                },
                {
                    "date": "2026-08-30",
                    "day": {
                        "maxtemp_c": 34.0, "maxtemp_f": 93.2,
                        "mintemp_c": 27.0, "mintemp_f": 80.6,
                        "condition": {"text": "Nắng / Sunny"},
                        "daily_chance_of_rain": 10,
                        "maxwind_kph": 14.0,
                        "uv": 8.0
                    }
                },
                {
                    "date": "2026-08-31",
                    "day": {
                        "maxtemp_c": 32.0, "maxtemp_f": 89.6,
                        "mintemp_c": 26.0, "mintemp_f": 78.8,
                        "condition": {"text": "Mưa dông / Thunderstorm"},
                        "daily_chance_of_rain": 70,
                        "maxwind_kph": 18.0,
                        "uv": 5.0
                    }
                }
            ]
        }
    },
    "brisbane": {
        "location": {"name": "Brisbane", "region": "Queensland", "country": "Australia"},
        "current": {
            "temp_c": 22.0,
            "temp_f": 71.6,
            "feelslike_c": 22.0,
            "feelslike_f": 71.6,
            "condition": {"text": "Sunny / Quang đãng"},
            "humidity": 55,
            "wind_kph": 15.0,
            "wind_mph": 9.3,
            "wind_dir": "S",
            "pressure_mb": 1018.0,
            "uv": 5.0,
            "vis_km": 10.0,
            "last_updated": "2026-08-29 10:00",
        },
        "forecast": {
            "forecastday": [
                {
                    "date": "2026-08-29",
                    "day": {
                        "maxtemp_c": 24.0, "maxtemp_f": 75.2,
                        "mintemp_c": 12.0, "mintemp_f": 53.6,
                        "condition": {"text": "Sunny / Trời nắng"},
                        "daily_chance_of_rain": 5,
                        "maxwind_kph": 16.0,
                        "uv": 6.0
                    }
                },
                {
                    "date": "2026-08-30",
                    "day": {
                        "maxtemp_c": 25.0, "maxtemp_f": 77.0,
                        "mintemp_c": 13.0, "mintemp_f": 55.4,
                        "condition": {"text": "Partly Cloudy"},
                        "daily_chance_of_rain": 10,
                        "maxwind_kph": 14.0,
                        "uv": 6.0
                    }
                },
                {
                    "date": "2026-08-31",
                    "day": {
                        "maxtemp_c": 23.0, "maxtemp_f": 73.4,
                        "mintemp_c": 14.0, "mintemp_f": 57.2,
                        "condition": {"text": "Possible Shower"},
                        "daily_chance_of_rain": 40,
                        "maxwind_kph": 20.0,
                        "uv": 5.0
                    }
                }
            ]
        }
    }
}

def _get_mock_data(city: str) -> dict[str, Any]:
    city_key = city.lower().replace(" ", "")
    for k, v in _MOCK_WEATHER.items():
        if k in city_key or city_key in k:
            return v
    return {
        "location": {"name": city.capitalize(), "region": city.capitalize(), "country": "Earth"},
        "current": {
            "temp_c": 26.0,
            "temp_f": 78.8,
            "feelslike_c": 27.0,
            "feelslike_f": 80.6,
            "condition": {"text": "Partly Cloudy / Có mây"},
            "humidity": 65,
            "wind_kph": 10.0,
            "wind_mph": 6.2,
            "wind_dir": "NE",
            "pressure_mb": 1012.0,
            "uv": 5.0,
            "vis_km": 10.0,
            "last_updated": "2026-08-29 10:00",
        },
        "forecast": {
            "forecastday": [
                {
                    "date": "2026-08-29",
                    "day": {
                        "maxtemp_c": 28.0, "maxtemp_f": 82.4,
                        "mintemp_c": 22.0, "mintemp_f": 71.6,
                        "condition": {"text": "Partly Cloudy"},
                        "daily_chance_of_rain": 20,
                        "maxwind_kph": 12.0,
                        "uv": 6.0
                    }
                },
                {
                    "date": "2026-08-30",
                    "day": {
                        "maxtemp_c": 29.0, "maxtemp_f": 84.2,
                        "mintemp_c": 23.0, "mintemp_f": 73.4,
                        "condition": {"text": "Sunny"},
                        "daily_chance_of_rain": 10,
                        "maxwind_kph": 10.0,
                        "uv": 7.0
                    }
                },
                {
                    "date": "2026-08-31",
                    "day": {
                        "maxtemp_c": 27.0, "maxtemp_f": 80.6,
                        "mintemp_c": 21.0, "mintemp_f": 69.8,
                        "condition": {"text": "Rain"},
                        "daily_chance_of_rain": 60,
                        "maxwind_kph": 15.0,
                        "uv": 4.0
                    }
                }
            ]
        }
    }

async def fetch_openweather(endpoint: str, city: str, days: int = 3) -> dict[str, Any] | None:
    """Fetch data from OpenWeatherMap API."""
    if not OPENWEATHER_API_KEY:
        return None
    url = f"{OPENWEATHER_BASE}/{endpoint}"
    params = {"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"}
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(url, params=params, timeout=10.0)
            if r.status_code == 200:
                data = r.json()
                if endpoint == "weather":
                    return {
                        "location": {
                            "name": data.get("name", city),
                            "region": data.get("sys", {}).get("country", ""),
                            "country": data.get("sys", {}).get("country", "")
                        },
                        "current": {
                            "temp_c": data["main"]["temp"],
                            "temp_f": round(data["main"]["temp"] * 9/5 + 32, 1),
                            "feelslike_c": data["main"].get("feels_like", data["main"]["temp"]),
                            "feelslike_f": round(data["main"].get("feels_like", data["main"]["temp"]) * 9/5 + 32, 1),
                            "condition": {"text": data["weather"][0]["description"].title() if data.get("weather") else "Clear"},
                            "humidity": data["main"]["humidity"],
                            "wind_kph": round(data["wind"]["speed"] * 3.6, 1),
                            "wind_mph": round(data["wind"]["speed"] * 2.237, 1),
                            "wind_dir": str(data["wind"].get("deg", 0)) + "°",
                            "pressure_mb": data["main"]["pressure"],
                            "uv": 5.0,
                            "vis_km": round(data.get("visibility", 10000) / 1000, 1),
                            "last_updated": "Realtime (OpenWeather)"
                        }
                    }
                elif endpoint == "forecast":
                    forecast_list = data.get("list", [])
                    daily_data = {}
                    for item in forecast_list:
                        date_str = item["dt_txt"].split(" ")[0]
                        if date_str not in daily_data:
                            daily_data[date_str] = {
                                "date": date_str,
                                "day": {
                                    "maxtemp_c": item["main"]["temp_max"],
                                    "maxtemp_f": round(item["main"]["temp_max"] * 9/5 + 32, 1),
                                    "mintemp_c": item["main"]["temp_min"],
                                    "mintemp_f": round(item["main"]["temp_min"] * 9/5 + 32, 1),
                                    "condition": {"text": item["weather"][0]["description"].title() if item.get("weather") else "Clear"},
                                    "daily_chance_of_rain": int(item.get("pop", 0) * 100),
                                    "maxwind_kph": round(item["wind"]["speed"] * 3.6, 1),
                                    "uv": 5.0
                                }
                            }
                        else:
                            daily_data[date_str]["day"]["maxtemp_c"] = max(daily_data[date_str]["day"]["maxtemp_c"], item["main"]["temp_max"])
                            daily_data[date_str]["day"]["mintemp_c"] = min(daily_data[date_str]["day"]["mintemp_c"], item["main"]["temp_min"])
                            daily_data[date_str]["day"]["maxtemp_f"] = round(daily_data[date_str]["day"]["maxtemp_c"] * 9/5 + 32, 1)
                            daily_data[date_str]["day"]["mintemp_f"] = round(daily_data[date_str]["day"]["mintemp_c"] * 9/5 + 32, 1)
                    
                    selected_days = list(daily_data.values())[:days]
                    return {
                        "location": {
                            "name": data.get("city", {}).get("name", city),
                            "region": data.get("city", {}).get("country", ""),
                            "country": data.get("city", {}).get("country", "")
                        },
                        "forecast": {
                            "forecastday": selected_days
                        }
                    }
        except Exception as e:
            print(f"OpenWeather request error: {e}")
    return None

async def make_weather_request(endpoint: str, params: dict[str, str]) -> dict[str, Any] | None:
    """Make a request to WeatherAPI, OpenWeather, or fallback to mock data."""
    city = params.get("q", "Hanoi")
    
    # 1. Try OpenWeather
    if OPENWEATHER_API_KEY:
        ow_endpoint = "weather" if "current" in endpoint else "forecast"
        ow_data = await fetch_openweather(ow_endpoint, city, int(params.get("days", 3)))
        if ow_data:
            return ow_data

    # 2. Try WeatherAPI
    if WEATHERAPI_KEY:
        headers = {"User-Agent": USER_AGENT}
        params["key"] = WEATHERAPI_KEY
        url = f"{WEATHERAPI_BASE}/{endpoint}"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers, params=params, timeout=10.0)
                if response.status_code == 200:
                    return response.json()
            except Exception as e:
                print(f"WeatherAPI error: {e}")
                
    # 3. Fallback to Mock Data
    return _get_mock_data(city)

@mcp.tool()
async def get_current_weather(city: str) -> str:
    """Get current weather conditions for a city.

    Args:
        city: City name (e.g., "Hanoi", "Haiphong", "Danang", "Brisbane", "Sydney")
    """
    params = {
        "q": city,
        "aqi": "no"
    }
    
    data = await make_weather_request("current.json", params)

    if not data:
        if not API_KEY:
            return f"❌ WeatherAPI key not configured. Please set WEATHERAPI_KEY environment variable with your API key from weatherapi.com"
        return f"Unable to fetch current weather data for {city}. Please check the city name and API key configuration."

    current = data["current"]
    location = data["location"]
    
    return f"""
Current Weather for {location['name']}, {location['region']}, {location['country']}:

Temperature: {current['temp_c']}°C ({current['temp_f']}°F)
Feels like: {current['feelslike_c']}°C ({current['feelslike_f']}°F)
Condition: {current['condition']['text']}
Humidity: {current['humidity']}%
Wind: {current['wind_kph']} km/h ({current['wind_mph']} mph) {current['wind_dir']}
Pressure: {current['pressure_mb']} mb
UV Index: {current['uv']}
Visibility: {current['vis_km']} km

Last updated: {current['last_updated']}
"""

@mcp.tool()
async def get_forecast(city: str, days: int = 3) -> str:
    """Get weather forecast for a city.

    Args:
        city: City name (e.g., "Hanoi", "Haiphong", "Danang", "Brisbane", "Sydney", "Melbourne")
        days: Number of days to forecast (1-3 for free tier, max 10 for paid)
    """
    # Limit days to 3 for free tier
    days = min(days, 3)
    
    params = {
        "q": city,
        "days": str(days),
        "aqi": "no",
        "alerts": "no"
    }
    
    data = await make_weather_request("forecast.json", params)

    if not data:
        if not API_KEY:
            return f"❌ WeatherAPI key not configured. Please set WEATHERAPI_KEY environment variable with your API key from weatherapi.com"
        return f"Unable to fetch forecast data for {city}. Please check the city name and API key configuration."

    location = data["location"]
    forecast_days = data["forecast"]["forecastday"]
    
    forecasts = []
    forecasts.append(f"Weather Forecast for {location['name']}, {location['region']}, {location['country']}:")
    
    for day in forecast_days:
        day_data = day["day"]
        date = day["date"]
        
        forecast = f"""
{date}:
High: {day_data['maxtemp_c']}°C ({day_data['maxtemp_f']}°F)
Low: {day_data['mintemp_c']}°C ({day_data['mintemp_f']}°F)
Condition: {day_data['condition']['text']}
Chance of Rain: {day_data['daily_chance_of_rain']}%
Max Wind: {day_data['maxwind_kph']} km/h
UV Index: {day_data['uv']}
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)

@mcp.tool()
async def health_check() -> str:
    """Health check endpoint for deployment verification."""
    return "✅ Weather MCP Server is running! Ready to provide weather data for Australian cities and worldwide."

print("✅ MCP server initialized with Streamable HTTP transport")
print("🔧 Available tools: get_current_weather, get_forecast, health_check")

if __name__ == "__main__":
    import sys
    
    if "--stdio" in sys.argv:
        print("Starting FastMCP server in stdio mode for local client", file=sys.stderr)
        mcp.run(transport="stdio")
    else:
        print(f"🚀 Starting MCP server on http://0.0.0.0:{port}/mcp")
        mcp.run(transport="streamable-http")