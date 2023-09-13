import cv2
from tracker import HandTracker
from classification import Hand, PoseClassifier
from camera import StartCam


POSE_FILE = 'BasicASL.json'


def DebugOutput(lh:Hand, rh:Hand, image):
    #h, w, c = image.shape

    if rh is not None:
        pose, strength = poses.ClassifyPose(rh)
        s = f'{pose}: {round(strength, 3)}'
        cv2.putText(image, s, (10, 40), cv2.FONT_HERSHEY_PLAIN, 2, ((pose is not None) * 255, 0, (pose is None) * 255), 3)


tracker = HandTracker(False)
poses = PoseClassifier(POSE_FILE)

StartCam(tracker,
         DebugOutput)

