import passiogo

class System:
    def __init__(self, system_id):
        self.id = system_id
        self.system = passiogo.getSystemFromID(int(system_id))
        self.name = self.system.name
        self.routes = []
        """for route in self.system.getRoutes():
            if route.outdated != '1':
                self.routes.append(route)"""

        self.routes = [route for route in self.system.getRoutes() if (route.outdated!='1')]

    def get_available_routes(self):
        return self.routes