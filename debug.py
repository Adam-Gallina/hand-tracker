from classification import Hand
import cv2

def DrawHandOrigin(image, hand:Hand, size=10, color=(0, 0, 255)):
    h, w, c = image.shape
    cv2.circle(image, hand.palm.to_img(w, h), size, color, cv2.FILLED)

def DrawHandVectors(image, hand, size=3, color=(0,0,255)):
    h, w, c = image.shape
    for i in range(0, 3):
        cv2.arrowedLine(image,
                        hand.thumb_coord[i].to_img(w, h),
                        (hand.thumb_coord[i] + hand.thumb[i+1] / 20).to_img(w, h),
                        color, size)
