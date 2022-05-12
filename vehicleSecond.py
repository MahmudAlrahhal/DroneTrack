from __future__ import print_function
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative,Command
from pymavlink import mavutil
# Set up option parsing to get connection string
import argparse

def connectMyCopter():
    global vehicle
    parser = argparse.ArgumentParser(description='commands')
    parser.add_argument('--connect')
    # args = parser.parse_args()

    connection_string = '127.0.0.1:14551'

    if not connection_string:
       import dronekit_sitl
       sitl = dronekit_sitl.start_default()
       connection_string = sitl.connection_string()

    vehicle = connect(connection_string,wait_ready=True)

    return vehicle


def arm_and_takeoff(aTargetAltitude):

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)



def location_callback(self, attr_name, value):
    point1 = LocationGlobalRelative(value.lat,value.lon,value.alt)
    vehicle.simple_goto(point1) 



vehicle = connectMyCopter()
arm_and_takeoff(10)
first_vehicle_connection_string = '127.0.0.1:14552' # We have to give the drone connection information to follow.
vehicle_first = connect(first_vehicle_connection_string,wait_ready=True)


vehicle_first.add_attribute_listener('location.global_frame', location_callback)
time.sleep(500)

