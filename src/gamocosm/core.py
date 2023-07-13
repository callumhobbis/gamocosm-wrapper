from __future__ import annotations

import os
import requests
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Self, Any


cfg_root = Path(
    os.environ.get("APPDATA")
    or os.environ.get("XDG_CONFIG_HOME")
    or os.path.join(os.environ["HOME"], ".config")
) / "gamocosm"
servers_path = cfg_root/"server_list.toml"
os.makedirs(cfg_root, exist_ok=True)


JSONDict = dict[str, str | float | bool]


class CommandError(Exception):
    """Gamocosm comand returned an error."""
    pass


@dataclass
class Status:
    server_active: bool
    operation: str | None
    minecraft_active: bool
    domain: str | None
    download: str | None

    @classmethod
    def from_json(cls, status: dict) -> Self:
        return Status(
            server_active=status["server"],
            operation=status["status"],
            minecraft_active=status["minecraft"],
            domain=status["domain"],
            download=status["download"],
        )

@dataclass
class Server:
    server_id: str
    api_key: str

    @classmethod
    def from_toml(cls, name: str) -> Self:
        with open(servers_path, "rb") as fp:
            server_list = tomllib.load(fp)
        info = server_list[name]
        return Server(info["server_id"], info["api_key"])

    def start(self: Self) -> None:
        """Start the DO server and Minecraft."""
        self._basic_command("start")

    def stop(self: Self) -> None:
        """Stop the DO server and Minecraft."""
        self._basic_command("stop")

    def pause(self: Self) -> None:
        """Stop Minecraft."""
        self._basic_command("pause")

    def resume(self: Self) -> None:
        """Resume Minecraft."""
        self._basic_command("resume")

    def reboot(self: Self) -> None:
        """Reboot the DO server."""
        self._basic_command("reboot")

    def backup(self: Self) -> None:
        """Make a backup of the Minecraft world in the backups/ folder."""
        self._basic_command("backup")

    def status(self: Self) -> Status:
        """Get status of the server."""
        response = command("status", self.server_id, self.api_key)
        return Status.from_json(response)

    def exec(self: Self, command_str: str) -> None:
        """Execute a Minecraft command."""
        command("exec", self.server_id, self.api_key, {"command": command_str})

    def _basic_command(self: Self, name: str) -> None:
        valid_commands = ["start", "stop", "pause", "resume", "reboot", "backup"]
        if name not in valid_commands:
            raise ValueError(name)
        response = command(name, self.server_id, self.api_key)
        if response["error"] is not None:
            raise CommandError(response["error"])


def command(name: str, server_id: str, api_key: str, data: Any = None) -> JSONDict:
    """Send a command to the Gamocosm server.

    - `start` starts the server and Minecraft.
    - `stop` stops the server and Minecraft.
    - `pause` stops Minecraft.
    - `resume` starts Minecraft.
    - `reboot` restarts the Digital Ocean server.
    - `backup` makes a zipped backup of the current world and puts it in
      the remote `backups` folder.
    - `status` returns a dictionary with keys:
        - `server`: true if the DO server is created and active
        - `status`: pending operation of the server (`null` if not doing
          anything, otherwise doing something like `starting` or
          `preparing` or `saving`
        - `minecraft`: true if Minecraft is running
        - `ip`: IP address of the server (or `null` if server is not
          running
        - `domain`: domain of the server (should never be `null`)
        - `download`: download URL; `null` if server has not fully
          started
    - `exec` executes a Minecraft command, given data of the form
      `{"command": <command string>}`.

    Parameters
    ----------
    name: "start", "stop", "pause", or "resume"
        The name of the command.
    server_id: str
        The server id.
    api_key: str
        The API key for the server (found under Advanced Settings).
    data: optional
        Extra data to be passed to the POST request.

    Returns
    -------
    JSONDict
        The returned JSON.

    Raises
    ------
    KeyError
        If the command name is not valid.
    """
    valid_commands = [
        "start",
        "stop",
        "pause",
        "resume",
        "reboot",
        "backup",
        "status",
        "exec",
    ]
    if name not in valid_commands:
        raise ValueError(name)
    url = f"https://gamocosm.com/servers/{server_id}/api/{api_key}/{name}"
    if name == 'status':
        r = requests.get(url=url, data=data)
    else:
        r = requests.post(url=url, data=data)
    return r.json()

