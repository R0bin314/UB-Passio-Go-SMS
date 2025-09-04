import passiogo

class System:
    def __init__(self, system_id):
        self.id = system_id
        self.system = passiogo.getSystemFromID(int(system_id))
        self.name = self.system.name
        self.routes = self.system.getRoutes()

    def getRoutes(self): # Naming convention from passio go API
        return self.system.getRoutes()