import color_detector.color_detector as cd
import params as p
import socket
import cv2 as cv
import color_detector.rgb_extract as rgb_ex
import color_detector.color_store as cs
import csv
import sys
import select
from time import sleep

def read_file(file) : 

  # Create an empty list to store the CSV data
  csv_data = []

  # Open the CSV file and read its contents
  with open(file, newline='', encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile)
    
    # Iterate over each row in the CSV file
    for row in csv_reader:
        # Assuming each row contains only one value, you can use row[0]
        csv_data.append(row[0])

  return csv_data

def click_space(color_name) -> bool : 
  arrow = read_file(p.ARROW_FILE)
  bowling_ball = read_file(p.BOWLING_BALL_FILE)
  # skimmer = read_file(p.SKIMMER_FILE)
  # anchor = read_file(p.ANCHOR_FILE)
  # bullet = read_file(p.BULLET_FILE)
  # basketball = read_file(p.BASKETBALL_FILE)
  # parachute = read_file(p.PARACHUTE_FILE)
  # planger = read_file(p.PLANGER_FILE)
  # cupcake = read_file(p.CUPCAKE_FILE)

  if color_name in (arrow or bowling_ball) : # or basketball or bowling_ball or skimmer or anchor or bullet or parachute or planger or cupcake: 
    return True
  
  return False


address = ('localhost', 6006)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

color_detector = cd.Color_Detector(cam_id=0)
color_store = cs.Color_store()

while True : 
  color = color_detector.detect()
  r, g, b = rgb_ex.Rgb_Extract.extract_rgb(color)
  color_name = rgb_ex.Rgb_Extract.extract_color_name(color)
  print(f"{color_name} Red: {r}, Green: {g}, Blue: {b}")
  # color_store.append_arrow_rgb(r, g, b)
  # color_store.append_color_name("bowling_ball_colors.csv", color_name)
  res = click_space(color_name)
  print(f"res : {res}")
  if res : 
    client_socket.sendto(b'P_FIRE', address)
    sleep(1/60)
    client_socket.sendto(b'R_FIRE', address)
  if cv.waitKey(1) & 0xFF == ord('q'):
    break
  

# color_store.plot_arrow()


# sleep(3)
# data = b'P_LEFT'
# client_socket.sendto(data, address)
# sleep(3)
# data = b'R_LEFT'
# client_socket.sendto(data, address)
# sleep(3)
# data = b'BLAH BLAH BLAH'
# client_socket.sendto(data, address)

