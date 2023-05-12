from prober.sys_prober import SystemProberThread
from uploader.uploader import UploaderThread

import datetime
import socket
import toml
import sys
import os
import re


def config_checker(fileconfig):
    checker = os.path.isfile(fileconfig)
    return checker


def config_maker():
    base_config_folder = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "config"
    )
    while True:
        try:
            file_log_path = str(
                input(
                    'Where do you want to put config output (E.g. "/var/log/server") : '
                )
            )

            file_log_prefix = str(
                input(
                    "Do you have any file log name prefix (E.g. Current Hostname) ? : "
                )
            )

            url_reporter = str(
                input(
                    'URL reporter endpoint (E.g. "https://reporter.host:5000/upload") : '
                )
            )

            if file_log_path and file_log_prefix and url_reporter:
                log_path = file_log_path
                log_prefix_1 = file_log_prefix
                log_reporter = url_reporter

            else:
                log_path = "/var/log/"
                log_prefix_1 = "host"
                log_reporter = "http://localhost:5000/upload"

            print("[*]Creating folder config...")
            if not os.path.isdir(base_config_folder):
                os.mkdir(base_config_folder)
            print("[!]Folder config created...\n")

            print("[*]Writting config to file")
            with open(os.path.join(base_config_folder, "config.toml"), "w") as c_write:
                config = {
                    "log": {
                        "path": log_path,
                        "fileformat": "slg",
                        "filename_prefix_1": log_prefix_1,
                        "filename_prefix_2": "timestamp",
                    },
                    "reporter": {
                        "url_link": log_reporter,
                    },
                }

                toml.dump(config, c_write)
            print("[!]Config created, running next procedure")

            break

        except KeyboardInterrupt:
            print("\nconfig creation canceled !")
            sys.exit()


def job_run():
    base_path = os.path.dirname(os.path.abspath(__file__))
    config = os.path.join(base_path, "config")
    config_file = os.path.join(config, "config.toml")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H:%M:%SZ")

    check = config_checker(config_file)
    if check:
        with open(os.path.join(config, "config.toml"), "r") as settings:
            config_obj = toml.load(settings)

            if (
                config_obj.get("log").get("filename_prefix_1") == "host"
                and config_obj.get("log").get("filename_prefix_2") == "timestamp"
            ):
                filename_construct = f"{socket.gethostname()}_{timestamp}.{config_obj.get('log').get('fileformat')}"

            else:
                filename_construct = f"{config_obj.get('log').get('filename_prefix_1')}_{timestamp}.{config_obj.get('log').get('fileformat')}"

            reporter_link = config_obj.get("reporter").get("url_link")
            filepath = config_obj.get("log").get("path")
            filename = filename_construct
            extended_filepath = os.path.join(filepath, filename_construct)

            sys_prober_thread = SystemProberThread(extended_filepath)
            uploader_thread = UploaderThread(extended_filepath, reporter_link, "dev")

    else:
        config_maker()


def main():
    job_run()


if __name__ == "__main__":
    main()
