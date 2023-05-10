from uploader.uploader import UploaderThread


def main():
    send = UploaderThread("test.slg", "http://localhost:5000/upload", "dev")

    send.start()
    send.join()


if __name__ == "__main__":
    main()
