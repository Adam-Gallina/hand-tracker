import cv2
from tracker import HandTracker


def StartCam(tracker: HandTracker, callback=None, commands:dict=None):
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame")
            continue

        # Mark the image as not writeable to pass by reference and improve performance
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        lh, rh, image = tracker.ProcessImg(image)

        if callback is not None:
            callback(lh, rh, image)

        cv2.imshow('MediaPipe Hands', image)

        k = cv2.waitKey(5)
        if k == 27: # Escape key
            break
        elif k == -1: # No key pressed
            continue
        elif commands is not None and k in commands.keys():
            commands[k](lh, rh, image)

    cap.release()
