import glob
import os

import cv2
import time
from email_image import send_email

video = cv2.VideoCapture(0)
# Time apart from each frame, outside of loop to prevent a second delay between frames, now it will simply run a smooth
# video after a 1-second delay
time.sleep(1)

first_frame = None
status_list = []
count = 1


def clean_folder():
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)


while True:
    status = 0
    check, frame = video.read()
    # Will convert the frame into grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Polish the image, takes the image, blur amount and standard deviation
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    # Will open a program which shows the video footage
    # cv2.imshow("My Video", gray_frame_gau)

    # in the first iteration the frame will be equal to the matrix of the first frame, on the first loop, first_frame
    # will be None
    # this saves the first frame to be compared to later
    # Once the firt loop run, first_frame will no longer be None, therefore it will not update after the first loop
    if first_frame is None:
        first_frame = gray_frame_gau

    # Checking the difference between the first frame and current frame
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    # Classify pixels that are 30 or higher and assign them to 255
    # we want to reassign the value to white
    # a List and we want to extract the second value
    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
    # higher iteration = higher processing
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # find contours
    # Detect the contours around the white areas
    # can check all white areas and calculate the area to determine where there are fake positives
    # going to check all the contour areas in the contours variable
    # will extract the dimensions of the positive contour area, the object we are trying to capture
    # will use these dimensions to create a rectangle on the current frame, with proper coloring
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        # this point is when motion or difference is detected, therefore any function that is called upon motion should
        # be placed after here
        x, y, w, h = cv2.boundingRect(contour)
        # specify the frame to add the rectangle to, the top x and y, the bottom x and y, and the color of the rectangle
        # final argument is optional and is the width
        rectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1
            # only want to produce the image if the status is 1, meaning a new object is in the FoV
            cv2.imwrite(f"images/{count}.png", frame)
            count = count + 1
            produced_images = glob.glob("images/*.png")
            image_to_send = produced_images[int(len(produced_images) / 2)]
    # will continually add the status of 1 when a rectangle is present
    status_list.append(status)
    status_list = status_list[-2:]

    # checking if the last two items of the list are 1 and 0, therefore indicating that the object has left the video
    if status_list[0] == 1 and status_list[1] == 0:
        send_email(image_to_send)
        clean_folder()

    # Will result in the current frame with a rectangle on the motion captured image
    cv2.imshow("My Video", frame)
    # await a key input
    key = cv2.waitKey(1)

    # when the user clicks the q key, break out of the loop
    if key == ord("q"):
        break

# Stops the video footage
video.release()
