from tracker import HandTracker
from classification import PoseClassifier
from camera import CamController


POSE_FILE = 'NewPoseClassifications'

def CreatePose(lh, rh, image):
    print('Enter a pose name (Leave blank to cancel)')
    n = input('> ')
    if len(n) == 0:
        return
    poses.AddPose(n, rh)
    poses.SavePoses(fname)
    print('Pose saved')
def ShowHands(lh, rh, image):
    cam.SetDebugImages(not cam.showDebugImages)


print(f'Enter a filename (blank for {POSE_FILE}.json)')
fname = input('> ')

if len(fname) == 0:
    fname = POSE_FILE
fname += '.json'

tracker = HandTracker(True)
poses = PoseClassifier(fname)

print('Starting Hand Tracker')
print('Press N to create a new pose')

cam = CamController(tracker)
cam.StartCam(None,
             {
                 ord('n'): CreatePose,
                 ord('h'): ShowHands
             })

