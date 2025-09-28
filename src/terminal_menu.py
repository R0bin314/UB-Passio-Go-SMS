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
        self.is_minimal = get_minimal()
        self.routes = []
        for sys in self.systems:
            self.routes += sys.get_available_routes()


    def select_route(self):
        print("Please select a route:")

        i = 0
        for route in self.routes:
            print(str(i) + ". " + route.name)
            i += 1

        route_selection = input("\nRoute selection: ")

        if route_selection.isnumeric():
            if int(route_selection) < len(self.routes) or int(route_selection) < 0:
                route = self.routes[int(route_selection)]
                return route
            else:
                return None
        elif route_selection == '#':
            self.show_start_menu()
            return '#'
        else:
            return None

    def __select_stop(self, route=None, stops=None):
        if route is None:
            route = self.select_route()
        if route is None:
            print("Invalid route selected. To return to the menu, select '#'")
            self.__select_stop()
        elif route == '#':
           self.show_start_menu()
        else:

            print_stops(route, stops)
            stop_selection = input("\nSelect a stop: ")
            if stop_selection.isnumeric():
                stops = route.getStops()
                if int(stop_selection) < len(stops) or int(stop_selection) < 0:
                    stop = stops[int(stop_selection)]
                    if print_etas(route, stop) is None: # Stop is passed through to prevent API from being queried twice
                        print("I'm sorry, no busses go to this stop!\n")
                        self.show_start_menu()
                else:
                    print("Invalid stop selected. To return to the menu, select '#'")
                    self.__select_stop(route=route, stops=stops)
            elif stop_selection == '#':
                self.show_start_menu()
            else:
                print("Invalid stop selected. To return to the menu, select '#'")
                self.__select_stop(route=route)

    """def help(self):
        print("help")"""

    def show_start_menu(self):
        if not self.is_minimal:
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

        print("\nTo select a stop, enter 'stop' or '1'. To exit, enter 'exit' or '2'.")
        start_menu_selection = input("> ")

        """if start_menu_selection == "help" or start_menu_selection == '0':
            self.help()"""

        if start_menu_selection == "stop" or start_menu_selection == '1':
            self.__select_stop()

        elif start_menu_selection == 'exit' or start_menu_selection == '2':
            exit()
        else:
            print("Invalid command!\n")
            self.show_start_menu()

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

def get_minimal():
    confighandler = config_handler.ConfigHandler()
    minimal = confighandler.get_minimal()
    return minimal


def print_stops(route, stops=None):
    i = 0
    print("\nHere is your route information...")
    print("Route name: " + route.name)
    print("Stops:")
    if stops is None: # Allows menu to be entered recursively if invalid input is entered
        stops = route.getStops()
    
    for stop in stops:
        print(str(i) + " " + stop.name)
        i += 1


def get_etas(stop):
    #Need to ensure stop_id is string
    stop_id = stop.id
    stop_data = requests.get(BASE_URL +
                             str(random.randint(10000000,99999999)) + "&stopIds=" + str(stop_id))
    stop_json = stop_data.json()


    if stop_id in stop_json['ETAs'].keys():
        eta_list = stop_json['ETAs'][stop_id] # Lists all ETAs for stop w/ info about buses, etc.
        for eta in eta_list:
            print("* " + eta['eta'])
        return 'Success' # Ignore
    else:
        return None


def print_etas(route, stop):
    print("Route Name: " + route.name)
    print("Stop Name: " + stop.name)
    return get_etas(stop)