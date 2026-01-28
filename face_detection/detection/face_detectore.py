import cv2
import os
import datetime

# Chargement des classifieurs Haar
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_eye.xml"
)

# Dossier de sauvegarde
SAVE_DIR = "visages_detectes"
os.makedirs(SAVE_DIR, exist_ok=True)


def detect_on_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    for i, (x, y, w, h) in enumerate(faces):
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        face = img[y:y + h, x:x + w]

        filename = os.path.join(
            SAVE_DIR,
            f"face_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}.png"
        )
        cv2.imwrite(filename, face)

    cv2.imshow("Detection Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def detect_on_video(source=0):
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.imshow("Detection Video / Webcam", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
