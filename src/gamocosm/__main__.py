import argparse

from gamocosm.core import Server

parser = argparse.ArgumentParser()
parser.add_argument("server")
parser.add_argument("command", default="status")
parser.add_argument("rest", nargs=argparse.REMAINDER)
args = parser.parse_args()

server = Server.from_toml(args.server)

match args.command:
    case "start":
        server.start()
    case "stop":
        server.stop()
    case "pause":
        server.pause()
    case "resume":
        server.resume()
    case "reboot":
        server.reboot()
    case "backup":
        server.backup()
    case "status":
        status = server.status()
        print(status)
    case "exec":
        mc_command = ' '.join(args.rest)
        print(f"rest: {mc_command!r}")
        server.exec(mc_command)
    case _:
        raise ValueError

