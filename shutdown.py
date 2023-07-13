from gamocosm import Server


def main() -> None:
    names = ["vanilla", "atm8"]
    servers = [Server.from_toml(name) for name in names]
    for server in servers:
        server.stop()


if __name__ == "__main__":
    main()
