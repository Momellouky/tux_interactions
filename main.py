import color_detector.color_detector as cd 
import Direction.face_tracking as ft 
import socket
import threading

address = ('localhost', 6006)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# GAME CONTROLS OBJECTS 
color_detector = cd.Color_Detector(0)
head_tracking = ft.Head_tracking(0)

# THREADS FOR EACH PROGRAM 
results = []
cd_thread = threading.Thread(target=lambda: results.append(color_detector.detect()))
ht_thread = threading.Thread(target=lambda: results.append(head_tracking.get_left_right(None)))
while True : 

  ## GAME CODE HERE 
  cd_thread.start()
  ht_thread.start()

  # Synching threads
  cd_thread.join()
  ht_thread.join()

  # Get results from function running in threads 
  color = results[0]
  head = results[1]
