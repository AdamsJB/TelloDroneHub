# Import the necessary modules
import socket
import threading
import time
import math
import logging

# IP and port of Tello
tello_address = ('192.168.10.1', 8889)

# IP and port of local computer
local_address = ('', 9594)

# Create a UDP connection that we'll send the command to
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the local address and port
sock.bind(local_address)

# Send the message to Tello and allow for a delay in seconds
def send(message, delay):
  # Try to send the message otherwise print the exception
  try:
    sock.sendto(message.encode(), tello_address)
    print("Sending message: " + message)
  except Exception as e:
    print("Error sending: " + str(e))

  # Delay for a user-defined period of time
  time.sleep(delay)

# Receive the message from Tello
def receive():
  # Continuously loop and listen for incoming messages
  while True:
    # Try to receive the message otherwise print the exception
    try:
      response, ip_address = sock.recvfrom(128)
      print("Received message: " + response.decode(encoding='utf-8'))
    except Exception as e:
      # If there's an error close the socket and break out of the loop
      sock.close()
      print("Error receiving: " + str(e))
      break

# Create and start a listening thread that runs in the background
# This utilizes our receive functions and will continuously monitor for incoming messages
receiveThread = threading.Thread(target=receive)
receiveThread.daemon = True
receiveThread.start()

# Boxlegs Tello uses cm units by default.
box_leg_distance20 =20
box_leg_distance30 = 30
box_leg_distance40 = 40
box_leg_distance50 = 50
box_leg_distance60 = 60
box_leg_distance70 = 70
box_leg_distance100 = 100
box_leg_distance200 = 200
box_leg_distance300 = 300

#Yaw degrees
yaw_angle30 = 30
yaw_angle60 = 60  
yaw_angleNintey = 90
yaw_angle180 = 180
yaw_angle360 = 360

# Yaw clockwise (right)
yaw_ccw = "ccw"
yaw_cw = "cw"

# up / down variables 
down60 = 60
down70 = 70 

#variable for a curve-path 
curveAng= 270, 70, 0, 140, 0, 0, 20
photo_count = 20 
radius = photo_count *5
angle_increment = 360/photo_count
x1=radius
y1=0 
x2= math.cos(angle_increment/180.0 * math.pi) * radius
y2= math.sin(angle_increment/180.0 * math.pi) * radius
distance = math.sqrt((x2 - x1)** 2 + (y2-y1) **2 )

# Curve
# send("command", 4)
# send("battery?", 2)
# send("takeoff", 5)
# send("cw " + str(yaw_angleNintey), 4)
# send("curve 80, 30, 0, 100, 20, 0, 30", 6)
# send("curve -80, -30, 0, -100, -20, 0, 30", 6)
# send("land", 4)
# print("Mission completed successfully!")


# 

def fly_poly(sides):
  for s in range(sides):
    # send("forward " + str(box_leg_distance20), 4)
    send("right " + str(box_leg_distance40), 4)
    send("ccw " + str(yaw_angle360/ sides), 4)
    
try:
  send("command", 3)
  send("takeoff", 6)
  send("down " + str(down60), 5)
  fly_poly(10)

except Exception as e:
  logging.error(e)

send("land", 5)
send("battery?", 4)
# Print message
print("Mission completed successfully!")
# Close the socket
sock.close()
