#M E 369P - Team 4 - Short n' Clean 
#Allen Hewson, Brenda Miltos, Marcie Legarde, Pranay Srivastava
#Edge Detection File:
#    This file prepares images to train the model using edge detection 

#importing required libraries
from asyncore import write
import cv2
import os

folders = ["Cow", "Snake", "Bird", "None"]    # change to what you want your folder names to be
for folder in folders:
  dir = f"D:\marci\Documents\Desktop\ME\ME369P-Project-4-ShortnClean\{folder}"          # change to your file path
  new_dir = f"D:\marci\Documents\Desktop\ME\ME369P-Project-4-ShortnClean\{folder}edge"  # change to your file path
  for item in os.listdir(dir):
      if item.endswith("jpg"):
        img = cv2.imread(os.path.join(dir, item))
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # The image needs to be blurred to improve edge detection
        img_blur = cv2.GaussianBlur(img_gray, (3,3), 0)
        # Get Sobel X and Y edge detection
        sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5) # Combined X
        cv2.imwrite(os.path.join(dir, item), sobelxy)