import socket
import pyautogui
import json
import time
import os
import signal
import sys

# Load configuration from appConfig.json
config_file = 'appConfig.json'
if not os.path.exists(config_file):
    config = {
        "use_key_mapping": True,
        "key_mapping": {
            "0": "a",
            "1": "b",
            "2": "c",
            "3": "d",
            "4": "e",
            "5": "f",
            "6": "g",
            "7": "h",
            "8": "i",
            "9": "j"
        },
        "seperator": " ",
        "server_address": "localhost",
        "port": 24242,
        "wait_time": 1,
        "receive_buffer_size": 16
    }
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=4)
else:
    with open(config_file, 'r') as f:
        config = json.load(f)

use_key_mapping = config['use_key_mapping']
if use_key_mapping:
    print("Key mapping is enabled")
key_mapping = config['key_mapping']
seperator = config['seperator']
server_address = (config['server_address'], config['port'])
wait_time = config['wait_time']
receive_buffer_size = config['receive_buffer_size']

def signal_handler(sig, frame):
    print('Ctrl+C pressed, exiting...')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

while True:
    try:
        # Set up the TCP server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(server_address)
        print(f"Connected to server at {server_address}")

        while True:
            data = sock.recv(receive_buffer_size)
            if data:
                message = data.decode('utf-8').strip()
                print(f"received: {message}") 
                if use_key_mapping:
                    try:
                        key_list = message.split(seperator)
                        #print(f"key_list {key_list}")
                        for key in key_list:
                            if key in key_mapping:
                                key_to_press = key_mapping[key]
                                pyautogui.press(key_to_press)
                                print(f"Pressed {key_to_press}")
                    except:
                        pass
                else:
                    for key in message:
                        key_to_press = key
                        pyautogui.press(key_to_press)
                    #print(f"message {message}")
            else:
                break
            time.sleep(wait_time)
    except Exception as e:
        print(f"Connection failed: {e}")
    finally:
        sock.close()
        print("Reconnecting...")
        time.sleep(1)  # Wait a bit before trying to reconnect