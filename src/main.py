"""
TODO:
Split main and terminal_menu code
Maybe turn this into a module so I can create SMS and terminal?
"""

import random
import passiogo
import requests
UB_STAMPEDE_ID = 4882 # Stampede
UB_SHUTTLE_ID = 5230 # Shuttle

BASE_URL = "https://passiogo.com/mapGetData.php?eta=3&deviceId="
UB_system = passiogo.getSystemFromID(UB_STAMPEDE_ID)
UB_routes = UB_system.getRoutes()

def select_route():
    print("Please select a route:")

    i=0
    for route in UB_routes:
        print(str(i) + ". " + route.name)
        i+=1

    route_selection = input("\nRoute selection: ")
    route = UB_routes[int(route_selection)]

    if int(route_selection) <= len(UB_routes) or int(route_selection) < 0:
        print_route_info(route)
        return route
    else:
        print("Invalid route selected.")
        return None

def print_route_info(route):
    i = 0
    print("\nHere is your route information...")
    print("Route name: " + route.name)
    print("Stops:")
    for stop in route.getStops():
        print(str(i) + " " + stop.name)
        i += 1

def select_stop():
    route = select_route()

    stop_selection = input("\nSelect a stop: ")
    stop = route.getStops()[int(stop_selection)]

    print_stop_info(route, stop)

def print_stop_info(route, stop):
    print("Route Name: " + route.name)
    print("Stop Name: " + stop.name)
    get_etas(stop)

def get_etas(stop):
    #Need to ensure stop_id is string
    stop_id = stop.id
    stop_data = requests.get(BASE_URL +
                             str(random.randint(10000000,99999999)) + "&stopIds=" + str(stop_id))
    stop_json = stop_data.json()

    eta_list = stop_json['ETAs'][stop_id] # Lists all ETAs for stop w/ info about buses, etc.

    for eta in eta_list:
        print("* " + eta['eta'])

select_stop()