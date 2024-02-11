import csv
import socket
import configparser
import os
from typing import Tuple
import time
import threading
import glob

def send_data_with_time(
    s: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM),
    data: str = "",
    time_delay: int = 0,
    weight: int = 0,
    packet: str = "",
) -> None:
    print("-" * 70)
    print(
        "time delay : ",
        time_delay,
        " for packet : ",
        packet,
        " with weight : ",
        weight,
        " and length : ",
        len(data),
    )
    message = f'{{"packet":"{packet}","data":"{data}","weight":{weight}}}'
    time.sleep(time_delay)
    s.send(message.encode("utf-8"))


def setup() -> Tuple[str, int, list]:
    config_path = os.path.join(os.path.abspath(os.path.join("config.ini")))
    config = configparser.ConfigParser()
    config.read(config_path)
    csv_files = glob.glob(os.path.join(config["CONFIGS"]["csv_address"], 'data_*_*.csv'))
    source_csv_address_list = []

    for item in csv_files:
        source_csv_address_list.append({
            "addr": item,
            "weight": os.path.basename(item).split("_")[2].split(".")[0]
        })
    return (
        socket.gethostname(),
        int(config["CONFIGS"]["router_port"]),
        source_csv_address_list,
    )


def read_csv_files(source_csv_address_list: list = None) -> list:
    data_lists = []
    for source in source_csv_address_list:
        with open(os.path.join(os.getcwd(), source["addr"]), "r") as file:
            reader = csv.reader(file)
            reader_list = list(reader)
            reader_list.pop(0)
            data_lists.append({"weight": int(source["weight"]), "data": reader_list})
    return data_lists


host, destination_port, source_csv_address_list = setup()
data_list = read_csv_files(source_csv_address_list=source_csv_address_list)


threads = []
sockets = []
for data in data_list:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, destination_port))
    sockets.append(s)
    if isinstance(data, dict):
        weight = data["weight"]
        for row in data["data"]:
            packet = row[0]
            data = row[1].strip()
            time_delay = int(row[2])
            thread = threading.Thread(
                target=send_data_with_time, args=(s, data, time_delay, weight, packet)
            )
            threads.append(thread)
            thread.start()

for thread in threads:
    thread.join()

for s in sockets:
    s.close()


