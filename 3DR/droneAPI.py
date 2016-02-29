#!/usr/bin/env python

def gps_callback(self, attr_name, value):
  if value != None:
     print(json.dumps({ 'gpsCoords':{ 'lat':value.lat, 'long':value.lon, 'alt':value.alt }}))

def process_command(command,vehicle):
   x = command.split();
   if x[0] == "goto":
      coord_lat = float(x[1])
      coord_long = float(x[2])
      coord_alt = float(x[3])
      cmd_str = "goto " + str(coord_lat) + " " + str(coord_long) + " " + str(coord_alt)
      print(json.dumps({ 'cmd':cmd_str }))
      if vehicle.mode.name != "GUIDED": vehicle.mode = dronekit.VehicleMode("GUIDED")
      a_location = dronekit.LocationGlobal(coord_lat,coord_long,coord_alt)
      vehicle.simple_goto(a_location,groundspeed=2.0)
   elif x[0] == "isArmed":
      isArmed = vehicle.armed
      modeName = vehicle.mode.name
      print(json.dumps({ 'isArmed':isArmed, 'mode':modeName }))
   elif x[0] == "rtl":
      vehicle.mode = dronekit.VehicleMode("RTL")
      print(json.dumps({ 'cmd':'rtl' }))

      
# Connect to UDP endpoint (and wait for default attributes to accumulate)
def main():
   target = "udpin:0.0.0.0:14550"
   vehicle = dronekit.connect(target,wait_ready=True)
   vehicle.add_attribute_listener('location.global_frame', gps_callback)
   while 1:
      line = ""
      for c in raw_input():
         line = line + c
      process_command(line,vehicle)
   vehicle.close()

try:
   import dronekit
   import sys
   import json
   main()
except ImportError:
   pass
