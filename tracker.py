import mediapipe as mp
from classification import Hand
from vector import Vector3

# Landmark to Vector3
def LtoV3(landmark):
    return Vector3(landmark.x, landmark.y, landmark.z)

# Landmark to Vector3 mirroring the landmarks
def LLtoV3(landmark):
    return Vector3(-landmark.x, landmark.y, landmark.z)

class HandTracker:
    def __init__(self, ):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
                    max_num_hands=2,
                    model_complexity=0,
                    min_detection_confidence=0.5,
                    min_tracking_confidence=0.5)

    # Returns (LeftHand, RightHand, image)
    def ProcessImg(self, image, generateDebugOutput=False):
        results = self.hands.process(image)

        lh, rh = None, None
        if results.multi_hand_landmarks:
            for i in range(len(results.multi_hand_landmarks)):
                hand_landmarks = results.multi_hand_landmarks[i]

                # Reverse which hand is set, mediapipe assumes a mirrored image
                if results.multi_handedness[i].classification[0].label == 'Left':
                    rh = Hand(LtoV3(hand_landmarks.landmark[0]),
                              (LtoV3(hand_landmarks.landmark[1]), LtoV3(hand_landmarks.landmark[2]), LtoV3(hand_landmarks.landmark[3]), LtoV3(hand_landmarks.landmark[4])),
                              (LtoV3(hand_landmarks.landmark[5]), LtoV3(hand_landmarks.landmark[6]), LtoV3(hand_landmarks.landmark[7]), LtoV3(hand_landmarks.landmark[8])),
                              (LtoV3(hand_landmarks.landmark[9]), LtoV3(hand_landmarks.landmark[10]), LtoV3(hand_landmarks.landmark[11]), LtoV3(hand_landmarks.landmark[12])),
                              (LtoV3(hand_landmarks.landmark[13]), LtoV3(hand_landmarks.landmark[14]), LtoV3(hand_landmarks.landmark[15]), LtoV3(hand_landmarks.landmark[16])),
                              (LtoV3(hand_landmarks.landmark[17]), LtoV3(hand_landmarks.landmark[18]), LtoV3(hand_landmarks.landmark[19]), LtoV3(hand_landmarks.landmark[20])))
                else:
                    lh = Hand(LtoV3(hand_landmarks.landmark[0]),
                              (LtoV3(hand_landmarks.landmark[1]), LtoV3(hand_landmarks.landmark[2]), LtoV3(hand_landmarks.landmark[3]), LtoV3(hand_landmarks.landmark[4])),
                              (LtoV3(hand_landmarks.landmark[5]), LtoV3(hand_landmarks.landmark[6]), LtoV3(hand_landmarks.landmark[7]), LtoV3(hand_landmarks.landmark[8])),
                              (LtoV3(hand_landmarks.landmark[9]), LtoV3(hand_landmarks.landmark[10]), LtoV3(hand_landmarks.landmark[11]), LtoV3(hand_landmarks.landmark[12])),
                              (LtoV3(hand_landmarks.landmark[13]), LtoV3(hand_landmarks.landmark[14]), LtoV3(hand_landmarks.landmark[15]), LtoV3(hand_landmarks.landmark[16])),
                              (LtoV3(hand_landmarks.landmark[17]), LtoV3(hand_landmarks.landmark[18]), LtoV3(hand_landmarks.landmark[19]), LtoV3(hand_landmarks.landmark[20])))

                if generateDebugOutput:
                    self.mp_drawing.draw_landmarks(image,
                                                   hand_landmarks,
                                                   self.mp_hands.HAND_CONNECTIONS,
                                                   self.mp_drawing_styles.get_default_hand_landmarks_style(),
                                                   self.mp_drawing_styles.get_default_hand_connections_style())

        return lh, rh, image
