import os 
from datetime import datetime 
import pandas as pd
import cv2 as cv 
import params as p 

class Color_Detector : 

  # default attributes 
  

  def __init__(self, cam_id=0, color_file_name="colors.csv") -> None:
    self.default_webcam_id = 0 
    self.__start_webcam(cam_id)
    self.FILE_NAME = color_file_name
    self.colors_dir = self.__init_default_colors_path()
    self.colors = self.__read_colors() 

  def __init_default_colors_path(self) -> str : 
    print("Looking for the colors csv file")
    CURRENT_DIR = os.getcwd() 
    COLORS_DIR = CURRENT_DIR + "/colors/" + self.FILE_NAME
    DATETIME_NOW = datetime.now()
    print(f"[{DATETIME_NOW}] : We are in the following {CURRENT_DIR}")
    DATETIME_NOW = datetime.now()
    print(f"[{DATETIME_NOW}] : The {self.FILE_NAME} is at {COLORS_DIR}")
    return COLORS_DIR
  
  def __read_colors(self) -> None : 
    index = ["color", "color_name", "hex", "R", "G", "B"]
    
    colors = pd.read_csv(self.colors_dir, names=index, header=None)
    return colors; 

  def __get_color_name(self, colors, R, G, B) -> str:
      minimum = 10000
      for i in range(len(colors)):
          d = abs(R - int(colors.loc[i, "R"])) + abs(G - int(colors.loc[i, "G"])) + abs(B - int(colors.loc[i, "B"]))
          if d <= minimum:
              minimum = d
              cname = colors.loc[i, "color_name"]
      return cname

  def __start_webcam(self, default_cam_id = 0) -> None: 
    # start webcam
    self.cap = cv.VideoCapture(0)
    # cap.set(3, p.CAM_WIDTH)
    # cap.set(4, p.CAM_HEIGHT)
  
  def __extract_color(self, img) :
    '''
      img : a 2x2 matrix representing the frame.
      return the red, green, blue components
    '''
    b, g, r = img[p.Y_POS_SAMPLING, p.X_POS_SAMPLING]
    b = int(b)
    g = int(g)
    r = int(r)

    return r, g, b
  
  def __release_ressource(self, cv) -> None : 
    self.cap.release()
    cv.destroyAllWindows()
  
  def detect_color(self, cap) -> None :

    # cv.namedWindow('Webcam')

    success, img = cap.read()
    if not success : 
        print("We got no frame. ")
    else : 
      # cv.imshow('Webcam', img)

      # extracting color 
      r, g, b = self.__extract_color(img)
      
      # Creating text string to display( Color name and RGB values )
      color_text = self.__get_color_name(self.colors, r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

      return color_text 


