import cv2
import numpy as np
import os

colors = np.load("calibration.npy")
#print(colors)
def match_color(H, S, V):
    this_color = np.array([H, S, V])
    best_match = 0
    lowest_diff = 3*255
    for i, color in enumerate(colors):
        diff = 2*abs(color[0]-this_color[0])
        diff += abs(color[1]-this_color[1])
        if diff < lowest_diff:
            lowest_diff = diff
            best_match = i
    return best_match

def print_face(face):
    for square in face:
        if square == 0: print("orange", end=' ')
        elif square == 1: print("green", end=' ')
        elif square == 2: print("white", end=' ')
        elif square == 3: print("blue", end=' ')
        elif square == 4: print("yellow", end=' ')
        elif square == 5: print("red", end=' ')
    print()

def scan():
    os.system("./config_cam.sh")
    cap = cv2.VideoCapture(0)
    _, img = cap.read()
    height, width, _ = img.shape
    faces = ["Top", "Left", "Front", "Right", "Back", "Bottom"]
    cube_num = []
    print(faces.pop(0))
    cb_size = 300
    sq_size = cb_size//3
    while True:
        _, img = cap.read()
        disp_img = cv2.flip(img, 1)

        for r in range(int((width-cb_size)//2), int((width-cb_size)//2)+cb_size, sq_size):
            for c in range(int((height-cb_size)//2), int((height-cb_size)//2)+cb_size, sq_size):
                start = (r+sq_size//4, c+sq_size//4)
                end = (start[0]+sq_size//2, start[1]+sq_size//2)
                cv2.rectangle(disp_img, start, end, 255, 3)
        disp_img = cv2.copyMakeBorder(disp_img, 400, 400, 800, 800, cv2.BORDER_CONSTANT, value=(255, 255, 255))
        cv2.imshow("cube", disp_img)
        key = cv2.waitKey(33)
        if key == ord('q'):
            break
        elif key == ord('c'):
            hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            # iterate through all the pixels
            face = []
            for r in range(int((height-cb_size)//2), int((height-cb_size)//2)+cb_size, sq_size):
                for c in range(int((width-cb_size)//2), int((width-cb_size)//2)+cb_size, sq_size):
                    start = (r+sq_size//4, c+sq_size//4)
                    end = (start[0]+sq_size//2, start[1]+sq_size//2)
                    H = 0; S = 0; V = 0
                    pixel_count = 0
                    for y in range(start[0], end[0], 5):
                        for x in range(start[1], end[1], 5):
                            H += hsv_img[y, x, 0]
                            S += hsv_img[y, x, 1]
                            V += hsv_img[y, x, 2]
                            pixel_count += 1
                            #cv2.circle(hsv_img, (y, x), 1, 255)
                    H //= pixel_count
                    S //= pixel_count
                    V //= pixel_count
                    #print(H, S, V)
                    face.append(match_color(H, S, V))
            cube_num.append(face)
            print_face(face)
            #cv2.imshow("hsv", hsv_img)

            # prompt
            if (len(faces) > 0):
                print(faces.pop(0))
            else:
                square_list = ["U", "L", "F", "R", "B", "D"]
                for face in cube_num:
                    original = face[4] # center
                    replace_with = square_list.pop(0)
                    if replace_with == "F":
                        continue
                    for face in cube_num:
                        #print(face)
                        for i, square in enumerate(face):
                            if square == original:
                                face[i] = replace_with
                #for face in cube_num:
                #    print(face)
                #    print()
                #print()
                for face in cube_num:
                    for i, square in enumerate(face):
                        if isinstance(square, int):
                            face[i] = "F"
                #for face in cube_num:
                #    print(face)
                #    print()
                #print()
                for i, face in enumerate(cube_num):
                    #print(face)
                    cube_num[i] = "".join(face)
                cube_str = "".join(cube_num)
                os.system("./reverse_cam.sh")
                #print(cube_str)
                return cube_str
                break

if __name__ == "__main__":
    scan()
