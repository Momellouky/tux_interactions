import matplotlib.pyplot as plt
import csv 

class Color_store : 

  def __init__(self) -> None:
    self.red = []
    self.green = []
    self.blue = []
    ############################
    # self.arrow = arrow.Arrow()
    # self.basketball = basketball.Basketball()
    ############################
    self.arrow = [] 

  def append_arrow_rgb(self, r, g, b): 
    self.red.append(r)
    self.red.append(g)
    self.red.append(b)

  def append_color_name(self, file_name, color_name) : 

    # Writing to CSV file
    with open(file_name, mode='a', newline='') as file:
      writer = csv.writer(file)
      writer.writerow([color_name])

  def plot_arrow(self) -> None : 
    plt.scatter(range(0, len(self.red), 1), self.red)
    plt.show()