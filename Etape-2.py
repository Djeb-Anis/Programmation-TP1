import sys
import pandas as pd
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QMessageBox, \
    QDialog, QTableWidget, QTableWidgetItem, QVBoxLayout

fichier_csv = ("./nutrition.csv")

#

# Fonction effaçant le reste des boutons et qui présente de nouveaux boutons
def clear_layout(window):
    for i in reversed(range(window.layout.count())):
        widget = window.layout.itemAt(i).widget()
        if widget is not None:
            widget.deleteLater()



# Classe principale pour la fenetre #
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Dimension fenetre principale
        self.setWindowTitle("Nutrition")
        self.setGeometry(100, 100, 800, 600)

        # Organise les widget verticalement
        self.layout = QVBoxLayout()

        clear_layout(self)

        # Ajout des boutons dans le menu
        self.Etape_1_button = QPushButton("Afficher les aliments")
        self.layout.addWidget(self.Etape_1_button)

        self.Etape_2_button = QPushButton("Valeur nutritive")
        self.layout.addWidget(self.Etape_2_button)
        self.Etape_2_button.clicked.connect(lambda: self.choisir_valeur_nutri_window())

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


# --------------------------------- Méthodes Etape-2 ---------------------------------

    def choisir_valeur_nutri_window(self):

        # Lecture du fichier csv
        self.df = pd.read_csv(fichier_csv, sep=';')

        clear_layout(self)

        nom_proteines = 'Protéine'
        self.proteines_button = QPushButton("Protéines")
        self.layout.addWidget(self.proteines_button)
        self.proteines_button.clicked.connect(lambda: show_data_viewer(nom_proteines))


        self.gras_button = QPushButton("Gras")
        self.layout.addWidget(self.gras_button)


        self.cholesterol_button = QPushButton("Cholésterol")
        self.layout.addWidget(self.cholesterol_button)


        self.sodium_button = QPushButton("Sodium")
        self.layout.addWidget(self.sodium_button)


        self.back_button = QPushButton("Retour")
        self.layout.addWidget(self.back_button)
        self.back_button.clicked.connect(MainWindow)  # THIS BUTTON STILL DOESN'T WORK

        def show_data_viewer(nom_button):
            viewer = DataViewer_Etape_2(self.df, nom_button)
            viewer.exec()


class DataViewer_Etape_2(QDialog):
    def __init__(self, original_df, nom_button):

        # Générer mon nouveau dataframe en utilisant mon dataframe original
        new_df = original_df[['Id', 'Catégorie', 'Description']].copy()
        new_df.loc[:, nom_button] = original_df[nom_button].values

        # -----------------GUI Part-----------------
        super().__init__()
        self.setWindowTitle(nom_button) # Title will be name of Button


        # Creer un tableau pour les donnees
        self.table = QTableWidget()

        # Définir le nombre de colonnes et rangées
        self.table.setRowCount(new_df.shape[0])
        self.table.setColumnCount(new_df.shape[1])
        self.table.setHorizontalHeaderLabels(new_df.columns)
        # self.table.setVerticalHeaderLabels(new_df.index.astype(str).tolist()) Maybe add this idk yet

        # Boucle pour ajouter les donnees du fichier
        for i in range(new_df.shape[0]):  # Chaque ligne du fichier
            for j in range(new_df.shape[1]):  # Chaque colonne du fichier
                self.table.setItem(i, j, QTableWidgetItem(str(new_df.iat[i, j])))  # Creation d'un item dans le tableau selon l'emplacement de [i, j]    # .iat --> Accede/modifie un element dans un fichier en utilisant les indices [i, j]

        # Créer mon layout
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)









# Creer une instance de QApplication
app = QApplication(sys.argv)
# Creer une instance de MainWindow
window = MainWindow()
window.show()
# Execute la boucle de l'application
sys.exit(app.exec())
