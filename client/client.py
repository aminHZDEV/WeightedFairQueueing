import csv
import socket
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
source_csv_address = config['CONFIGS']['source_csv_address']
destination_url = config['CONFIGS']['destination_url']
destination_port = int(config['CONFIGS']['destination_port'])

with open(source_csv_address, 'r') as file:
    reader = csv.reader(file)
    data = list(reader)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((destination_url, destination_port))

for row in data:
    packet = row[0]
    data = row[1]
    message = f"{packet},{data}"
    s.send(message.encode())

s.close()