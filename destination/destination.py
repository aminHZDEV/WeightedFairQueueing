import os
import threading
import socket
import configparser
import json
from datetime import datetime
import traceback

def setup():
    config_path = os.path.join(os.path.abspath(os.path.join("config.ini")))
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def handler(conn: dict = None) -> None:
    data = ""
    config = setup()
    while True:
        try:
            received_data = conn["conn"].recv(4048).decode()
            if not received_data:
                return
            data += received_data
            if data != "":
                data = str(data)
                data.replace("'", '"')

            json_data = json.loads(received_data)
            print("-" * 80)
            result = f"data receive in destination => packet : {json_data['packet']} data length : {len(json_data['data'])} , data : {json_data['data']} weight : {json_data['weight']} at {datetime.now().strftime('%H:%M:%S')}"
            print(result)
            with open(
                os.path.join(config["CONFIGS"]["result_Address"], "result.csv"), "a"
            ) as f:
                f.write(result + "\n")

            data = ""
        except Exception as e:
            print(e)
            print(traceback.format_exc())


def destination() -> None:
    # get the hostname
    config = setup()
    host = socket.gethostname()
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_port = int(config["CONFIGS"]["destination_port"])
    source_amount = int(config["CONFIGS"]["router_amount"])
    server_socket.bind((host, server_port))
    server_socket.listen(source_amount)
    connections = []
    print("Destination started. Waiting for connections...")
    for _ in range(source_amount):
        conn, address = server_socket.accept()
        print("Connection from: " + str(address))
        connections.append({"conn": conn, "addr": address})
    try:
        thread_list = []
        for i in range(source_amount):
            thread_list.append(threading.Thread(target=handler, args=(connections[i],)))
        for item in thread_list:
            item.start()
        for item in thread_list:
            item.join()
    except Exception as e:
        # Handle the exception if any error occurs
        print("ERROR : ", e)
        print(traceback.format_exc())
    server_socket.close()  # close the server socket


if __name__ == "__main__":
    destination()
