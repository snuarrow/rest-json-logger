import argparse
import json
import requests
import sys
from os import path, mkdir
from time import sleep
from datetime import datetime
from hexlogger import logger


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
    p.add_argument(
        '--loop',
        action="store_true",
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
        while i < 1:
            i += 1
            try:
                logger.info(f"GET: {url}")
                responses.append(requests.get(url).json())
                break
            except requests.exceptions.ConnectionError:
                logger.error(f"failed to connect: {url}")
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

    logger.info(f'logged {len(responses)} responses')


def do(config: dict):
    write_log(config=config, responses=get_responses(config))


def timed_loop(config: dict):
    while True:
        logger.info("requesting data..")
        do(config=config)
        sleep(config["interval_minutes"] * 60)


def main():
    args = parse_args()
    config = load_config_file(config_path=args.config_file)
    if args.loop:
        timed_loop(config=config)
    else:
        do(config=config)



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
