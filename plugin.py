class pluginModrinth:
    def __init__(self,id,version):
        self.id=id
        self.version=version
    
    def getPlugin(self):
        return {
            "type":"modrinth",
            "id":self.id,
            "version":self.version
        }