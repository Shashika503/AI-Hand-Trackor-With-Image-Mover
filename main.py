import os

import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.65)


class DragImg():
    def __init__(self, path, posOrigin):
        self.posOrigin = posOrigin
        self.path = path

        self.img = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)
        self.size = self.img.shape[:2]

    def update(self, cursor):
        ox, oy = self.posOrigin
        w, h = self.size
        if ox < cursor[0] < ox + w and oy < cursor[1] < oy + h:
            self.posOrigin = cursor[0] - w // 2, cursor[1] - h // 2


path = "Images"
myList = os.listdir(path)
print(myList)

listImg = []
for x, pathImg in enumerate(myList):
    listImg.append(DragImg(f'{path}/{pathImg}', [50 + x * 400, 50]))

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    if hands:

        lmList = hands[0]['lmList']

        length, info, img = detector.findDistance(lmList[8], lmList[12], img)

        if length < 60:
            cursor = lmList[8]
            for imgObject in listImg:
                imgObject.update(cursor)

    try:
        for imgObject in listImg:
            h, w = imgObject.size
            ox, oy = imgObject.posOrigin
            img = cvzone.overlayPNG(img, imgObject.img, [ox, oy])

    except:
        pass
    cv2.imshow("Virtual Image Trackor & Mover", img)
    cv2.waitKey(1)
