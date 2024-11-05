import tomli
import tomli_w
from yaspin import yaspin
from plugin import pluginModrinth

# Writes server.toml
@yaspin(text="Writing to config file...")
def setConf(serverToml:list, file="./server.toml"):
    with open(file, "wb") as f:
        tomli_w.dump(serverToml, f)

# Open server.toml and returns formatted content
@yaspin(text="Loading config file...")
def getConf(file="./server.toml"):
    with open(file, "rb") as f:
        serverToml = tomli.load(f)
    return serverToml

# Open server.toml and returns a list with all the plugins
@yaspin(text="Loading config file...")
def getPluginsList(file="./server.toml"):
    return getConf(file)["plugins"]

# Open server.toml and returns the server.jar type
@yaspin(text="Loading config file...")
def getServerType(file="./server.toml"):
    return getConf(file)['jar']['type']

@yaspin(text="Loading config file...")
def getServerVersion(file="./server.toml"):
    return getConf(file)['mc_version']

# Open server.toml and returns the server.jar type
@yaspin(text="Loading config file...")
def addPlugin(conf:list,plugin:pluginModrinth):
    conf["plugins"].append(plugin.getPlugin())
    return conf
