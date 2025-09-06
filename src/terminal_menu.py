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
        self.routes = []
        #system_routes = []
        for sys in self.systems:
            #system_routes = sys.get_available_routes()
            self.routes += sys.get_available_routes()
        is_minimal = False # Used for smaller devices



    def select_route(self):
        print("Please select a route:")

        i = 0
        for route in self.routes:
            print(str(i) + ". " + route.name)
            i += 1

        route_selection = input("\nRoute selection: ")
        route = self.routes[int(route_selection)]

        if int(route_selection) <= len(self.routes) or int(route_selection) < 0:
            print_route_info(route)
            return route
        else:
            print("Invalid route selected.")
            return None

    def __select_stop(self):
        route = self.select_route()

        stop_selection = input("\nSelect a stop: ")
        stop = route.getStops()[int(stop_selection)]

        print_stop_info(route, stop)

    def help(self):
        print("help")

    def show_start_menu(self):
        print("""
  _____              _          _____       _    _____ __  __  _____ 
 |  __ \\            (_)        / ____|     | |  / ____|  \\/  |/ ____|
 | |__) |_ _ ___ ___ _  ___   | |  __  ___ | | | (___ | \\  / | (___  
 |  ___/ _` / __/ __| |/ _ \\  | | |_ |/ _ \\| |  \\___ \\| |\\/| |\\___ \\ 
 | |  | (_| \\__ \\__ \\ | (_) | | |__| | (_) |_|  ____) | |  | |____) |
 |_|   \\__,_|___/___/_|\\___/   \\_____|\\___/(_) |_____/|_|  |_|_____/ 
        
        """)
        
        print("Welcome to Passio Go! SMS")
        print("This is the terminal version primarily used for testing. It lacks SMS capabilities.")

        print("\nPlease enter a command. For help, enter 'help' or '?'")
        start_menu_selection = input("> ")

        if start_menu_selection == "help" or start_menu_selection == '?':
            self.help()




    def show(self):
        self.show_start_menu()
        #self.__select_stop()


def get_system_ids():
    confighandler = config_handler.ConfigHandler()
    system_ids = confighandler.get_system_ids()
    return system_ids

def get_systems():
    confighandler = config_handler.ConfigHandler()
    systems = confighandler.get_systems()
    return [system.System(x[1]) for x in systems] # Create list for each system based on ID


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