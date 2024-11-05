import tomli
import requests
import json
import os
import zipfile

toUpdate=[]
upToDate=[]

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


modrinthPlugins=[]

with open("c:\srv\Mine\Canvas-V2\mcman\server.toml", "rb") as f:
    serverToml = tomli.load(f)

def getNewVersion(project_id, mod_loader):
    apiUrl = f"https://api.modrinth.com/v2/project/{project_id}/version"
    apiBody = {
        'loaders': json.dumps([mod_loader])
    }
    response = requests.get(apiUrl, params=apiBody)
    if response.status_code == 200:
        versions = response.json()
        for version in versions:
            if mod_loader in version['loaders']:
                return version
    
    return None


for i in serverToml["plugins"]:
    if i["type"] == "modrinth":

        apiResult = getNewVersion(i["id"],serverToml['jar']['type'])

        if i['version'] == apiResult['id'] or i['version'] == apiResult['name'] or i['version'] == apiResult['version_number']:
            upToDate.append(i["id"])
        else:
            toUpdate.append([i["id"] , i['version'] , apiResult['id']])


    elif i["type"] == "url":
        upToDate.append(i["filename"])

    elif i["type"] == "jenkins":
        upToDate.append(i["job"])

if len(toUpdate) > 0:
    print(bcolors.OKBLUE+"To Update".center(48,"_")+bcolors.ENDC)
    for i in toUpdate:
        print(bcolors.WARNING + i[0] +bcolors.ENDC+ " " + ("-"*(20 - len(i[0]))) + " | " +bcolors.FAIL+ i[1] + (" "*(9 - len(i[1]))) +bcolors.ENDC+" => " +bcolors.OKGREEN+ (" "*(9 - len(i[2]))) + i[2] +bcolors.ENDC+  " | " )
else:
    print(bcolors.FAIL+"Nothing to update."+bcolors.ENDC)
    quit()

while True:
    confirmation = input("Update everything? (Y/n): ").lower()
    if confirmation in ["n","no","não","nao"]:
        print("Finishing operation")
        quit()
    elif confirmation not in ["n","no","não","nao","y","yes","sim","s",""]:
        pass
    else: 
        break

print(bcolors.OKCYAN+"Updating...\n"+bcolors.ENDC)


with open("c:\srv\Mine\Canvas-V2\mcman\server.toml", "r") as f:
    updateFile=f.read()

for i in toUpdate:
    updateFile=updateFile.replace(i[1], i[2])
    print(bcolors.WARNING + i[0] +bcolors.ENDC+ " " + ("-"*(20 - len(i[0]))) + " | " +bcolors.OKGREEN+ i[2] +bcolors.ENDC+ " <= " +bcolors.OKBLUE+ "Scheduled" +bcolors.ENDC+ " | " )


with open("c:\srv\Mine\Canvas-V2\mcman\server.toml", "w") as f:
    f.write(updateFile)

os.system("cd c:\srv\Mine\Canvas-V2\mcman")

while True:
    confirmation = input("Backup world before update? (Y/n): ").lower()
    if confirmation in ["n","no","não","nao"]:
        print(bcolors.FAIL+bcolors.BOLD+"Skipping Backup!"+bcolors.ENDC)
        break
    elif confirmation not in ["n","no","não","nao","y","yes","sim","s",""]:
        pass
    else: 
        os.system("mcman w pack")
        os.system("copy c:\srv\Mine\Canvas-V2\mcman\server\plugins\ValhallaMMO c:\srv\Mine\Canvas-V2\mcman\config\plugins\ -Recurse -Force")
        os.system("copy C:\srv\Mine\Canvas-V2\mcman\server\plugins\\vane* c:\srv\Mine\Canvas-V2\mcman\config\plugins\ -Recurse -Force")
        break


os.system("mcman build")

with zipfile.ZipFile("c:\srv\Mine\Canvas-V2\mcman\server\plugins\\all-plugins.zip","r") as zip_ref:
    zip_ref.extractall("c:\srv\Mine\Canvas-V2\mcman\server\plugins\\")
    
for file in os.listdir("C:\srv\Mine\Canvas-V2\mcman\server\plugins\\"):
    for x in["vane-regions","vane-permissions", "all-plugins"]:
        if file.startswith(x):
            os.remove(os.path.join("C:\srv\Mine\Canvas-V2\mcman\server\plugins\\", file))


