import sys
import os
import pandas as pd
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QFileDialog, QMessageBox, \
    QDialog, QTableWidget, QTableWidgetItem, QVBoxLayout, QLabel, QLineEdit, QComboBox, QFormLayout
from PyQt6.QtGui import QIntValidator, QValidator
from PyQt6.QtCore import Qt


# Définission du fichier csv (vérifier si nous n'en avons pas généré un au préalable)
directory = './'
new_file_csv = 'Nouveau_Fichier.csv'
new_file_csv_path = os.path.join(directory, new_file_csv)

if os.path.exists(new_file_csv_path):
    fichier_csv = new_file_csv_path
else:
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
        if self.Categorie_combo_box.currentText() == "Autre":
            self.Categorie_custom_input.setVisible(True)
            self.Categorie_custom_input.setFocus()  # Set focus to the line edit
        else:
            self.Categorie_custom_input.setVisible(False)
            #self.instructions.setText(f"Selected: {self.Categorie_combo_box.currentText()}")


    # Fonction permettant l'ajout d'une option Autre
    def add_custom_option(self):
        # Get the custom input text
        custom_text = self.Categorie_custom_input.text().strip()
        if custom_text and custom_text not in self.Categorie_combo_box.itemTexts():
            # Add the custom option to the combo box
            self.Categorie_combo_box.addItem(custom_text)
            self.Categorie_combo_box.setCurrentText(custom_text)  # Set the combo box to the new option
            self.label.setText(f"Selected: {custom_text}")
            self.Categorie_custom_input.clear()  # Clear the input field


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

    # Méthode préparant les données rentrées par l'utilisateur à être utilisées dans le fichiers csv
    def prep_data(self, original_df):
        # Create a list composed of the input from each category
        element_list = [
            self.Categorie_combo_box, self.Categorie_custom_input, self.Descr_input, self.Energie_input,
            self.Prot_input, self.Gras_input, self.Chol_input, self.Sodium_input
        ]

        # Second empty list to hold text inputs
        text_element_list = []

        # Check which category input is used
        if self.Categorie_combo_box.currentText() == "Autre" and self.Categorie_custom_input.text():
            # If "Autre" is selected, use the custom input
            input = self.Categorie_custom_input.text()
        else:
            # Otherwise, use the selected category from the combo box
            input = self.Categorie_combo_box.currentText()

        # Add the selected or custom category to the text_element_list
        text_element_list.append(input)
        print(text_element_list)

        # Iterate over the rest of the elements and check if any are empty
        for element in element_list[2:]:  # Skip the first element since it's already added
            if element.text():
                text_element_list.append(element.text())
            else:
                self.ouvrir_Erreur_input()
                return False

        # Fetch the biggest ID in the original_df and append it to text_element_list with index 0
        ID = str(int(original_df['Id'].max()) + 1)
        text_element_list.insert(0, ID)

        # Add the new food item to the DataFrame from the Excel file
        new_row = pd.DataFrame([text_element_list], columns=original_df.columns)
        new_df = pd.concat([original_df, new_row], ignore_index=True)

        # Call the class to display the DataFrame
        viewer = DataViewer_Etape_5(new_df)
        viewer.exec()
        return True

        # Fetch the biggest ID in the original_df and append it to text_element_list with index 0
        ID = str(int(original_df['Id'].max()) + 1)
        text_element_list.insert(0, ID)

        # Ajout du nouvel aliment au data frame du fichier excel
        new_row = pd.DataFrame([text_element_list], columns=original_df.columns)
        new_df = pd.concat([original_df, new_row], ignore_index=True)

        # Appel de la classe permettant d'afficher le data frame
        viewer = DataViewer_Etape_5(new_df)
        viewer.exec()
        return True


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
    def __init__(self, df):
        super().__init__()
        self.setWindowTitle("Nouveau Fichier") # Title will be name of Button

        # Tri du df par ID
        df['Id'] = pd.to_numeric(df['Id'], errors='coerce')  # This will convert str types to int types and non-convertible values to NaN
        tri_ID_df = df.sort_values(by='Id')

        # Export du nouveau fichier csv
        tri_ID_df.to_csv('Nouveau_Fichier.csv', index_label=False, sep=';')

        # Creer un tableau pour les donnees
        self.table = QTableWidget()

        # Définir le nombre de colonnes et rangées
        self.table.setRowCount(tri_ID_df.shape[0])
        self.table.setColumnCount(tri_ID_df.shape[1])
        self.table.setHorizontalHeaderLabels(tri_ID_df.columns)

        # Boucle pour ajouter les donnees du fichier
        for i in range(tri_ID_df.shape[0]):  # Chaque ligne du fichier
            for j in range(tri_ID_df.shape[1]):  # Chaque colonne du fichier
                self.table.setItem(i, j, QTableWidgetItem(str(tri_ID_df.iat[i, j])))  # Creation d'un item dans le tableau selon l'emplacement de [i, j]    # .iat --> Accede/modifie un element dans un fichier en utilisant les indices [i, j]

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
