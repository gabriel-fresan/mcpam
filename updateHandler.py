from modrinthHandler import getPlugin
from yaspin import yaspin

def getUpdate(plugins:list, serverType:str="", serverVersion:str=""):
    upToDate=[]
    toUpdate=[]    

    for i in plugins:
        if i["type"] == "modrinth":
            apiResult = getPlugin(i["id"], game_version=serverVersion, mod_loader=serverType)

            if i['version'] == apiResult['id'] or i['version'] == apiResult['name'] or i['version'] == apiResult['version_number']:
                upToDate.append(i["id"])
            else:
                toUpdate.append([i["id"] , i['version'] , apiResult['id']])

        elif i["type"] == "url":
            upToDate.append(i["filename"])

        elif i["type"] == "jenkins":
            upToDate.append(i["job"])
        
    return toUpdate

@yaspin(text="Writing updates...")
def applyUpdate(config:list,toUpdate:list):
    
    for i in config["plugins"]:
        for x in toUpdate:
            if i["type"] =="modrinth":
                if i["id"] == x[0]:
                    i['version'] = x[2]
    
    return config
    
                    
