import random
from xml.etree.ElementTree import tostring

import passiogo
import requests
import json
UB_STAMPEDE_ID = 4882 # Stampede
UB_SHUTTLE_ID = 5230 # Shuttle
UB_system = passiogo.getSystemFromID(UB_STAMPEDE_ID)
UB_routes = UB_system.getRoutes()

def print_stops():
    i = 0
    for route in UB_routes:
        print("Route " + str(i) + ": " + route.name)
        for stop in route.getStops():
            print(stop.name)
        print("")
        i+=1

def select_route():
    i=0
    for route in UB_routes:
        print(str(i) + " " + route.name)
        i+=1

    route_selection = input("\nSelect a route: ")
    route = UB_routes[int(route_selection)]
    print("")
    i = 0
    if int(route_selection) <= len(UB_routes) or int(route_selection) < 0:
        print("Here is your route information...")
        print("Route name: "+ route.name)
        print("Stops:")
        for stop in route.getStops():
            print(str(i) + " " + stop.name)
            i+=1
        return [route_selection, route]
    else:
        print("Invalid route selected.")
        return None


def select_stop():
    route_info = select_route()
    route_selection = route_info[0]
    route = route_info[1]

    stop_selection = input("\nSelect a stop: ")
    get_stop_info(route_selection, stop_selection)


def get_stop_info(route_id, stop_id):
    route = UB_routes[int(route_id)]

    stop = route.getStops()[int(stop_id)] # OK up to here
    print("Route Name: " + route.name + " (ID " + str(stop_id) + ")")
    print("Stop Name: " + stop.name)
    get_etas(stop.id)

def get_etas(stop_id):
    #Need to ensure stop_id is string
    stop_data = requests.get("https://passiogo.com/mapGetData.php?eta=3&deviceId=" +
                             str(random.randint(10000000,99999999)) +"&stopIds=" + str(stop_id))
    stop_json = stop_data.json()

    eta_list = stop_json['ETAs'][stop_id] # Lists all ETAs for stop w/ info about buses, etc.

    for eta in eta_list:
        print("* " + eta['eta'])

select_stop()

"""
all_stops_id = 3
print("Buses for " + UB_routes[all_stops_id].getStops()[0].name + " on the " + UB_routes[all_stops_id].name + " route arrive in:")
get_etas(str(UB_routes[all_stops_id].getStops()[0].id))
"""
"""
ID  System Name
5230 UB Shuttle
4882 UB Stampede"""

"""
To find ID:
systems = passiogo.getSystems()

for system in systems:
    print(str(system.id)+ " " + system.name)
"""
