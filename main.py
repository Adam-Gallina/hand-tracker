import cv2
from tracker import HandTracker
from classification import Hand, PoseClassifier
from camera import StartCam


POSE_FILE = 'PoseClassifications.json'

def CreatePose(lh, rh, image):
    n = input('Enter a pose name: ')
    poses.AddPose(n, rh)
    print('Pose Added')
def SavePoses(lh, rh, image):
    poses.SavePoses(POSE_FILE)
    print('Poses Saved')


def DebugOutput(lh:Hand, rh:Hand, image):
    #h, w, c = image.shape
    #s = []
    #if lh is not None:
        #s.append('left')
        #cv2.circle(image, lh.palm.to_img(w, h), 10, (255, 0, 0), cv2.FILLED)
    if rh is not None:
        #s.append('right')
        s = []
        pose, strength = poses.ClassifyPose(rh)
        s.append(f'{pose}: {round(strength, 3)}')

        #cv2.circle(image, rh.palm.to_img(w, h), 10, (0, 0, 255), cv2.FILLED)
        #cv2.arrowedLine(image,
        #                rh.palm.to_img(w, h),
        #                (rh.palm + rh.thumb[0] / 20).to_img(w, h),
        #                (0, 0, 255), 3)
        #for i in range(0, 3):
        #    cv2.arrowedLine(image,
        #                    rh.thumb_coord[i].to_img(w, h),
        #                    (rh.thumb_coord[i] + rh.thumb[i+1] / 20).to_img(w, h),
        #                    (0, 0, 255), 3)
        for i in range(len(s)):
            y = 30 + i * 30
            cv2.putText(image, s[i], (10, y), cv2.FONT_HERSHEY_PLAIN, 2, ((pose is not None) * 255, 0, (pose is None) * 255), 3)


tracker = HandTracker(True)
poses = PoseClassifier(POSE_FILE)

StartCam(tracker,
         DebugOutput,
         {
            ord('n'): CreatePose,
            ord('s'): SavePoses
         })

