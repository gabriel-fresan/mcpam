import updateHandler
import installHandler
import configHandler
import plugin

import typer
from typer import secho as echo
from typer import style

import inquirer

app = typer.Typer()

@app.command(name="upgrade",hidden=True)
@app.command(name="update")
def update(configFile:str="./server.toml"):

    pluginsList=configHandler.getPluginsList(configFile)
    serverType=configHandler.getServerType(configFile)
    serverConfig=configHandler.getConf(configFile)


    toUpdate = updateHandler.getUpdate(plugins=pluginsList,serverType=serverType)
    
    updateConfirmed=False

    if len(toUpdate) > 0:

        message=48
        for i in toUpdate:
            if len(str(i[0]+i[1]+i[2]))+11 > message:
                message = len(str(i[0]+i[1]+i[2]))+11

        echo(
            "╭"+
            "To Update"
            .center(
                (message),"─"
            )+
            "╮", 
            fg='blue'
        )

        for i in toUpdate:
            echo(
                style(
                    "│ ", 
                    fg='blue'
                )+
                style(
                    i[0], fg="yellow"
                )+
                " "+ 
                " " *(20 - len(i[0])) +
                " │ " + 
                style(
                    " "*(message - 31 - len(i[1]) - len(i[2]))
                    +i[1] 
                    , fg="red"
                ) +
                " => " +
                style(
                    " "*(9 - len(i[2]))
                    + i[2] 
                    , fg="green"
                )+
                style(
                    " │", 
                    fg='blue'
                )
            )

        echo(
            "╰"+
            ("─"*message)+
            "╯", 
            fg='blue'
        ) 

        updateConfirmed=inquirer.confirm("Should the updates be applied?", default=True)
        
    else:
        echo(style("Nothing to update.",fg='red'))
        updateConfirmed=False

    if updateConfirmed:
        updatedServerConfig=updateHandler.applyUpdate(serverConfig, toUpdate)
        configHandler.setConf(updatedServerConfig, configFile)


@app.command(name="ls", hidden=True)
@app.command(name="list")
def list(configFile:str="./server.toml"):
    pluginsListCrude=configHandler.getPluginsList(configFile)
    pluginsList=[]


    for i in pluginsListCrude:
        if i["type"] == "modrinth":
            pluginsList.append(i["id"])
        elif i["type"] == "url":
            pluginsList.append(i["filename"])
        elif i["type"] == "jenkins":
            pluginsList.append(i["job"])

    if len(pluginsList) > 0:
        message=25
        for i in pluginsList:
            if len(i) > message:
                message = len(i)+5
        echo("╭"+"List".center((message),"─")+"╮", fg='blue')
        for i in pluginsList:
            echo("│ ", nl=False, fg='blue')
            echo("- " + i + ((message-3-len(i))*" "), fg="yellow", nl=False)
            echo("│", fg='blue')
        echo("╰"+("─"*message)+"╯", fg='blue')  


@app.command(name="i",hidden=True)
@app.command(name="install")
def install(query:str,configFile:str="./server.toml"):

    serverType=configHandler.getServerType(configFile) 
    serverVersion=configHandler.getServerVersion(configFile) 
    serverConfig=configHandler.getConf(configFile)

    
    queryResult=installHandler.getInstall(query,serverType,serverVersion)

    choices=[]

    for i in range(len(queryResult)):
        if i > 5:
            break
        choices.append(queryResult[i]["title"])
    choices.append('Cancel')
    
    if len(queryResult) > 0:
        selectedPlugin = inquirer.list_input(
            message="Which of the plugins do you want to install?",
            choices=choices
        )

        for i in queryResult:
            if i["title"] == selectedPlugin:
                selectedPlugin = i 
                break
            elif selectedPlugin == "Cancel":
                echo("Operation Canceled!", fg='red')
            
        
    else:
        echo("Plugin/Mod not found", fg='red')
        quit()

    echo((" - "+selectedPlugin["title"]+" - ").center(len(selectedPlugin["description"])), fg='green')
    echo(selectedPlugin["description"]+'\n')

    if inquirer.confirm("Should the installation be applied?", default=True):
        version=updateHandler.getUpdate([{'type':'modrinth' ,'id':selectedPlugin["slug"],'version':''}])
        pluginToAdd=plugin.pluginModrinth(selectedPlugin["slug"],version[0][2])

        if installHandler.isDupe(pluginToAdd,serverConfig):
            echo("Error, Plugin/Mod already installed!",fg='red')
            echo("Run `update` or `remove` instead.",fg='yellow')
            quit()

        updatedConf=configHandler.addPlugin(serverConfig,pluginToAdd)
        configHandler.setConf(updatedConf,configFile)
    

"""
@app.command()
def test(configFile:str="./server.toml"):

    pluginsList=configHandler.getPluginsList(configFile)
    serverType=configHandler.getServerType(configFile)
    serverConfig=configHandler.getConf(configFile)

    toUpdate = updateHandler.getUpdate(plugins=pluginsList,serverType=serverType)

    updateHandler.applyUpdate(serverConfig,toUpdate)
"""

if __name__ == "__main__":
    app()
