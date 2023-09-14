import cv2
from tracker import HandTracker
from classification import Hand, PoseClassifier
from camera import CamController
import random
import time

POSE_FILE = 'TestScripts\\BasicASL.json'
FRAMES_TO_SWAP = 5
SECS_TO_CORRECT = .75


flashcards = {1:'One', 2:'Two', 3:'Three', 4:'Four', 5:'Five',
              6:'Six', 7:'Seven', 8:'Eight', 9:'Nine', 10:'Ten'}


def GetRandomCard():
    f = random.choice(list(flashcards.keys()))
    return f, flashcards[f]

currCard = GetRandomCard()
score = 0
lastPose = (None, 0)
frameCount = 0
def Flashcards(lh:Hand, rh:Hand, image):
    global lastPose, frameCount, score, currCard
    h, w, c = image.shape

    # Score
    cv2.putText(image, str(score), (10, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)

    currCol = (255, 0, 0)
    if rh is not None:
        pose, strength = poses.ClassifyPose(rh)

        if pose != lastPose[0]:
            frameCount += 1
            if lastPose[0] is None or frameCount >= FRAMES_TO_SWAP:
                lastPose = (pose, time.time())
                frameCount = 0
        #cv2.putText(image, lastPose[0], (10, h - 60), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)

        if lastPose[0] == currCard[1]:
            currCol = (0, 255, 0)
            if time.time() - lastPose[1] >= SECS_TO_CORRECT:
                currCard = GetRandomCard()
                score += 1

    # Curr card
    cv2.putText(image, str(currCard[0]), (int(w / 2), h - 60), cv2.FONT_HERSHEY_PLAIN, 6, currCol, 6)

tracker = HandTracker()
poses = PoseClassifier(POSE_FILE)

cam = CamController(tracker)
cam.StartCam(Flashcards)

