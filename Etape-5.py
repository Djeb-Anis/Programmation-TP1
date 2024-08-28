import sys
import pandas as pd
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QFileDialog, QMessageBox, \
    QDialog, QTableWidget, QTableWidgetItem, QVBoxLayout, QLabel, QLineEdit, QComboBox, QFormLayout
from PyQt6.QtGui import QIntValidator, QValidator
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


# --------------------------------- Classes et Méthodes Etape-5 ---------------------------------


class ajouter_element_window(QMainWindow):
    def __init__(self):
        super().__init__()

        # Lecture du fichier csv
        self.df = pd.read_csv(fichier_csv, sep=';')

        # Charactéristiques de la fenêtre
        self.setWindowTitle('Veuillez ajouter un aliment')

        # Méthodes validant les données entrées
        self.int_validator = QIntValidator(0, 100000)

        # ----Catégorie----
        self.Categorie_combo_box = QComboBox()
        self.Categorie_combo_box.addItems(["Déjeuner", "Salade", "Sandwich", "Vinaigrette", "Frites", "Autre"])

        self.Categorie_custom_input = QLineEdit()
        self.Categorie_custom_input.setPlaceholderText("Autre")
        self.Categorie_custom_input.setVisible(False)  # Initially hidden

        self.Categorie_combo_box.currentIndexChanged.connect(self.Categorie_on_combobox_changed)
        # ----Catégorie----


        # ----Déscription----
        self.Descr_input = QLineEdit()
        self.Descr_input.setPlaceholderText("Déscription")
        self.Descr_input.setValidator(LatinLetterValidator())
        # ----Déscription----


        # ----Énergie----
        self.Energie_input = QLineEdit()
        self.Energie_input.setPlaceholderText("Kcal")
        self.Energie_input.setValidator(self.int_validator)
        # ----Énergie----


        # ----Protéines----
        self.Prot_input = QLineEdit()
        self.Prot_input.setPlaceholderText("(g)")
        self.Prot_input.setValidator(self.int_validator)
        # ----Protéines----


        # ----Gras----
        self.Gras_input = QLineEdit()
        self.Gras_input.setPlaceholderText("(g)")
        self.Gras_input.setValidator(self.int_validator)
        # ----Gras----


        # ----Cholestérol----
        self.Chol_input = QLineEdit()
        self.Chol_input.setPlaceholderText("(g)")
        self.Chol_input.setValidator(self.int_validator)
        # ----Cholestérol----

        # ----Sodium----
        self.Sodium_input = QLineEdit()
        self.Sodium_input.setPlaceholderText("(g)")
        self.Sodium_input.setValidator(self.int_validator)
        # ----Sodium----



        self.OK_button = QPushButton('Ajouter')
        self.OK_button.clicked.connect(lambda: self.prep_data(self.df))

        self.back_button = QPushButton("Retour")
        self.back_button.clicked.connect(lambda: self.open_main_window())  # THIS BUTTON STILL DOESN'T WORK

        # Créer mon layout
        layout = QFormLayout()

        layout.addRow("Catégorie", self.Categorie_combo_box)
        layout.addRow(self.Categorie_custom_input)

        layout.addRow("Déscription", self.Descr_input)

        layout.addRow("Énergie", self.Energie_input)

        layout.addRow("Protéines", self.Prot_input)

        layout.addRow("Gras", self.Gras_input)

        layout.addRow("Cholestérol", self.Chol_input)

        layout.addRow("Sodium", self.Sodium_input)


        layout.addRow(self.OK_button)
        layout.addRow(self.back_button)

        # Set my layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


    #Fonction permettant l'utilisation du drop down menu
    def Categorie_on_combobox_changed(self, index):
        # Show or hide the custom input based on selection
        if self.Categorie_combo_box.currentText() == "Other":
            self.Categorie_custom_input.setVisible(True)
            self.Categorie_custom_input.setFocus()  # Set focus to the line edit
        else:
            self.Categorie_custom_input.setVisible(False)
            #self.instructions.setText(f"Selected: {self.Categorie_combo_box.currentText()}")


    # This will be used to add any custom option chosen to the current options list
    # def add_custom_option(self):
    #     # Get the custom input text
    #     custom_text = self.Categorie_custom_input.text().strip()
    #     if custom_text and custom_text not in self.Categorie_combo_box.itemTexts():
    #         # Add the custom option to the combo box
    #         self.Categorie_combo_box.addItem(custom_text)
    #         self.Categorie_combo_box.setCurrentText(custom_text)  # Set the combo box to the new option
    #         self.label.setText(f"Selected: {custom_text}")
    #         self.Categorie_custom_input.clear()  # Clear the input field


    # Méthode permettant d'ouvrir le message d'erreur
    def ouvrir_Erreur_input(self):
        dialog = Erreur_input()  # Pass the main window as the parent
        dialog.setWindowModality(Qt.WindowModality.ApplicationModal)  # Optional: Set modality
        dialog.resize(200, 100)  # Resize the dialog to a suitable size

        # Center the dialog relative to the main window
        main_window_rect = self.geometry()
        dialog_rect = dialog.geometry()
        x = main_window_rect.x() + (main_window_rect.width() - dialog_rect.width()) // 2
        y = main_window_rect.y() + (main_window_rect.height() - dialog_rect.height()) // 2
        dialog.move(x, y)

        dialog.exec()  # Show the dialog as modal

    def prep_data(self, original_df):
        # Création Liste composée du input de chaque catégorie
        element_list = [
            self.Categorie_combo_box, self.Categorie_custom_input, self.Descr_input, self.Energie_input,
            self.Prot_input, self.Gras_input, self.Chol_input, self.Sodium_input
            ]

        # Seconde liste vide
        text_element_list = []

        # Check which category input is used and remove the QComboBox object
        if self.Categorie_combo_box and self.Categorie_combo_box.currentText():
            input = self.Categorie_combo_box.currentText()
            self.Categorie_custom_input.setText(input)
            element_list.remove(self.Categorie_combo_box)
        elif self.Categorie_custom_input and self.Categorie_custom_input.text():
            element_list.remove(self.Categorie_combo_box)

        # Iterate over the list and check if any element is empty
        for element in element_list:
            if element.text():
                text_element_list.append(element.text())
            else:
                self.ouvrir_Erreur_input()
                return False

        print(text_element_list)
        print(original_df.head())
        # THERE IS MISMATCH BETWEEN THE NUMBER OF COLUMNS AND THE NUMBER OF ELEMENTS IN THE LIST
        # I NEED TO GET THE BIGGEST ID IN THE DF AND APPEND IT ITS VALUE+1 TO MY LIST, WITH INDEX 0
        # Ajout du nouvel aliment au data frame du fichier excel
        #new_df = original_df.loc[len(original_df)] = text_element_list
        print("OK")
        # Appel de la classe permettant d'afficher le data frame
        # viewer = DataViewer_Etape_5(new_df)
        # viewer.exec()
        # return True


    def open_main_window(self):
        self.main_window = MainWindow()  # Create an instance of MainWindow
        self.main_window.show()  # Show the main window
        self.close()  # Close the current window if needed


# CLasse contenant la fenêtre de dialogue en cas d'érreur
class Erreur_input(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Erreur")
        self.setModal(True)

        self.message_erreur = QLabel("Une ou plusieurs entrées sont vides")

        layout = QVBoxLayout()
        layout.addWidget(self.message_erreur)

        self.setLayout(layout)


# Classe permettant la validation de caractères alphanumériques
class LatinLetterValidator(QValidator):
    def validate(self, input_str, pos):
        # Check if the input string contains only Latin letters
        if all(char.isalpha() for char in input_str):
            return QValidator.State.Acceptable, input_str, pos
        else:
            return QValidator.State.Invalid, input_str, pos

class DataViewer_Etape_5(QDialog):

        # Insertion de la nouvelle entrée

    # -----------------GUI Part-----------------
    def __init__(self, original_df):
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
