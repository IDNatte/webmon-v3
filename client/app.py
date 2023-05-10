from prober.sys_prober import SystemProberThread
from uploader.uploader import UploaderThread

import json
import time
import sys
import os


def main():
    base_path = os.path.dirname(os.path.abspath(__file__))
    config = os.path.join(base_path, "config")

    # To-Do:
    # check if config is available or no

    with open(os.path.join(config, "config.json"), "r") as settings:
        config_obj = json.loads(settings)

    print(config_obj)


if __name__ == "__main__":
    main()
