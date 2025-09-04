import random
import requests

import system
import config_handler

BASE_URL = "https://passiogo.com/mapGetData.php?eta=3&deviceId="

class TerminalMenu:

    def __init__(self):
        # Need to select system

        self.system_ids = get_system_ids()
        self.systems = get_systems()

        self.selected_system : system.System = get_systems()[0]
        self.selected_system_id = self.selected_system.id
        self.selected_routes = self.selected_system.getRoutes()
        self.select_system()
        self.select_stop()

    def select_system(self):
        print("Please select a system:")
        i=0

        for sys in self.systems:
            print(str(i) + ". " + sys.name)
            i+=1
        
        system_selection = input("\nSystem selection: ")
        self.selected_system = self.systems[int(system_selection)]
        self.selected_system_id = self.selected_system.id
        self.selected_routes = self.selected_system.getRoutes()

    def select_route(self):
        print("Please select a route:")

        i = 0
        for route in self.selected_routes:
            print(str(i) + ". " + route.name)
            i += 1

        route_selection = input("\nRoute selection: ")
        route = self.selected_routes[int(route_selection)]

        if int(route_selection) <= len(self.selected_routes) or int(route_selection) < 0:
            print_route_info(route)
            return route
        else:
            print("Invalid route selected.")
            return None

    def select_stop(self):
        route = self.select_route()

        stop_selection = input("\nSelect a stop: ")
        stop = route.getStops()[int(stop_selection)]

        print_stop_info(route, stop)


def get_system_ids():
    confighandler = config_handler.ConfigHandler()
    system_ids = confighandler.get_system_ids()
    return system_ids

def get_systems():
    confighandler = config_handler.ConfigHandler()
    systems = confighandler.get_systems()
    return [system.System(x[1]) for x in systems]
    #return systems



def print_route_info(route):
    i = 0
    print("\nHere is your route information...")
    print("Route name: " + route.name)
    print("Stops:")
    for stop in route.getStops():
        print(str(i) + " " + stop.name)
        i += 1


def get_etas(stop):
    #Need to ensure stop_id is string
    stop_id = stop.id
    stop_data = requests.get(BASE_URL +
                             str(random.randint(10000000,99999999)) + "&stopIds=" + str(stop_id))
    stop_json = stop_data.json()

    eta_list = stop_json['ETAs'][stop_id] # Lists all ETAs for stop w/ info about buses, etc.

    for eta in eta_list:
        print("* " + eta['eta'])


def print_stop_info(route, stop):
    print("Route Name: " + route.name)
    print("Stop Name: " + stop.name)
    get_etas(stop)