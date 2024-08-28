import sys
import pandas as pd
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QMessageBox, \
    QDialog, QTableWidget, QTableWidgetItem, QVBoxLayout, QLabel, QTextEdit
from PyQt6.QtCore import Qt

fichier_csv = ("./nutrition.csv")



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

        # Ajout des boutons dans le menu
        self.Etape_1_button = QPushButton("Afficher les aliments")
        self.layout.addWidget(self.Etape_1_button)

        self.Etape_2_button = QPushButton("Valeur nutritive")
        self.layout.addWidget(self.Etape_2_button)

        self.Etape_3_button = QPushButton("ID")
        self.layout.addWidget(self.Etape_3_button)

        self.Etape_4_button = QPushButton("Modifier")
        self.layout.addWidget(self.Etape_4_button)

        self.Etape_5_button = QPushButton("Ajouter")
        self.layout.addWidget(self.Etape_5_button)
        self.Etape_5_button.clicked.connect(lambda: self.open_ajouter_element_window())

        self.boutton_quitter = QPushButton("Quitter")
        self.layout.addWidget(self.boutton_quitter)

        # Centralise les boutons
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

    def open_ajouter_element_window(self):
        other_window = ajouter_element_window()
        other_window.show()


# --------------------------------- Méthodes Etape-2 ---------------------------------

class ajouter_element_window(QMainWindow):
    def __init__(self):
        super().__init__()

        # Lecture du fichier csv
        self.df = pd.read_csv(fichier_csv, sep=';')

        # clear_layout(self)

        # nom_proteines = 'Protéine'
        # self.proteines_button = QPushButton("Protéines")
        # self.layout.addWidget(self.proteines_button)
        # self.proteines_button.clicked.connect(lambda: show_data_viewer(nom_proteines))


        self.instructions = QLabel('Veuillez insérer un aliment sous cette forme')
        self.example = QLabel('Catégorie;Description;Energ_Kcal;Protéine;gras;Cholestérol;Sodium')

        self.user_input = QTextEdit()
        self.user_input.setPlaceholderText('Nouvel Aliment')

        self.OK_button = QPushButton('Ajouter')
        self.OK_button.clicked.connect(lambda: self.show_data_viewer(self.df, self.user_input))

        self.back_button = QPushButton("Retour")
        self.back_button.clicked.connect(lambda: self.open_main_window())  # THIS BUTTON STILL DOESN'T WORK

        # Créer mon layout
        layout = QVBoxLayout()
        layout.addWidget(self.instructions)
        layout.addWidget(self.example)
        layout.addWidget(self.user_input)
        layout.addWidget(self.OK_button)
        layout.addWidget(self.back_button)

        # Set my layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Set alignement
        self.instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.example.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.user_input.setAlignment(Qt.AlignmentFlag.AlignCenter) This doesn't work properly

    def open_main_window(self):
        self.main_window = MainWindow()  # Create an instance of MainWindow
        self.main_window.show()  # Show the main window
        self.close()  # Close the current window if needed

    def show_data_viewer(self, original_df, user_input):
        viewer = DataViewer_Etape_5(original_df, user_input)
        viewer.exec()


class DataViewer_Etape_5(QDialog):

    # Méthode Validation de l'entrée
    def validation_entree(self, user_input):
        expected_parts = 6
        user_input = str(user_input)
        parts = user_input.split(';')
        if  len(parts) != expected_parts:
            return False, "Ceci n'est pas une entrée valide."
        else:
            return True, "Entrée valide."



        # Insertion de la nouvelle entrée

    # -----------------GUI Part-----------------
    def __init__(self, original_df, user_input):
        super().__init__()
        self.setWindowTitle() # Title will be name of Button


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
