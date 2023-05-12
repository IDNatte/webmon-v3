import threading
import msgpack
import psutil


class SystemProberThread(threading.Thread):
    def __init__(self, output):
        super().__init__()
        self.output = output
        self.stop_event = threading.Event()

    def run(self):
        while not self.stop_event.is_set():
            with open(self.output, "ab") as sys_probed:
                sys_info = [
                    proc.info
                    for proc in psutil.process_iter(["pid", "name", "username"])
                ]
                packed = msgpack.packb(sys_info)
                sys_probed.write(packed)

    def stop(self):
        self.stop_event.set()
