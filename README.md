# gamocosm-wrapper

A Python wrapper around the [Gamocosm](https://github.com/Gamocosm/Gamocosm/) API.

Requires a `server_list.toml` in the root directory structured like:

```toml
[server1]
server_id = "<server 1's ID>"
api_key = "<server 1's API key>"

[server2]
server_id = "<server 2's ID>"
api_key = "<server 2's API key>"
```

The above example is for two Gamocosm servers labelled as `server1` and `server2`. These names can be picked arbitrarily, but allow you to load a server via `Server.from_toml("server1")` rather than `Server(<server 1's ID>, <server 2's API key>)`.

The server ID can be found in the URL of the Gamocosm server's dashboard page, and the API key can be found under the Advanced Configuration tab.

## Examples

With `server_list.toml` as above, you can start a server with:

```python
from gamocosm import Server

server = Server.from_toml("server1")
server.start()
```

You can then check on the status of it with `server.status()`:

```python
if server.status().minecraft_active:
    print("Minecraft is running!")
else:
    print("Minecraft is not running...")
```

You can pass commands into the server with `server.exec()`:

```python
server.exec("say Jack: Ascend.")
server.exec("kill DerseQueen")
server.exec("op JackNoir")
```

```python
server.exec("ban terminallyCapricious PvP is not allowed on this server!")
server.exec("kick carcinoGeneticist Language!")
```
