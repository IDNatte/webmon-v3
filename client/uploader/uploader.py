import threading
import requests


class UploaderThread(threading.Thread):
    def __init__(self, target_file, url, token):
        super().__init__()
        self.upload_file = target_file
        self.stop_event = threading.Event()
        self.url = url
        self.headers = {"Authorization": f"Bearer {token}"}

    def run(self):
        with open(self.upload_file, "rb") as data:
            files = {"file": data}

            test = requests.post(self.url, headers=self.headers, files=files)

            print(test.json())
