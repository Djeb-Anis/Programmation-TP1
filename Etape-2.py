import sys
import pandas as pd
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QMessageBox, \
    QDialog, QTableWidget, QTableWidgetItem, QVBoxLayout

fichier_csv = ("./nutrition.csv")


########################## Etape 1 : ############################ COMMENTAIRE PARTOUT ############################ PAS TERMINÉ ##################################


# Classe principale pour la fenetre #
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Dimension fenetre principale
        self.setWindowTitle("Nutrition")
        self.setGeometry(100, 100, 800, 600)

        # Lecture du fichier csv
        self.df = pd.read_csv(fichier_csv,
                              sep=";")  # sep = ";" est un parametre pandas qui determine les separateurs dans le fichier

        # Organise les widget verticalement
        self.layout = QVBoxLayout()

        self.clear_layout()

        # Ajout des boutons dans le menu
        self.Etape_1_button = QPushButton("Afficher les aliments")
        self.Etape_1_button.clicked.connect(self.show_data)  # Fais le lien entre le bouton "Afficher les element" et le fichier
        self.layout.addWidget(self.Etape_1_button)

        self.Etape_2_button = QPushButton("Valeur nutritive")
        self.Etape_2_button.clicked.connect(self.choisir_valeur_nutri)
        self.layout.addWidget(self.Etape_2_button)

        self.Etape_3_button = QPushButton("ID")
        self.layout.addWidget(self.Etape_3_button)

        self.Etape_4_button = QPushButton("Modifier")
        self.layout.addWidget(self.Etape_4_button)

        self.Etape_5_button = QPushButton("Ajouter")
        self.layout.addWidget(self.Etape_5_button)

        self.boutton_quitter = QPushButton("Quitter")
        self.layout.addWidget(self.boutton_quitter)

        # Centralise les boutons
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

    # Méthode effaçant le reste des boutons et qui présente de nouveaux boutons
    def clear_layout(self):
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    # --------------------------------- Méthodes Etape-1 ---------------------------------

    # Afficher le fichier nutrition.csv dans une nouvelle fenetre.
    def show_data(self):
        self.df_viewer(self.df, "Afficher les aliments")  # self.df = pd.read_csv(fichier_csv, sep=";")

    # Afficher le fichier au viewer
    def df_viewer(self, df_show, title):
        viewer = Dataviewer(df_show, title)  # Creer une instance pour le fichier csv
        viewer.exec()


# --------------------------------- Méthodes Etape-2 ---------------------------------

    def choisir_valeur_nutri(self):

        self.clear_layout()

        self.proteines_button = QPushButton("Protéines")
        self.layout.addWidget(self.proteines_button)
        self.proteines_button.clicked.connect(DataViewer_Etape_2(#Argument for specific button
             ))

        self.gras_button = QPushButton("Gras")
        self.layout.addWidget(self.gras_button)
        self.gras_button.clicked.connect(DataViewer_Etape_2())

        self.cholesterol_button = QPushButton("Cholésterol")
        self.layout.addWidget(self.cholesterol_button)
        self.cholesterol_button.clicked.connect(DataViewer_Etape_2())

        self.sodium_button = QPushButton("Sodium")
        self.layout.addWidget(self.sodium_button)
        self.sodium_button.clicked.connect(DataViewer_Etape_2)

        self.back_button = QPushButton("Retour")
        self.layout.addWidget(self.back_button)
        self.back_button.clicked.connect(MainWindow)  # THIS BUTTON STILL DOESN'T WORK

    def afficher_valeur_nutri(self):
        self.df_viewer(self.df, "Valeur Nutritive")  # self.df = pd.read_csv(fichier_csv, sep=";")

    # Afficher le fichier au viewer
    def df_viewer(self, df_show, title):
        viewer = DataViewer_Etape_2(df_show, title)  # Creer une instance pour le fichier csv
        viewer.exec()


# Classe pour afficher le contenu d'un fichier dans une fenetre de dialogue #
class Dataviewer(QDialog):
    def __init__(self, df_show, title):
        super().__init__()
        self.setWindowTitle(title)

        # Organise la fenetre de dialogue
        layout = QVBoxLayout()

        # Creer un tableau pour les donnees
        self.table = QTableWidget()

        # Definis le nombre de ligne et de colonne en fonction du fichier
        self.table.setRowCount(df_show.shape[0])
        self.table.setColumnCount(df_show.shape[1])

        # Definis les titres des colonnes du tableau en fonction du fichier
        self.table.setHorizontalHeaderLabels(df_show.columns)

        # Boucle pour ajouter les donnees du fichier
        for i in range(df_show.shape[0]):  # Chaque ligne du fichier
            for j in range(df_show.shape[1]):  # Chaque colonne du fichier
                self.table.setItem(i, j, QTableWidgetItem(str(df_show.iat[i, j])))  # Creation d'un item dans le tableau selon l'emplacement de [i, j]    # .iat --> Accede/modifie un element dans un fichier en utilisant les indices [i, j]

        # Ajout du tableau a la fenetre
        layout.addWidget(self.table)
        # Organise la fenetre
        self.setLayout(layout)

class DataViewer_Etape_2(QDialog, type_button=None):
    def __init__(self, df_show, title):
        super().__init__()
        self.setWindowTitle(title) # Need title

        # Creer un tableau pour les donnees
        self.table = QTableWidget()

        # Definis le nombre de ligne et de colonne en fonction du fichier
        self.table.setRowCount(4)

        # Definis les titres des colonnes du tableau en fonction du fichier
        columns = df_show.iloc[:,[0, 1, 2, 3]]
        self.table.setHorizontalHeaderLabels()












# Creer une instance de QApplication
app = QApplication(sys.argv)
# Creer une instance de MainWindow
window = MainWindow()
window.show()
# Execute la boucle de l'application
sys.exit(app.exec())
