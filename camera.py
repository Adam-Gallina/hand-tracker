import cv2

from tracker import HandTracker


class CamController:
    def __init__(self, tracker: HandTracker, showDebugImages=False, enableDefaultCommands=True):
        self.cap = cv2.VideoCapture(0)
        self.tracker = tracker
        self.showDebugImages = showDebugImages
        self.enableDefaultCommands = enableDefaultCommands

    def StartCam(self, callback=None, commands:dict=None):
        while self.cap.isOpened():
            success, image = self.cap.read()
            if not success:
                print("Ignoring empty camera frame")
                continue

            # Mark the image as not writeable to pass by reference and improve performance
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            lh, rh, image = self.tracker.ProcessImg(image, self.showDebugImages)

            if callback is not None:
                callback(lh, rh, image)

            cv2.imshow('MediaPipe Hands', image)

            k = cv2.waitKey(5)
            if k == 27: # Escape key
                break
            elif k == -1: # No key pressed
                continue
            elif self.enableDefaultCommands and k == ord('h'):
                self.SetDebugImages(not self.showDebugImages)
            elif commands is not None and k in commands.keys():
                commands[k](lh, rh, image)

        self.cap.release()

    def SetDebugImages(self, show):
        self.showDebugImages = show
