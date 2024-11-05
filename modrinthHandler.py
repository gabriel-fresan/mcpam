import requests
import json
from yaspin import yaspin

@yaspin(text="Feching Modrinth API...")
def getPlugin(project_id="Required", game_version="", mod_loader=""):

    apiUrl = f"https://api.modrinth.com/v2/project/{project_id}/version"
    apiBody={}
    response={}

    if game_version == "" and mod_loader == "":
        response = requests.get(apiUrl)

    if game_version != "" and mod_loader == "":
        apiBody = {
            'game_versions': json.dumps([game_version])
        }
        response = requests.get(apiUrl, params=apiBody)

    if game_version == "" and mod_loader != "":
        apiBody = {
            'loaders': json.dumps([mod_loader])
        }
        response = requests.get(apiUrl, params=apiBody)

    if game_version != "" and mod_loader != "":
        apiBody = {
            'loaders': json.dumps([mod_loader]),
            'game_versions': json.dumps([game_version])
        }
        response = requests.get(apiUrl, params=apiBody)


    if response.status_code == 200:
        versions = response.json()
        for version in versions:
            if len(mod_loader) >= 1:
                if mod_loader in version['loaders']:
                    return version
            else:
                return version
    
    return None

#@yaspin(text="Feching Modrinth API...")
def searchPlugin(name:str,gameVersion:str,modLoader:str):
    apiUrl = f'https://api.modrinth.com/v2/search?index=downloads&query={name}'
    apiBody={}
    response={}

    if len(gameVersion+modLoader) > 0:

        apiUrl=apiUrl+"&facets=["
        modLoaderFilter=len(modLoader) > 0
        gameVersionFilter=len(gameVersion) > 0

        if modLoaderFilter:
            apiUrl=apiUrl+f'["categories:{modLoader}"]'

        if gameVersionFilter and modLoaderFilter:
            apiUrl=apiUrl+','

        if gameVersionFilter:
            apiUrl=apiUrl+f'["versions:{gameVersion}"]'
        
        apiUrl=apiUrl+"]"


    response = requests.get(apiUrl,params=apiBody)

    if response.status_code == 200:
        plugins = response.json()
        return plugins["hits"]
            
    return None