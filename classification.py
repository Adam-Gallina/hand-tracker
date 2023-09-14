from vector import Vector3
import json
from os import path
from math import atan2, pi, copysign

HAND_LANDMARKS = 21
FINGER_POINTS = 4
FINGERS = [ 'thumb', 'index', 'middle', 'ring', 'pinky' ]

def ProcessFinger(origin: Vector3, finger_coords: tuple[Vector3], angle: Vector3, invertHand=False):
    finger = [(finger_coords[0] - origin).normalize()]
    for i in range(1, FINGER_POINTS):
        finger.append((finger_coords[i] - finger_coords[i - 1]).normalize())

    for i in range(len(finger)):
        if invertHand:
            finger[i].x *= -1
        finger[i] = finger[i].rotate(angle)

    return tuple(finger)

# X axis parallel with thumb
# Y axis parallel to ring finger
# Z axis perpendicular to palm
def CalcHandAngle(upV:Vector3, sideV:Vector3):
    x = atan2(upV.z, upV.y)
    y = atan2(sideV.z, sideV.x)
    z = atan2(upV.x, upV.y)
    return Vector3(copysign(pi - abs(x), x),
                   y,
                   copysign(pi - abs(z), z))


class Hand:
    def __init__(self, palm, thumb, index, middle, ring, pinky, invertHand=False):
        self.palm = palm
        self.thumb_coord = thumb
        self.index_coord = index
        self.middle_coord = middle
        self.ring_coord = ring
        self.pinky_coord = pinky

        # angle is in radians
        self.angle = CalcHandAngle(self.ring_coord[0] - self.palm, self.thumb_coord[0] - self.palm)

        self.thumb = ProcessFinger(palm, thumb, -self.angle, invertHand)
        self.index = ProcessFinger(palm, index, -self.angle, invertHand)
        self.middle = ProcessFinger(palm, middle, -self.angle, invertHand)
        self.ring = ProcessFinger(palm, ring, -self.angle, invertHand)
        self.pinky = ProcessFinger(palm, pinky, -self.angle, invertHand)

    def get_finger(self, finger, coords=False):
        if finger == 'thumb':
            return self.thumb_coord if coords else self.thumb
        elif finger == 'index':
            return self.index_coord if coords else self.index
        elif finger == 'middle':
            return self.middle_coord if coords else self.middle
        elif finger == 'ring':
            return self.ring_coord if coords else self.ring
        elif finger == 'pinky':
            return self.pinky_coord if coords else self.pinky

    def ToJson(self):
        return {
            'palm': self.palm.ToJson(),
            'thumb': [i.ToJson() for i in self.thumb_coord],
            'index': [i.ToJson() for i in self.index_coord],
            'middle': [i.ToJson() for i in self.middle_coord],
            'ring': [i.ToJson() for i in self.ring_coord],
            'pinky': [i.ToJson() for i in self.pinky_coord]
        }

    # Score similarity based on the COS of the angle between vectors
    def Compare(self, other):
        score = self.palm.cos(other.palm)
        for name in FINGERS:
            f = self.get_finger(name)
            of = other.get_finger(name)
            for i in range(1, len(f)):
                score += f[i].cos(of[i])

        # Not using first knuckles as those don't move
        score /= HAND_LANDMARKS - 5 # [-1, 1]
        score = (score + 1) / 2 # [0, 1]

        return score ** 3

# Array to Vector3
def AtoV3(arr):
    return Vector3(arr[0], arr[1], arr[2])

class PoseClassifier:
    def __init__(self, filename):
        self.poses = {}

        if path.isfile(filename):
            with open(filename, 'r') as f:
                data = json.load(f)

            for k in data.keys():
                self.poses.update({
                    k: Hand(AtoV3(data[k]['palm']),
                            (AtoV3(data[k]['thumb'][0]), AtoV3(data[k]['thumb'][1]), AtoV3(data[k]['thumb'][2]), AtoV3(data[k]['thumb'][3])),
                            (AtoV3(data[k]['index'][0]), AtoV3(data[k]['index'][1]), AtoV3(data[k]['index'][2]), AtoV3(data[k]['index'][3])),
                            (AtoV3(data[k]['middle'][0]), AtoV3(data[k]['middle'][1]), AtoV3(data[k]['middle'][2]), AtoV3(data[k]['middle'][3])),
                            (AtoV3(data[k]['ring'][0]), AtoV3(data[k]['ring'][1]), AtoV3(data[k]['ring'][2]), AtoV3(data[k]['ring'][3])),
                            (AtoV3(data[k]['pinky'][0]), AtoV3(data[k]['pinky'][1]), AtoV3(data[k]['pinky'][2]), AtoV3(data[k]['pinky'][3]))
                        )
                })

            print(f'Loaded {len(self.poses.keys())} poses')

    def AddPose(self, name, pose: Hand):
        self.poses.update({name: pose})

    def SavePoses(self, filename):
        jsonData = {}
        for i in self.poses.keys():
            jsonData.update({i: self.poses[i].ToJson()})

        with open(filename, 'w') as f:
            json.dump(jsonData, f, indent=2)

    def ClassifyPose(self, hand, threshold=0.5):
        s = 0
        pose = None

        for k in self.poses.keys():
            v = self.poses[k].Compare(hand)
            if v > s:
                s = v
                pose = k

        if s <= threshold:
            return None, (threshold - s) / threshold

        return pose, s
