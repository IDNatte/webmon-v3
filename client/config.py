import toml
import os


def main():
    base_path = os.path.dirname(os.path.abspath(__file__))
    config = os.path.join(base_path, "config")
    with open(os.path.join(config, "config.toml")) as config:
        test = toml.load(config)

    print(test)


if __name__ == "__main__":
    main()
