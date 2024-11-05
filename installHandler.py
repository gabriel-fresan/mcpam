from modrinthHandler import searchPlugin
from yaspin import yaspin
import plugin as pluginObj

@yaspin(text="Searching for plugin/mod...")
def getInstall(plugin:str, serverType:str, serverVersion:str):
    return searchPlugin(plugin, serverVersion, serverType)

@yaspin(text="Searching for plugin/mod...")
def isDupe(plugin:pluginObj, serverConf:list):
    for i in serverConf["plugins"]:
        if i["type"] == "modrinth":
            if i['id'] == plugin.getPlugin()['id']:
                return True
    return False