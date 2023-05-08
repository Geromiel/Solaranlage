# Open Weather Map free API account:
# https://home.openweathermap.org/users/sign_up

import requests
import json
from influxdb import InfluxDBClient
import sys
sys.path.insert(0, '/home/pi/')
import config


API_KEY = config.openweathermap['API_KEY']
LAT = config.openweathermap['LAT']
LONG = config.openweathermap['LONG']
API_URL = config.openweathermap['API_URL']
INFLUXDB_IP = config.database['INFLUXDB_IP']
INFLUXDB_PORT = config.database['INFLUXDB_PORT']
INFLUXDB_DATABASE_NAME = config.database['INFLUXDB_DATABASE_NAME_WEATHER']


def api_call():
    response = requests.get(API_URL % (LAT, LONG, API_KEY))
    data = json.loads(response.text)
    return data


def extract_data(weather_data):
    current_temperature = weather_data["current"]["temp"]
    humidity = weather_data["current"]["humidity"]
    clouds = weather_data["current"]["clouds"]
    wind_speed = weather_data["current"]["wind_speed"]
    wind_deg = weather_data["current"]["wind_deg"]
    sunrise = weather_data["current"]["sunrise"]
    sunset = weather_data["current"]["sunset"]
    uvi = weather_data["current"]["uvi"]
    weather = weather_data["current"]["weather"][0]["main"]


    data_point = {
        'current_temperature': current_temperature,
        'humidity': humidity,
        'clouds': clouds,
        'wind_speed': wind_speed,
        'wind_deg': wind_deg,
        'sunrise': sunrise,
        'sunset': sunset,
        'uvi': uvi,
        'weather': weather

    }
    return data_point


def influxdb(data):
    client = InfluxDBClient(host=INFLUXDB_IP, port=INFLUXDB_PORT)
    client.switch_database(INFLUXDB_DATABASE_NAME)

    data_point = [
        {
            'measurement': 'weather_data',
            'fields': {
                'current_temperature': data["current_temperature"],
                'humidity': data["humidity"],
                'clouds': data["clouds"],
                'wind_speed': data["wind_speed"],
                'wind_deg': data["wind_deg"],
                'sunrise': data["sunrise"],
                'sunset': data["sunset"],
                'uvi': data["uvi"],
                'weather': data["weather"]
            }

        }
    ]
    client.write_points(data_point)


def main():
    weather_data = api_call()
    data_point = extract_data(weather_data)
    influxdb(data_point)


if __name__ == "__main__":
    main()
