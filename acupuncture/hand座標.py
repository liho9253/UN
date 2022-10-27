import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands #手部模型
hands = mpHands.Hands()

Draw = mp.solutions.drawing_utils
# Draw.DrawingSpec(color=(0, 0, 255), thickness=5)  點或線的外觀 


while True:
    ret, img = cap.read()
    if ret:
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(imgRGB)
        # print(result.multi_hand_landmarks)
        
        imgHeight = img.shape[0]
        imgWidth = img.shape[1]
        if result.multi_hand_landmarks:
            for handLms in result.multi_hand_landmarks:
                Draw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
                for i, lm in enumerate(handLms.landmark):
                    xPos = int(lm.x * imgWidth)
                    yPos = int(lm.y * imgHeight)
                    
                    cv2.putText(img, str(i), (xPos-25, yPos+5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 2)
                    print(i, xPos, yPos)
                    
                    # if ( i == 6 ) | ( i == 7 ):
                    #     xPos = int(lm.x * imgWidth)
                    #     yPos = int(lm.y * imgHeight)
                    #     if i == 6:
                    #         xp6 =  int(lm.x * imgWidth)
                    #         yp6 =  int(lm.y * imgHeight)
                    #         zp6 =  int(lm.z)
                    #     if i == 7:
                    #         xp7 =  int(lm.x * imgWidth)
                    #         yp7 =  int(lm.y * imgHeight)
                    #         zp7 =  int(lm.z)
                    #     cv2.putText(img, str(i), (xPos-25, yPos+5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 2)
                        
                # len67 = ((xp6-xp7)**2+(yp6-yp7)**2)**0.5
                # len67 = ((xp6-xp7)**2+(yp6-yp7)**2+(zp6-zp7)**2)**0.5
                # print(int(len67))
                
        cv2.imshow("img", img)
    
    if cv2.waitKey(1) == ord("q"):
        break
    
    









