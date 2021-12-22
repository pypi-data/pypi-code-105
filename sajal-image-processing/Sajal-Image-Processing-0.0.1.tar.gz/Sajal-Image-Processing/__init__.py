import cv2 as cv
import os 
# import numpy as np
# from pathlib import Path

def ReadImage(img_path:str):
    # img_path = r'{}'.format(img_path)
    # print(img_path)
    # img_path = img_path.encode('unicode_escape')
    if os.path.exists(img_path):
        
        img = cv.imread(img_path)
        return img
    
    else:
        print("Image Does not exist")
        return -1
    
    
def ProcessImage(img_array):
    
    img_gray = cv.cvtColor(img_array, cv.COLOR_BGR2GRAY)
    blur_img = cv.GaussianBlur(img_gray,(3,3),0)
    
    return blur_img

def WriteImage(blur_img, out_path:str):
    out_path+="\\test.jpg"
    # out_path = out_path.encode('unicode_escape')
    # out_path = r'{}'.format(out_path)
    cv.imwrite(out_path, blur_img)
    # return out_path
    
    
    