import argparse
import os
import time
from threading import Thread

import src.config as config


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config_path', default='/project/etc/config.yml')
    for k, v in vars(parser.parse_args()).items():
        setattr(config, k, v)


def listen_for_config_updates():
    def do():
        last_update = None
        while True:
            mtime = os.stat(config.config_path).st_mtime
            if last_update is None or last_update < mtime:
                config.load()
                last_update = mtime
            time.sleep(1)
    t = Thread(target=do)
    t.daemon = True
    t.start()


def boot_flask_server():
    pass


if __name__ == '__main__':
    parse_args()
    listen_for_config_updates()
    boot_flask_server()
    time.sleep(600)
