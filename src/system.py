import config_handler
import passiogo

class System:
    def __init__(self, system_id):
        self.id = system_id
        self.system = passiogo.getSystemFromID(int(system_id))
        self.routes = self.system.getRoutes()

    def getRoutes(self):
        return self.system.getRoutes()