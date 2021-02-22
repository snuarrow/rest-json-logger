import argparse
import json
import requests
import sys
from os import path, mkdir
from time import sleep
from datetime import datetime
from plot import plot
import threading

def parse_args():
    p = argparse.ArgumentParser(
        description='Rest api json response logger',
    )
    p.add_argument(
        '--config-file',
        type=str,
    )
    p.add_argument(
        '--plot',
        action='store_true',
    )
    return p.parse_args()


def load_config_file(config_path: str):
    with open(config_path) as f:
        return json.load(f)


def get_responses(config: dict):
    responses = []
    for url in config["urls"]:
        if 'http' not in url:
            url = f'http://{url}'
        
        i = 0
        while i < 10:
            i += 1
            try:
                responses.append(requests.get(url).json())
                break
            except requests.exceptions.ConnectionError:
                continue
    return responses


def write_log(config: dict, responses: list):
    if not path.exists(config["log_folder"]):
        mkdir(config["log_folder"])
    logfile = f'{config["log_folder"]}/{datetime.now().strftime("%Y_%m_%d")}_00.json'
    try:
        with open(logfile) as f:
            file_content = json.load(f)
            f.close()
    except FileNotFoundError:
        file_content = []

    
    #plot()

    file_content.append({
        "t": datetime.now(),
        "responses": responses
    })

    with open(f"latest_read.json", 'w') as f:
        json.dump({
            "t": datetime.now(),
            "responses": responses
        }, f, indent=4, default=str)

    with open(logfile, 'w') as f:
        json.dump(file_content, f, indent=4, default=str)

    print(f'{datetime.now()}: logged {len(responses)} responses')


def do(config: dict):
    write_log(config=config, responses=get_responses(config))


def timed_loop():
    config = load_config_file(config_path=config_file)
    while True:
        do(config=config)
        print("imma loopin")
        sleep(config["interval_minutes"] * 60)


def main():
    args = parse_args()
    
    running = True
    thread = threading.Thread(name='daemon', target=timed_loop)
    thread.setDaemon(True)
    thread.start()

    plot()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)