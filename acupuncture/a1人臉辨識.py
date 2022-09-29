import cv2
import matplotlib.pyplot as plt
import mediapipe

img_base = cv2.imread("366256.jpg")
img = img_base.copy()
plt.imshow(img[:, :, ::-1])

faceModule = mediapipe.solutions.face_mesh
face_mesh = faceModule.FaceMesh(static_image_mode=True)
results = face_mesh.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

landmarks = results.multi_face_landmarks[0]

facial_areas = {
    'Contours': faceModule.FACEMESH_CONTOURS
    , 'Lips': faceModule.FACEMESH_LIPS
    , 'Face_oval': faceModule.FACEMESH_FACE_OVAL
    , 'Left_eye': faceModule.FACEMESH_LEFT_EYE
    , 'Left_eye_brow': faceModule.FACEMESH_LEFT_EYEBROW
    , 'Right_eye': faceModule.FACEMESH_RIGHT_EYE
    , 'Right_eye_brow': faceModule.FACEMESH_RIGHT_EYEBROW
    , 'Tesselation': faceModule.FACEMESH_TESSELATION
}
def plot_landmark(img_base, facial_area_name, facial_area_obj):
    
    print(facial_area_name, ":")
    
    img = img_base.copy()
    
    for source_idx, target_idx in facial_area_obj:
        source = landmarks.landmark[source_idx]
        target = landmarks.landmark[target_idx]

        relative_source = (int(img.shape[1] * source.x), int(img.shape[0] * source.y))
        relative_target = (int(img.shape[1] * target.x), int(img.shape[0] * target.y))

        cv2.line(img, relative_source, relative_target, (255, 255, 255), thickness = 2)
    
    fig = plt.figure(figsize = (15, 15))
    plt.axis('off')
    plt.imshow(img[:, :, ::-1])
    plt.show()

for facial_area in facial_areas.keys():
    facial_area_obj = facial_areas[facial_area]
    plot_landmark(img_base, facial_area, facial_area_obj)