import cv2
import mediapipe as mp

class HandDetector:
    def __init__(self, mode=False, maxHands=2,modelComplexity=1, detectionCon=0.5, minTrackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.minTrackCon = minTrackCon
        self.modelComplex=modelComplexity
        self.mpHands = mp.solutions.hands # mp的手部支持模塊
        # Hands完成對Hands初始化配置
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex,
                                        self.detectionCon, self.minTrackCon)
        #mode爲True爲圖片輸入
        # maxhand 爲最大手數目
        # modelcomplex爲模型的複雜度
        # detectioncon和trackcon爲置信度閾值，越大越準確
        self.mpDraw = mp.solutions.drawing_utils# 用於繪製
        self.tipIds = [4, 8, 12, 16, 20]#對應手指的指尖
        self.fingers = []
        self.lmList = []

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # 將傳入的圖轉爲RGB模式，
        # 返回一個列表，包含21個標誌點的x、y、z的值
        self.results = self.hands.process(imgRGB)# 完成圖像的處理，輸入必須爲RGB格式的圖片

        if self.results.multi_hand_landmarks:# hands in list
            for handLms in self.results.multi_hand_landmarks:# 提取每個指頭並繪製標點和連接線
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        xList = []
        yList = []
        bbox = []
        bboxInfo =[]
        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                px, py = int(lm.x * w), int(lm.y * h)
                xList.append(px)
                yList.append(py)
                self.lmList.append([px, py])
                if draw:
                    cv2.circle(img, (px, py), 5, (255, 0, 255), cv2.FILLED)
            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            boxW, boxH = xmax - xmin, ymax - ymin
            bbox = xmin, ymin, boxW, boxH
            cx, cy = bbox[0] + (bbox[2] // 2), \
                     bbox[1] + (bbox[3] // 2)
            bboxInfo = {"id": id, "bbox": bbox,"center": (cx, cy)}

            if draw:
                cv2.rectangle(img, (bbox[0] - 20, bbox[1] - 20),
                              (bbox[0] + bbox[2] + 20, bbox[1] + bbox[3] + 20),
                              (0, 255, 0), 2)

        return self.lmList, bboxInfo

    def fingersUp(self):
        if self.results.multi_hand_landmarks:
            myHandType = self.handType()
            fingers = []
            # Thumb
            if myHandType == "Right":
                if self.lmList[self.tipIds[0]][0] > self.lmList[self.tipIds[0] - 1][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            else:
                if self.lmList[self.tipIds[0]][0] < self.lmList[self.tipIds[0] - 1][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # 4 Fingers
            for id in range(1, 5):
                if self.lmList[self.tipIds[id]][1] < self.lmList[self.tipIds[id] - 2][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        return fingers
    # 判別左右手
    def handType(self):
        if self.results.multi_hand_landmarks:
            if self.lmList[17][0] < self.lmList[5][0]:
                return "Right"
            else:
                return "Left"