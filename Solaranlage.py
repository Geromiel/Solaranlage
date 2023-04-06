import requests
import re
from influxdb import InfluxDBClient

PATTERN = r'var webdata_now_p = "(.*?)";'
HOSTNAME = 'IP OF SOLAR PANEL'
INFLUXDB_IP = 'IP OF INFLUXDB'
INFLUXDB_PORT = 'PORT OF INFLUXDB'
USERNAME_DEYE = 'admin'
PASSWORD_DEYE = 'admin'


def website():
    session = requests.Session()
    session.auth = (USERNAME_DEYE, PASSWORD_DEYE)
    response = session.get('http://' + HOSTNAME + '/status.html')

    html = response.text

    temp = re.search(PATTERN, html).group(0)
    result = re.findall('\d+', temp)

    return str(result[0])


def influxdb(power_output):
    power_output = power_output
    field = 'watt'
    client = InfluxDBClient(host=INFLUXDB_IP, port=INFLUXDB_PORT)
    client.switch_database('solarpanel')

    data_point = [
        {
            'measurement': 'PowerOutput',
            'fields': {field: power_output}
        }
    ]

    client.write_points(data_point)


def main():
    power_output = website()
    influxdb(power_output)


if __name__ == "__main__":
    main()
