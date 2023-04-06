import requests
import re
from influxdb import InfluxDBClient
import config

PATTERN = r'var webdata_now_p = "(.*?)";'
DEYE_IP = config.solarpanel['SOLARPANEL_IP']
DEYE_USERNAME = config.solarpanel['DEYE_USERNAME']
DEYE_PASSWORD = config.solarpanel['DEYE_PASSWORD']
INFLUXDB_IP = config.database['INFLUXDB_IP']
INFLUXDB_PORT = config.database['INFLUXDB_PORT']
INFLUXDB_DATABASE_NAME = config.database['INFLUXDB_DATABASE_NAME']


def website():
    session = requests.Session()
    session.auth = (DEYE_USERNAME, DEYE_PASSWORD)
    response = session.get('http://' + DEYE_IP + '/status.html')

    html = response.text

    temp = re.search(PATTERN, html).group(0)
    result = re.findall('\d+', temp)

    return str(result[0])


def influxdb(power_output):
    power_output = power_output
    field = 'watt'
    client = InfluxDBClient(host=INFLUXDB_IP, port=INFLUXDB_PORT)
    client.switch_database(INFLUXDB_DATABASE_NAME)

    data_point = [
        {
            'measurement': 'PowerOutput',
            'fields': {field: power_output}
        }
    ]
    client.write_points(data_point)


def main():
    try:
        power_output = website()
    except:
        power_output = '0'
        # Could implement alarming here, but my solar panel is not reachable during night time, so wouldn't be useful
    influxdb(power_output)


if __name__ == "__main__":
    main()
