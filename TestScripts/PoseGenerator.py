from tracker import HandTracker
from classification import PoseClassifier, HandMovement
from camera import CamController


POSE_FILE = 'NewPoseClassifications'

def CreatePose(lhm:HandMovement, rhm:HandMovement, image):
    print('Enter a pose name (Leave blank to cancel)')
    n = input('> ')
    if len(n) == 0:
        return
    poses.AddPose(n, rhm.hand)
    poses.SavePoses(fname)
    print('Pose saved')


print(f'Enter a filename (blank for {POSE_FILE}.json)')
fname = input('> ')
if len(fname) == 0:
    fname = POSE_FILE
fname += '.json'

tracker = HandTracker()
poses = PoseClassifier(fname)

print('Starting Hand Tracker')
print('Press N to create a new pose')

cam = CamController(tracker, showDebugImages=True)
cam.StartCam(None,
             {
                 ord('n'): CreatePose
             })

