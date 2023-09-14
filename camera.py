import cv2
from time import time
from tracker import HandTracker
from classification import HandMovement


class CamController:
    def __init__(self, tracker: HandTracker, flipLeftHand=True, showDebugImages=False, enableDefaultCommands=True):
        self.cap = cv2.VideoCapture(0)
        self.tracker = tracker
        self.flipLeftHand = flipLeftHand
        self.showDebugImages = showDebugImages
        self.enableDefaultCommands = enableDefaultCommands

        self.lhm = HandMovement()
        self.rhm = HandMovement()

    def StartCam(self, callback=None, commands:dict=None):
        t = time()
        while self.cap.isOpened():
            success, image = self.cap.read()
            if not success:
                print("Ignoring empty camera frame")
                continue

            # Mark the image as not writeable to pass by reference and improve performance
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            lh, rh, image = self.tracker.ProcessImg(image, self.flipLeftHand, self.showDebugImages)
            self.lhm.UpdateHand(lh, t - time()) if lh is not None else self.lhm.ClearHand()
            self.rhm.UpdateHand(rh, t - time()) if rh is not None else self.rhm.ClearHand()

            if callback is not None:
                callback(self.lhm, self.rhm, image)

            cv2.imshow('MediaPipe Hands', image)

            t = time()
            k = cv2.waitKey(5)
            if k == 27: # Escape key
                break
            elif k == -1: # No key pressed
                continue
            elif self.enableDefaultCommands and k == ord('h'):
                self.SetDebugImages(not self.showDebugImages)
            elif commands is not None and k in commands.keys():
                commands[k](self.lhm, self.rhm, image)

        self.cap.release()

    def SetDebugImages(self, show):
        self.showDebugImages = show
