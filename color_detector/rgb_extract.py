import re 

class Rgb_Extract : 

  def __init__(self) -> None:
    self.r = None 
    self.g = None 
    self.b = None 


  @staticmethod
  def extract_rgb(color_string)  : 

    pattern = r'R=(\d+) G=(\d+) B=(\d+)' # color_string's pattern

    
    match = re.search(pattern, color_string) # Use re.search to find the pattern in the color string

    if match:
        # Extract the RGB values from the matched groups
        red_value = int(match.group(1))
        green_value = int(match.group(2))
        blue_value = int(match.group(3))
        return red_value, green_value, blue_value
    else:
        Exception("No match found")

  @staticmethod
  def extract_color_name(color_string) : 

    # Define a regular expression pattern to match the part before "R="
    pattern = r'(.+?)\s+R='

    # Use re.search to find the pattern in the color strings
    match1 = re.search(pattern, color_string)

    if match1:
        # Extract the part before "R=" from the matched group
        color_name = match1.group(1)
        return color_name
    else: 
       return ""

