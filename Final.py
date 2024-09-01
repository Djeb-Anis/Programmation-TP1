import sys
import pandas as pd
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QDialog, QTableWidget, \
    QTableWidgetItem, QVBoxLayout, QMessageBox

fichier_csv = "./nutrition.csv"

# Fonction effaçant le reste des boutons et qui présente de nouveaux boutons
def clear_layout(window):
    for i in reversed(range(window.layout.count())):
        widget = window.layout.itemAt(i).widget()
        if widget is not None:
            widget.deleteLater()

# Classe principale pour la fenêtre
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Dimension de la fenêtre principale
        self.setWindowTitle("Nutrition")
        self.setGeometry(100, 100, 800, 600)

        # Organiser les widgets verticalement
        self.layout = QVBoxLayout()

        # Configurer le widget central et le layout
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        self.initialize_ui()

    def initialize_ui(self):
        # Effacer les widgets précédents
        clear_layout(self)

        # Ajouter des boutons dans le menu
        self.Etape_1_button = QPushButton("Afficher les aliments")
        self.Etape_1_button.clicked.connect(self.show_data)  # Fais le lien entre le bouton "Afficher les aliments" et la méthode show_data
        self.layout.addWidget(self.Etape_1_button)

        self.Etape_2_button = QPushButton("Valeur nutritive")
        self.layout.addWidget(self.Etape_2_button)
        self.Etape_2_button.clicked.connect(self.choisir_valeur_nutri_window)

        self.Etape_3_button = QPushButton("ID")
        self.layout.addWidget(self.Etape_3_button)

        self.Etape_4_button = QPushButton("Modifier")
        self.layout.addWidget(self.Etape_4_button)

        self.Etape_5_button = QPushButton("Ajouter")
        self.layout.addWidget(self.Etape_5_button)

        self.boutton_quitter = QPushButton("Quitter")
        self.boutton_quitter.clicked.connect(self.fermer_appli)
        self.layout.addWidget(self.boutton_quitter)

    def show_data(self):
        # Lecture du fichier CSV
        self.df = pd.read_csv(fichier_csv, sep=';')
        self.df_viewer(self.df, "Afficher les aliments")

    # Afficher le fichier au viewer
    def df_viewer(self, df_show, title):
        viewer = Dataviewer(df_show, title)  # Créer une instance pour le fichier CSV
        viewer.exec()

    def fermer_appli(self):
        reponse = QMessageBox.question(self, "Quitter", "Voulez-vous quitter ?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reponse == QMessageBox.StandardButton.Yes:
            QMessageBox.information(self, "Au revoir", "Thank you come again !")
            QApplication.quit()

    def choisir_valeur_nutri_window(self):
        # Lecture du fichier CSV
        self.df = pd.read_csv(fichier_csv, sep=';')

        clear_layout(self)

        # Créer les boutons pour les différentes valeurs nutritives
        self.proteines_button = QPushButton("Protéines")
        self.layout.addWidget(self.proteines_button)
        self.proteines_button.clicked.connect(lambda: self.show_data_viewer('Protéine'))

        self.gras_button = QPushButton("Gras")
        self.layout.addWidget(self.gras_button)
        self.gras_button.clicked.connect(lambda: self.show_data_viewer('gras'))

        self.cholesterol_button = QPushButton("Cholestérol")
        self.layout.addWidget(self.cholesterol_button)
        self.cholesterol_button.clicked.connect(lambda: self.show_data_viewer('Cholestérol'))

        self.sodium_button = QPushButton("Sodium")
        self.layout.addWidget(self.sodium_button)
        self.sodium_button.clicked.connect(lambda: self.show_data_viewer('Sodium'))

        self.back_button = QPushButton("Retour")
        self.layout.addWidget(self.back_button)
        self.back_button.clicked.connect(self.initialize_ui)

    def show_data_viewer(self, nom_button):

        viewer = DataViewer_Etape_2(self.df, nom_button)
        viewer.exec()

class Dataviewer(QDialog):
    def __init__(self, df_show, title):
        super().__init__()
        self.setWindowTitle(title)

        # Organiser la fenêtre de dialogue
        layout = QVBoxLayout()
        # Créer un tableau pour les données
        self.table = QTableWidget()
        # Définir le nombre de lignes et de colonnes en fonction du DataFrame
        self.table.setRowCount(df_show.shape[0])
        self.table.setColumnCount(df_show.shape[1])
        # Définir les titres des colonnes du tableau en fonction du DataFrame
        self.table.setHorizontalHeaderLabels(df_show.columns)

        # Boucle pour ajouter les données du DataFrame
        for i in range(df_show.shape[0]):  # Chaque ligne du DataFrame
            for j in range(df_show.shape[1]):  # Chaque colonne du DataFrame
                self.table.setItem(i, j, QTableWidgetItem(str(df_show.iat[i, j])))  # Création d'un item dans le tableau selon l'emplacement de [i, j]

        # Ajouter le tableau à la fenêtre
        layout.addWidget(self.table)
        # Organiser la fenêtre
        self.setLayout(layout)

class DataViewer_Etape_2(QDialog):
    def __init__(self, original_df, nom_button):
        super().__init__()
        self.setWindowTitle(nom_button)

        # Générer un nouveau DataFrame en utilisant le DataFrame original
        new_df = original_df[['Id', 'Catégorie', 'Description']].copy()
        new_df[nom_button] = original_df[nom_button]

        # Créer un tableau pour les données
        self.table = QTableWidget()

        # Définir le nombre de colonnes et rangées
        self.table.setRowCount(new_df.shape[0])
        self.table.setColumnCount(new_df.shape[1])
        self.table.setHorizontalHeaderLabels(new_df.columns)

        # Ajouter les données au tableau
        for i in range(new_df.shape[0]):
            for j in range(new_df.shape[1]):
                self.table.setItem(i, j, QTableWidgetItem(str(new_df.iat[i, j])))

        # Créer le layout
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

# Créer une instance de QApplication
app = QApplication(sys.argv)
# Créer une instance de MainWindow
window = MainWindow()
window.show()
# Exécuter la boucle de l'application
sys.exit(app.exec())
