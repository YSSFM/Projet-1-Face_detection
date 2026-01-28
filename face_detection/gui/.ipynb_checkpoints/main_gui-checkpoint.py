import customtkinter as ctk  # Import de la bibliothèque d'interface graphique moderne
import os  # Pour les opérations système
from tkinter import filedialog  # Pour les dialogues de sélection de fichiers
# On importe les fonctions et les variables de dossiers pour éviter la NameError
from detection.face_detector import detect_on_image, detect_on_video, SAVE_IMG, SAVE_VID

class GlassApp(ctk.CTk):
    """Classe principale de l'application avec effet verre."""
    def __init__(self):
        super().__init__()  # Initialise la classe parente CTk

        # Configuration de la fenêtre
        self.title("Détection de visage - Style Glassmorphisme")  # Titre de la fenêtre
        self.geometry("950x600")  # Dimensions de la fenêtre
        
        # Variable liée à la checkbox 
        self.save_var = ctk.BooleanVar(value=False)

        # 1. Fond principal (Bleu très sombre nuit)
        self.main_bg = ctk.CTkFrame(self, fg_color="#0b0f19") 
        self.main_bg.pack(fill="both", expand=True)  # Remplit tout l'espace

        # 2. Panneau central 
        self.glass_panel = ctk.CTkFrame(
            self.main_bg, 
            fg_color="#161b2b", # Sombre mais légèrement bleuté
            corner_radius=25,  # Coins arrondis
            border_width=2,  # Épaisseur de la bordure
            border_color="#00d2ff" # Bordure néon Cyan
        )
        # Place le panneau au centre de la fenêtre
        self.glass_panel.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.85, relheight=0.8)

        self.setup_ui()  # Configure l'interface utilisateur

    def setup_ui(self):
        """Configure tous les éléments de l'interface utilisateur."""
        # Titre haut de l'application
        ctk.CTkLabel(self.glass_panel, text="BIENVENUE", font=("Consolas", 16, "bold"), text_color="#ffffff").pack(pady=(25, 5))
        
        # Séparateur horizontal fin entre le titre et le contenu
        ctk.CTkFrame(self.glass_panel, height=1, fg_color="#334155").pack(fill="x", padx=100, pady=10)

        # Conteneur pour séparer Gauche et Droite
        content = ctk.CTkFrame(self.glass_panel, fg_color="transparent")
        content.pack(expand=True, fill="both", padx=40)

        # CÔTÉ GAUCHE (Boutons Actions) 
        left_side = ctk.CTkFrame(content, fg_color="transparent")
        left_side.pack(side="left", expand=True, fill="both")

        # Style commun pour tous les boutons d'analyse
        btn_style = {"width": 210, "height": 45, "border_width": 1, "fg_color": "transparent", 
                     "border_color": "#00d2ff", "hover_color": "#00354d", "font": ("Cosolas", 13)}

        # Bouton pour analyser une image
        ctk.CTkButton(left_side, text="Analyser une image", command=self.action_img, **btn_style).pack(pady=10)
        # Bouton pour analyser une vidéo
        ctk.CTkButton(left_side, text="Analyser une vidéo", command=self.action_vid, **btn_style).pack(pady=10)
        # Bouton pour utiliser la webcam en temps réel
        ctk.CTkButton(left_side, text="Webcam Temps réel", command=self.action_web, **btn_style).pack(pady=10)
        
        # Bouton Quitter (rouge pour être visible)
        ctk.CTkButton(left_side, text="Quitter", fg_color="#7f1d1d", text_color="white", 
                      width=120, command=self.quit).pack(pady=35)

        # CÔTÉ DROIT (Texte Logo & Consultation) ---
        right_side = ctk.CTkFrame(content, fg_color="transparent")
        right_side.pack(side="right", expand=True, fill="both")

        # Texte principal du logo (explication de l'application)
        logo_text = "Détection de Visage\npar l'algorithme Haar\nCascade."
        ctk.CTkLabel(right_side, text=logo_text, font=("Consolas", 30, "bold"), 
                    justify="left", text_color="#ffffff").pack(pady=20)

        # Bouton pour ouvrir le dossier des images enregistrées
        ctk.CTkButton(right_side, text="Consulter les images enregistrées", fg_color="#1e293b", 
                      command=lambda: os.startfile(SAVE_IMG)).pack(pady=8, fill="x")
        # Bouton pour ouvrir le dossier des vidéos enregistrées
        ctk.CTkButton(right_side, text="Consulter les vidéos enregistrées", fg_color="#1e293b", 
                      command=lambda: os.startfile(SAVE_VID)).pack(pady=8, fill="x")

        # BAS (Checkbox de sauvegarde)
        footer = ctk.CTkFrame(self.glass_panel, fg_color="transparent")
        footer.pack(side="bottom", fill="x", padx=30, pady=20)

        # Checkbox pour activer/désactiver la sauvegarde
        self.chk = ctk.CTkCheckBox(footer, text="Enregistrer l'image/vidéo analysée", 
                                   variable=self.save_var, text_color="#ffffff",
                                   fg_color="#00d2ff", hover_color="#00d2ff")
        self.chk.pack(side="right")  # Aligné à droite

    # Fonctions de rappel des boutons
    def action_img(self):
        """Ouvre un dialogue pour sélectionner une image à analyser."""
        p = filedialog.askopenfilename()  # Ouvre le dialogue de sélection de fichier
        if p:  # Si un fichier a été sélectionné
            detect_on_image(p, {"save": self.save_var.get()})  # Lance la détection

    def action_vid(self):
        """Ouvre un dialogue pour sélectionner une vidéo à analyser."""
        p = filedialog.askopenfilename()
        if p:
            detect_on_video(p, {"save": self.save_var.get()})

    def action_web(self):
        """Lance la détection sur la webcam en temps réel."""
        detect_on_video(0, {"save": self.save_var.get()})  # 0 = index de la webcam par défaut

def main_gui():
    """Point d'entrée principal de l'interface graphique."""
    app = GlassApp()  # Crée une instance de l'application
    app.mainloop()  # Lance la boucle principale de l'interface