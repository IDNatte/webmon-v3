from prober.sys_prober import SystemProberThread
from uploader.uploader import UploaderThread

import time
import sys


def main():
    sys_probe = SystemProberThread("test.slg")

    sys_probe.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        sys_probe.stop()
        sys_probe.join()


if __name__ == "__main__":
    main()
