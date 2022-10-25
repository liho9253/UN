import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

IMAGE_FILES = [".\img\h15.jpg"]
with mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=2,
    min_detection_confidence=0.5) as hands:
    for idx, file in enumerate(IMAGE_FILES):
        img = cv2.imread(file)
      
        h, w = img.shape[0], img.shape[1]
        neww = 550
        newh = 730
        
        if w / h >= neww / newh:
            img = cv2.resize(img, (neww, int(h * neww / w)))
        else:
            img = cv2.resize(img, (int(w * newh / h), newh))
            
        image = cv2.flip(img, 1) 
        if h > w:
            coinimage = img[250:490, 0:190]
        else:
            coinimage = img[120:300, 0:190]
            
        coinimage = cv2.cvtColor(coinimage, cv2.COLOR_BGR2GRAY)
        Gauss = cv2.GaussianBlur(coinimage, (3, 3), 0)
        Canny = cv2.Canny(Gauss, 10, 100)
        
        a, b = cv2.findContours(Canny, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
        thresh = cv2.dilate(Canny, kernel)
        thresh = cv2.erode(thresh, kernel)
        closed = cv2.morphologyEx(thresh,cv2.MORPH_CLOSE, kernel, iterations=5)
        opened = cv2.morphologyEx(closed,cv2.MORPH_OPEN, kernel, iterations=5)


        max_area = 0
        for cnt in a:
            x, y, w, h = cv2.boundingRect(cnt)
            rec = cv2.rectangle(opened,(x, y), (x + w, y + h), (255, 255, 0), 2)
            
        # coinlen = w / 96 * 25.4
        cv2.imshow('imgContour', rec)
        print("硬幣: " + str(w))
        prop = w 
        # w : 2.6 = len67 : X 
        # X = len67 * 2.6 / w
        
        
        
        imgHeight = image.shape[0]
        imgWidth = image.shape[1]
        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        
        if not results.multi_hand_landmarks:
          continue
      
        annotated_image = image.copy()
        for hand_landmarks in results.multi_hand_landmarks:
          for i, lm in enumerate(hand_landmarks.landmark):
              if ( i == 10 ) | ( i == 11 ):
                  xPos = int(lm.x * imgWidth)
                  yPos = int(lm.y * imgHeight)
                  if i == 10:
                      xp6 =  int(lm.x * imgWidth)
                      yp6 =  int(lm.y * imgHeight)
                      zp6 =  int(lm.z)
                  elif i == 11:
                      xp7 =  int(lm.x * imgWidth)
                      yp7 =  int(lm.y * imgHeight)
                      zp7 =  int(lm.z)
                      
          len67 = ((xp6-xp7)**2+(yp6-yp7)**2+(zp6-zp7)**2)**0.5
          inc = str(round(len67 * 2.6 /prop, 2))
          print("1吋 = " + str(len67) + "px")
          print("1吋 = " + inc + "cm")
          mp_drawing.draw_landmarks(
              annotated_image,
              hand_landmarks,
              mp_hands.HAND_CONNECTIONS,
              mp_drawing_styles.get_default_hand_landmarks_style(),
              mp_drawing_styles.get_default_hand_connections_style())
        
        print('Handedness:', results.multi_handedness)
        if not results.multi_hand_world_landmarks:
          continue
        for hand_world_landmarks in results.multi_hand_world_landmarks:
          mp_drawing.plot_landmarks(
            hand_world_landmarks, mp_hands.HAND_CONNECTIONS, azimuth=5)
  
        