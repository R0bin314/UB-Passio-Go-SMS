import random
from xml.etree.ElementTree import tostring

import passiogo
import requests
import json
UB_ID = 4882

UB_system = passiogo.getSystemFromID(UB_ID)
UB_routes = UB_system.getRoutes()

route_selection = ""
""""
i = 0
for route in UB_routes:
    print("Route " + str(i) + ": " + route.name)
    for stop in route.getStops():
        print(stop.name)
    print("")
    i+=1
"""

"""
route_selection = input("\nSelect a route: ")
print("")

if int(route_selection) <= len(UB_routes) or int(route_selection) < 0:
    print("Here is your route information...")
    print("Route name: "+ UB_routes[0].name)
    print("Stops:")
    for stop in UB_routes[0].getStops():
        print(stop.name)
else:
    print("Invalid route selected.")
"""

def get_etas(stop_id):
    #Need to ensure stop_id is string
    stop_data = requests.get("https://passiogo.com/mapGetData.php?eta=3&deviceId=" +
                             str(random.randint(10000000,99999999)) +"&stopIds=" + stop_id)
    stop_json = stop_data.json()
    eta_list = stop_json['ETAs'][stop_id] # Lists all ETAs for stop w/ info about buses, etc.

    for eta in eta_list:
        print("* " + eta['eta'])

#print(UB_routes[0].getStops()[0].name)
all_stops_id = 3
print("Buses for " + UB_routes[all_stops_id].getStops()[0].name + " on the " + UB_routes[all_stops_id].name + " route arrive in:")
get_etas(str(UB_routes[all_stops_id].getStops()[0].id))