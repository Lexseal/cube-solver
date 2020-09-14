import cv2
import numpy as np
import os

"""
Capture an image with the webcam and select color with your mouse
"""

def mouseHSV(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN: #checks mouse left button down condition
        img = param[0]
        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        colors = param[1]
        color = []
        
        radius = 30
        H = 0; S = 0; V = 0
        pixel_count = 0
        for r in range(y-radius, y+radius, 5):
            for c in range(x-radius, x+radius, 5):
                H += hsv_img[r, c, 0]
                S += hsv_img[r, c, 1]
                V += hsv_img[r, c, 2]
                pixel_count += 1
        color.append(H//pixel_count)
        color.append(S//pixel_count)
        color.append(V//pixel_count)
        colors.append(color)
        print("Coordinates of pixel: X:", x,"Y:", y, "Color:", color)
        if len(colors) >= len(sample_colors):
            print(colors)
            np.save("calibration.npy", np.array(colors))
            cv2.imwrite("calib.jpg", img)
            os.system("./reverse_cam.sh")
            exit()
        print(sample_colors[len(colors)])

os.system("./config_cam.sh")
cap = cv2.VideoCapture(0)
_, img = cap.read()
cv2.namedWindow("cube")
while cv2.waitKey(33) != ord("c"):
    _, img = cap.read()
    img = cv2.copyMakeBorder(img, 400, 400, 800, 800, cv2.BORDER_CONSTANT, value=(255, 255, 255))
    cv2.imshow("cube", img)
height, width, _ = img.shape

sample_colors = ["Orange", "Green", "White", "Blue", "Yellow", "Red"]
colors = []
param = [img, colors]
cv2.setMouseCallback("cube", mouseHSV, param)
print(sample_colors[0])
while cv2.waitKey(33) != ord("q"):
    pass
print(colors)
os.system("./reverse_cam.sh")