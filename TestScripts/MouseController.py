import cv2
from tracker import HandTracker
from classification import HandMovement, PoseClassifier
from camera import CamController
from math import degrees
from debug import DrawHandVectors, DrawStationaryHandVectors, DrawHandAngle
from vector import Vector3


POSE_FILE = 'CameraControls.json'

dots = []
closed = False
pos = Vector3(50, 50, 0)
def DebugOutput(lhm:HandMovement, rhm:HandMovement, image):
    global pos, closed

    h, w, c = image.shape
    s = []
    if rhm.hand is not None:
        pose, strength, angle = poses.ClassifyPose(rhm.hand)
        s.append(f'(R) {pose}: {round(strength, 3)}, {round(angle, 3)}')
        s.append(f'(R) ({round(degrees(rhm.hand.angle.x), 1)}, {round(degrees(rhm.hand.angle.y), 1)}, {round(degrees(rhm.hand.angle.z), 1)}')

        if pose in ['PinchOpen', 'PinchClosed']:
            if pose == 'PinchClosed':
                if not closed:
                    dots.append(pos.to_img())
                    closed = True
            else:
                closed = False

            pos += rhm.velocity * 20

    cv2.circle(image, pos.to_img(), 5, (0,0,255), cv2.FILLED)
    for d in dots:
        cv2.circle(image, d, 5, (0,0,255), cv2.FILLED)

    for i in range(len(s)):
        y = 30 + i * 30
        cv2.putText(image, s[i], (10, y), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)


tracker = HandTracker()
poses = PoseClassifier(POSE_FILE)
cam = CamController(tracker)
cam.StartCam(DebugOutput)
