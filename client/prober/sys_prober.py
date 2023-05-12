import threading
import datetime
import msgpack
import psutil
import os


class SystemProberThread(threading.Thread):
    def __init__(self, output_dir, output_file):
        super().__init__()
        self.output_dir = output_dir
        self.output_file = output_file
        self.stop_event = threading.Event()

        if not os.path.isdir(self.output_dir):
            os.mkdir(os.path.join(os.path.abspath(output_dir)))

    def run(self):
        net_io = psutil.net_io_counters()
        with open(os.path.join(self.output_dir, self.output_file), "wb") as sys_probed:
            payload = {
                "probe_time": f"{datetime.datetime.now()}",
                "system_info": [
                    proc.info
                    for proc in psutil.process_iter(["pid", "name", "username"])
                ],
                "networks": {
                    "bytes_sent": net_io.bytes_sent,
                    "bytes_recv": net_io.bytes_recv,
                    "packets_sent": net_io.packets_sent,
                    "packets_recv": net_io.packets_recv,
                },
            }
            packed = msgpack.packb(payload)
            sys_probed.write(packed)

    def stop(self):
        self.stop_event.set()
