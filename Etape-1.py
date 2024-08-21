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
        self.df = pd.read_csv(fichier_csv,sep=";")  # sep = ";" est un parametre pandas qui determine les separateurs dans le fichier

        # Organise les widget verticalement
        layout = QVBoxLayout()

        # Ajout des boutons dans le menu
        self.show_button = QPushButton("Afficher les aliments")
        self.show_button.clicked.connect(self.show_data)  # Fais le lien entre le bouton "Afficher les element" et le fichier
        layout.addWidget(self.show_button)

        self.show_button1 = QPushButton("Valeur nutritive")
        layout.addWidget(self.show_button1)

        self.show_button2 = QPushButton("ID")
        layout.addWidget(self.show_button2)

        self.show_button3 = QPushButton("Modifier")
        layout.addWidget(self.show_button3)

        self.show_button4 = QPushButton("Ajouter")
        layout.addWidget(self.show_button4)

        self.show_button5 = QPushButton("Quitter")
        layout.addWidget(self.show_button5)

        # Centralise les boutons
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    # Afficher le fichier nutrition.csv dans une nouvelle fenetre.
    def show_data(self):
        self.df_viewer(self.df, "Afficher les aliments")  # self.df = pd.read_csv(fichier_csv, sep=";")

    # Afficher le fichier au viewer
    def df_viewer(self, df_show, title):
        viewer = Dataviewer(df_show, title)  # Creer une instance pour le fichier csv
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


# Creer une instance de QApplication
app = QApplication(sys.argv)
# Creer une instance de MainWindow
window = MainWindow()
window.show()
# Execute la boucle de l'application
sys.exit(app.exec())
