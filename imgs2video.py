import cv2
import numpy as np
import glob

img_array = []
img_num = len(glob.glob('./*.jpg'))
for num in range(img_num):
    filename = "{0:0=10d}".format(num)+'.jpg'
    print(filename)
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)


out = cv2.VideoWriter('project.mp4',cv2.VideoWriter_fourcc(*'mp4v'), 15, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()