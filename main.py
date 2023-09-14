import cv2
from tracker import HandTracker
from classification import Hand, PoseClassifier, CalcHandAngle
from camera import CamController
from math import degrees
from debug import DrawHandVectors, DrawStationaryHandVectors, DrawHandAngle
from vector import Vector3, V3toDegree


POSE_FILE = 'TestScripts\\BasicASL.json'

def CreatePose(lh, rh, image):
    n = input('Enter a pose name: ')
    poses.AddPose(n, rh)
    print('Pose Added')
def SavePoses(lh, rh, image):
    poses.SavePoses(POSE_FILE)
    print('Poses Saved')


def DebugOutput(lh:Hand, rh:Hand, image):
    h, w, c = image.shape
    s = []
    if lh is not None:
        #pose, strength = poses.ClassifyPose(lh)
        #s.append((f'(L) {pose}: {round(strength, 3)}', ((pose is not None) * 255, 0, (pose is None) * 255)))
        #s.append(f'(L) ({round(degrees(lh.angle.x), 1)}, {round(degrees(lh.angle.y), 1)}, {round(degrees(lh.angle.z), 1)}')
        DrawHandVectors(image, lh)
    if rh is not None:
        pose, strength = poses.ClassifyPose(rh)
        s.append(f'(R) {pose}: {round(strength, 3)}')
        s.append(f'(R) ({round(degrees(rh.angle.x), 1)}, {round(degrees(rh.angle.y), 1)}, {round(degrees(rh.angle.z), 1)}')
        #DrawHandVectors(image, rh, color=(255, 0, 0))
        DrawStationaryHandVectors(image, (100, h-130), rh)
        DrawHandAngle(image, rh.palm.to_img(w, h), rh.angle)

        a = CalcHandAngle(rh.ring[0], rh.thumb[0])
        s.append(f'(H) ({round(degrees(a.x), 1)}, {round(degrees(a.y), 1)}, {round(degrees(a.z), 1)}')
        DrawHandAngle(image, (100, h-130), a)

    for i in range(len(s)):
        y = 30 + i * 30
        cv2.putText(image, s[i], (10, y), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)


tracker = HandTracker()
poses = PoseClassifier(POSE_FILE)

print(V3toDegree(poses.poses['One'].angle))

cam = CamController(tracker)
cam.StartCam(DebugOutput,
             {
                 ord('n'): CreatePose,
                 ord('s'): SavePoses
             })

