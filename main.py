import cv2
import time

video = cv2.VideoCapture(0)
# Time apart from each frame, outside of loop to prevent a second delay between frames, now it will simply run a smooth
# video after a 1-second delay
time.sleep(1)

while True:
    check, frame = video.read()
    # Will open a program which shows the video footage
    cv2.imshow("My Video", frame)

    # await a key input
    key = cv2.waitKey(1)

    # when the user clicks the q key, break out of the loop
    if key == ord("q"):
        break

# Stops the video footage
video.release()
