import socket
import threading
import configparser
import os
import json
from common.buffer import Buffer
import time
import traceback


def handler(conn: dict = None, buff: Buffer = None) -> None:
    while True:
        data = ""
        try:
            received_data = conn["conn"].recv(4048).decode()
            if not received_data:
                return
            data += received_data
            if data != "":
                data = str(data)
                data.replace("'", '"')
                print("data => ", data, " receive to router from ", conn["addr"])
            json_data = json.loads(received_data)
            buff.buffer.put(item=json_data)
            data = ""
        except Exception as e:
            print(e)
            print(traceback.format_exc())


def sender(
    buff: Buffer = None, s: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
) -> None:
    while True:
        if not buff.buffer.empty():
            data = buff.buffer.get()
            print("data send to dest => ", data, "from address ", buff.addr)
            if data["weight"] != 0:
                time.sleep(len(data["data"]) / data["weight"])
            else:
                time.sleep(len(data["data"]))
            data = json.dumps(data)
            s.send(data.encode("utf-8"))


def setup_destination() -> socket:
    config_path = os.path.join(os.path.abspath(os.path.join("config.ini")))
    config = configparser.ConfigParser()
    config.read(config_path)
    host = socket.gethostname()
    destination_port = int(config["CONFIGS"]["destination_port"])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((host, destination_port))
    return s


def server_program() -> None:
    # get the hostname
    config_path = os.path.join(os.path.abspath(os.path.join("config.ini")))
    config = configparser.ConfigParser()
    config.read(config_path)
    host = socket.gethostname()
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_port = int(config["CONFIGS"]["router_port"])
    source_amount = int(config["CONFIGS"]["source_amount"])
    server_socket.bind((host, server_port))
    server_socket.listen(source_amount)
    connections = []
    buff = []
    print("Router started. Waiting for connections...")
    for _ in range(source_amount):
        conn, address = server_socket.accept()
        print("Connection from: " + str(address))
        connections.append({"conn": conn, "addr": address})
        buff.append(Buffer(addr=address))
    s = setup_destination()
    try:
        thread_list = []
        for i in range(source_amount):
            thread_list.append(
                threading.Thread(target=handler, args=(connections[i], buff[i]))
            )
            thread_list.append(threading.Thread(target=sender, args=(buff[i], s)))
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
    server_program()
