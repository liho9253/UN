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
                    
                
        cv2.imshow("img", img)
    
    if cv2.waitKey(1) == ord("q"):
        break
    
    









