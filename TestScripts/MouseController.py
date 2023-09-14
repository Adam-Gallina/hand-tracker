import cv2
from tracker import HandTracker
from classification import HandMovement, PoseClassifier
from camera import CamController
from math import degrees
from debug import DrawHandVectors, DrawStationaryHandVectors, DrawHandAngle


POSE_FILE = 'TestScripts\\BasicASL.json'


def DebugOutput(lhm:HandMovement, rhm:HandMovement, image):
    h, w, c = image.shape
    s = []
    if lhm.hand is not None:
        pose, strength, angle = poses.ClassifyPose(lhm.hand)
        s.append(f'(L) {pose}: {round(strength, 3)}, {round(angle, 3)}')
        s.append(f'(L) ({round(degrees(lhm.hand.angle.x), 1)}, {round(degrees(lhm.hand.angle.y), 1)}, {round(degrees(lhm.hand.angle.z), 1)}')
    if rhm.hand is not None:
        pose, strength, angle = poses.ClassifyPose(rhm.hand)
        s.append(f'(R) {pose}: {round(strength, 3)}, {round(angle, 3)}')
        s.append(f'(R) ({round(degrees(rhm.hand.angle.x), 1)}, {round(degrees(rhm.hand.angle.y), 1)}, {round(degrees(rhm.hand.angle.z), 1)}')

    for i in range(len(s)):
        y = 30 + i * 30
        cv2.putText(image, s[i], (10, y), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)


tracker = HandTracker()
poses = PoseClassifier(POSE_FILE)
cam = CamController(tracker)
cam.StartCam(DebugOutput)
