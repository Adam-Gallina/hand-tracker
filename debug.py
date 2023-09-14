from classification import Hand
from vector import Vector3
import cv2

def DrawHandOrigin(image, hand:Hand, size=10, color=(0, 0, 255)):
    h, w, c = image.shape
    cv2.circle(image, hand.palm.to_img(w, h), size, color, cv2.FILLED)

def DrawFingerVectors(image, finger, finger_coord, size=3, color=(0,0,255)):
    h, w, c = image.shape
    for i in range(0, 3):
        cv2.arrowedLine(image,
                        finger_coord[i].to_img(w, h),
                        (finger_coord[i] + finger[i+1] / 20).to_img(w, h),
                        color, size)

def DrawHandVectors(image, hand, size=3, color=(0,0,255)):
    DrawFingerVectors(image, hand.thumb, hand.thumb_coord, size, color)
    DrawFingerVectors(image, hand.index, hand.index_coord, size, color)
    DrawFingerVectors(image, hand.middle, hand.middle_coord, size, color)
    DrawFingerVectors(image, hand.ring, hand.ring_coord, size, color)
    DrawFingerVectors(image, hand.pinky, hand.pinky_coord, size, color)

def DrawStationaryFingerVectors(image, origin, finger, size=3, color=(0,0,255)):
    h, w, c = image.shape
    for i in range(0, 4):
        point = (finger[i] / 20).to_img(w, h)
        end = (origin[0] + point[0], origin[1] + point[1])
        cv2.arrowedLine(image,
                        origin,
                        end,
                        color, size)
        origin = end

def DrawStationaryHandVectors(image, origin, hand, size=3, color=(0,0,255)):
    DrawStationaryFingerVectors(image, origin, hand.thumb, size, color)
    DrawStationaryFingerVectors(image, origin, hand.index, size, color)
    DrawStationaryFingerVectors(image, origin, hand.middle, size, color)
    DrawStationaryFingerVectors(image, origin, hand.ring, size, color)
    DrawStationaryFingerVectors(image, origin, hand.pinky, size, color)

def DrawHandAngle(image, origin, angle:Vector3, length=.1, size=3):
    h, w, c = image.shape

    uV = Vector3(0, 1, 0).rotate(angle).to_img(w, h, length)
    rV = Vector3(1, 0, 0).rotate(angle).to_img(w, h, length)
    fV = Vector3(0, 0, 1).rotate(angle).to_img(w, h, length)

    end = (origin[0] + uV[0], origin[1] + uV[1])
    cv2.arrowedLine(image,
                    origin,
                    end,
                    (0, 255, 0), size)
    end = (origin[0] + rV[0], origin[1] + rV[1])
    cv2.arrowedLine(image,
                    origin,
                    end,
                    (0, 0, 255), size)
    end = (origin[0] + fV[0], origin[1] + fV[1])
    cv2.arrowedLine(image,
                    origin,
                    end,
                    (255, 0, 0), size)
