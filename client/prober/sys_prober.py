import threading
import datetime
import msgpack
import psutil
import socket
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
        network = psutil.net_io_counters(pernic=True)
        addr_prober = psutil.net_if_addrs()
        with open(os.path.join(self.output_dir, self.output_file), "wb") as sys_probed:
            payload = {
                "probe_time": f"{datetime.datetime.now()}",
                "system_info": {
                    "net_info": [
                        {
                            "interface": net,
                            "receive": network.get(net).bytes_recv,
                            "transfer": network.get(net).bytes_sent,
                            "ip_addr": [
                                net.address
                                for net in addr_prober.get(net)
                                if net.family == socket.AF_INET
                            ][0],
                        }
                        for net in network
                    ],
                    "hostname": socket.gethostname(),
                },
                "application": {
                    "app_net_usage": [
                        {
                            "proc_name": psutil.Process(conn.pid).name(),
                            "status": conn.status,
                            "address": {
                                "local_address": conn.laddr[0],
                                "local_port": conn.laddr[1],
                                "remote_address": conn.raddr[0],
                                "remote_port": conn.raddr[1],
                            },
                        }
                        for conn in psutil.net_connections()
                        if conn.status == psutil.CONN_ESTABLISHED
                    ],
                    "running_app": [
                        {
                            "proc_name": proc.info.get("name"),
                            "proc_info": proc.info,
                            "used_resource": {
                                "cpu": psutil.Process(
                                    proc.info.get("pid")
                                ).cpu_percent(),
                                "mem": psutil.Process(
                                    proc.info.get("pid")
                                ).memory_percent(memtype="rss"),
                            },
                        }
                        for proc in psutil.process_iter(["pid", "name", "username"])
                    ],
                },
            }
            packed = msgpack.packb(payload)
            sys_probed.write(packed)

    def stop(self):
        self.stop_event.set()
