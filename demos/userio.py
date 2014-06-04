import sys
import math
import SimpleInput
import SimpleOutput

def cal_volume():
  
  radius = 0.0
  height = 0.0
  volume = 0.0
  area   = 0.0
  pi     = 3.1416
 
  radius = requestNumber("Enter the radius of the cylinder")
  height = requestNumber("Enter the height of the cylinder")
  
  area = pi *radius* radius
  volume = area  * height
  
  showInformation("The volume of the cylinder is %.02f " % volume)

cal_volume()
