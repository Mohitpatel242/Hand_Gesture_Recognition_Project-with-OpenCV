import cv2
import time
import os
import HandTrackingModule as htm
# from cvzone.SerialModule import SerialObject
from pyfirmata import Arduino

wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# arduino = SerialObject("COM3")
board = Arduino("COM3")
# print(board.get_firmata_version())

folderpath  = "resoures"
myList = os.listdir(folderpath)
# print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderpath}/{imPath}')
    print(f'{folderpath}/{imPath}')
    overlayList.append(image)


# print((len(overlayList)))

pTime = 0
cTime = 0

detector = htm.handDetector()

tipIds = [4, 8, 12, 16, 20]

while True:
    success, img =cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img,)
    # print(lmList)

    if len(lmList) != 0:

        fingers = []

        # Thumb
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 fingers
        for id in range(1,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        print(fingers)
        totalFingers = fingers.count(1)
        # print(totalFingers)

        h, w, c = overlayList[totalFingers - 1].shape
        img[0:h, 0:w] = overlayList[totalFingers - 1]


        if fingers[0] == 1:board.digital[13].write(1)
        else:board.digital[13].write(0)

        if fingers[1] == 1:board.digital[12].write(1)
        else:board.digital[12].write(0)

        if fingers[2] == 1:board.digital[11].write(1)
        else:board.digital[11].write(0)

        if fingers[3] == 1:board.digital[10].write(1)
        else:board.digital[10].write(0)

        if fingers[4] == 1:board.digital[9].write(1)
        else:board.digital[9].write(0)

            # board.digital[13].write(1)
            # time.sleep(0.2)
            # board.digital[13].write(0)
            # time.sleep(0.2)

        # def valSend():
        #     if fingers[0] == 1 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
        #         return 1
        #     if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
        #         return 2
        #     if fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
        #         return 3
        #     if fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 1 and fingers[4] == 0:
        #         return 4
        #     if fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
        #         return 5
        #
        #     return 0
        #
        #
        # result = valSend()
        # print(result)
        # arduino.sendData([result])
        # print(arduino.sendData([result]))

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (400, 70), cv2.FONT_HERSHEY_PLAIN, 3,
            (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)



