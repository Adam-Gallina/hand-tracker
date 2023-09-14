import cv2
from tracker import HandTracker
from classification import Hand, PoseClassifier
from camera import CamController


POSE_FILE = 'TestScripts\\BasicASL.json'

def CreatePose(lh, rh, image):
    n = input('Enter a pose name: ')
    poses.AddPose(n, rh)
    print('Pose Added')
def SavePoses(lh, rh, image):
    poses.SavePoses(POSE_FILE)
    print('Poses Saved')
def ShowHands(lh, rh, image):
    cam.SetDebugImages(not cam.showDebugImages)


def DebugOutput(lh:Hand, rh:Hand, image):
    s = []
    if lh is not None:
        pose, strength = poses.ClassifyPose(lh)
        s.append((f'(L) {pose}: {round(strength, 3)}', ((pose is not None) * 255, 0, (pose is None) * 255)))

    if rh is not None:
        pose, strength = poses.ClassifyPose(rh)
        s.append((f'(R) {pose}: {round(strength, 3)}', ((pose is not None) * 255, 0, (pose is None) * 255)))

    for i in range(len(s)):
        y = 30 + i * 30
        cv2.putText(image, s[i][0], (10, y), cv2.FONT_HERSHEY_PLAIN, 2, s[i][1], 3)


tracker = HandTracker()
poses = PoseClassifier(POSE_FILE)

cam = CamController(tracker)
cam.StartCam(DebugOutput,
             {
                 ord('n'): CreatePose,
                 ord('s'): SavePoses,
                 ord('h'): ShowHands
             })

