import cv2
import os
import datetime
import numpy as np

# Configuration des chemins
SAVE_IMG = "visages_detectes"  # Dossier pour sauvegarder les images avec visages détectés
SAVE_VID = "videos_enregistrees"  # Dossier pour sauvegarder les vidéos enregistrées

# Création automatique des dossiers s'ils n'existent pas
for d in [SAVE_IMG, SAVE_VID]:
    os.makedirs(d, exist_ok=True)  # Crée les dossiers nécessaires

# Chargement du classifieur Haar Cascade officiel d'OpenCV pour la détection faciale
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
# Chargement du classifieur Haar Cascade pour la détection des yeux
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

def apply_pro_filters(frame):
    """Améliore la qualité de l'image avant détection."""
    # 1. Passage en niveaux de gris 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 2. Filtre Gaussien : lisse l'image pour supprimer le "bruit" (grains)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)  # Noyau de taille 5x5
    # 3. Égalisation d'histogramme : booste le contraste(aide si l'éclairage est mauvais)
    equalized = cv2.equalizeHist(blurred)
    return equalized

def detect_on_image(path, config):
    """Détecte les visages et les yeux sur une image statique."""
    img = cv2.imread(path)  # Lecture de l'image depuis le chemin
    if img is None: return  # Si l'image n'est pas valide, on quitte
    
    # Prétraitement de l'image
    processed = apply_pro_filters(img)
    # Détection des visages avec les paramètres de sensibilité
    faces = face_cascade.detectMultiScale(processed, 1.1, 5)

    for (x, y, w, h) in faces:
        # Rectangle Cyan autour du visage détecté
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 0), 2)
        
        # Région d'intérêt (ROI) pour la détection des yeux (limité au visage)
        roi_gray = processed[y:y+h, x:x+w]  # Zone du visage en niveaux de gris
        roi_color = img[y:y+h, x:x+w]       # Zone du visage en couleur
        
        # Détection des yeux dans la région du visage
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 3)
        
        for (ex, ey, ew, eh) in eyes:
            # Dessine des petits carrés cyan pour les yeux
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (255, 255, 0), 2)
            # Dessine un petit cercle à l'intérieur de chaque œil détecté 
            center = (ex + ew//2, ey + eh//2)
            radius = min(ew, eh) // 4
            cv2.circle(roi_color, center, radius, (0, 255, 255), 1)

    # Sauvegarde si activée dans l'interface
    if config.get("save"):
        ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')  # Timestamp pour nom unique
        cv2.imwrite(os.path.join(SAVE_IMG, f"face_{ts}.png"), img)  # Sauvegarde l'image

    # Affichage de l'image avec détections
    cv2.imshow("Détection de visage - Image", img)
    cv2.waitKey(0)  # Attente d'une touche pour fermer
    cv2.destroyAllWindows()  # Ferme toutes les fenêtres OpenCV

def detect_on_video(source, config):
    """Détecte les visages et les yeux en temps réel sur une vidéo ou webcam."""
    cap = cv2.VideoCapture(source)  # Ouvre la source vidéo 
    writer = None  # Initialise l'enregistreur vidéo
    
    while True:
        ret, frame = cap.read()  # Lit une frame de la vidéo
        if not ret: break  # Si aucune frame n'est lue, on sort de la boucle

        processed = apply_pro_filters(frame)  # Prétraitement de la frame
        faces = face_cascade.detectMultiScale(processed, 1.1, 5)  # Détection des visages

        for (x, y, w, h) in faces:
            # Dessine un rectangle autour du visage
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 2)
            
            # Région d'intérêt pour les yeux
            roi_gray = processed[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            
            # Détection des yeux dans le visage
            eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 3)
            
            for (ex, ey, ew, eh) in eyes:
                # Dessine des petits carrés pour les yeux
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (255, 255, 0), 2)
                # Optionnel : ajoute un point central dans l'œil
                center = (ex + ew//2, ey + eh//2)
                cv2.circle(roi_color, center, 2, (0, 255, 255), -1)

        # Enregistrement vidéo si activé
        if config.get("save"):
            if writer is None:
                h, w = frame.shape[:2]  # Récupère les dimensions de la frame
                fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec pour l'enregistrement
                # Chemin unique pour la vidéo enregistrée
                v_path = os.path.join(SAVE_VID, f"record_{datetime.datetime.now().strftime('%H%M%S')}.avi")
                writer = cv2.VideoWriter(v_path, fourcc, 20.0, (w, h))  # 20 FPS
            writer.write(frame)  # Écrit la frame dans le fichier vidéo

        # Affiche la frame avec les détections
        cv2.imshow("Détection de visage - Video (Appuyez sur 'q' pour quitter)", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break  # Quitte avec la touche 'q'

    # Libération des ressources
    cap.release()  # Ferme la capture vidéo
    if writer: writer.release()  # Ferme l'enregistreur vidéo si actif
    cv2.destroyAllWindows()  # Ferme toutes les fenêtres OpenCV