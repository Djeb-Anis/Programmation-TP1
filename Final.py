import sys
import os
import pandas as pd
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QDialog, QTableWidget, \
    QTableWidgetItem, QVBoxLayout, QMessageBox, QLineEdit, QComboBox, QFormLayout, QLabel, QTableView
from PyQt6.QtGui import QIntValidator, QValidator
from PyQt6.QtCore import Qt, QAbstractTableModel

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

# Classe principale pour la fenêtre
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Création d'une liste pour garder les variables contenant les autres fenêtres vivantes
        self.other_windows = []

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

    # Méthodes associées à la classe MainWindow

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
        self.Etape_3_button.clicked.connect(lambda: self.open_rechrcher_par_Id())

        self.Etape_4_button = QPushButton("Modifier")
        self.layout.addWidget(self.Etape_4_button)

        self.Etape_5_button = QPushButton("Ajouter")
        self.layout.addWidget(self.Etape_5_button)
        self.Etape_5_button.clicked.connect(lambda: self.open_ajouter_element_window())

        self.boutton_quitter = QPushButton("Quitter")
        self.boutton_quitter.clicked.connect(self.fermer_appli)
        self.layout.addWidget(self.boutton_quitter)

    def show_data(self):
        # Lecture du fichier CSV
        self.df = pd.read_csv(fichier_csv, sep=';')
        self.df_viewer(self.df, "Afficher les aliments")

    # Afficher le fichier au viewer
    def df_viewer(self, df_show, title):
        viewer = Dataviewer_Etape_1(df_show, title)  # Créer une instance pour le fichier CSV
        viewer.exec()

    def open_ajouter_element_window(self):
        window_ajout = ajouter_element_window()
        window_ajout.show()
        self.other_windows.append(window_ajout) # Ajout de la fenêtre à la liste initialisée précédement

    def open_rechrcher_par_Id(self):
        window_Id = rechrcher_par_Id()
        window_Id.show()
        self.other_windows.append(window_Id) # Ajout de la fenêtre à la liste initialisée précédement

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


#-------------------------- ÉTAPE 1 --------------------------

class Dataviewer_Etape_1(QDialog):
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


#-------------------------- ÉTAPE 2 --------------------------

class DataViewer_Etape_2(QDialog):
    def __init__(self, original_df, nom_button):
        super().__init__()
        self.setWindowTitle(nom_button)

        # Générer un nouveau DataFrame en utilisant le DataFrame original
        new_df = original_df[['Id', 'Catégorie', 'Description']].copy()
        # Copier la colonne d'intéret vers le nouveau data frame
        new_df[nom_button] = original_df[nom_button]
        # Exporter le nouveau data frame dans un fichier csv avec le nom requis
        new_df.to_csv(f'{nom_button}.csv', index_label=False, sep=';')


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


#-------------------------- ÉTAPE 3 --------------------------

# Modèle personnalisé permettant d'afficher le data frame intégré dans la fenêtre
class PandasModel(QAbstractTableModel):
    def __init__(self, dataframe):
        super().__init__()
        self._dataframe = dataframe

    def rowCount(self, parent=None):
        return self._dataframe.shape[0]

    def columnCount(self, parent=None):
        return self._dataframe.shape[1]

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid() and role == Qt.ItemDataRole.DisplayRole:
            return str(self._dataframe.iat[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._dataframe.columns[section]
            else:
                return self._dataframe.index[section]
        return None

class rechrcher_par_Id(QDialog):

    def __init__(self):
        super().__init__()

        # Création du data frame
        self.df = pd.read_csv(fichier_csv, sep=';')  # Replace with your actual CSV file path

        # Caractéristiques de la fenêtre
        self.setWindowTitle('Recherche par Id')
        self.setModal(True)  # Set the dialog to be modal

        # Ajout Input Field pour la recherche de l'Id
        self.Input_Id = QLineEdit()
        self.Input_Id.setPlaceholderText("Entrez l'Id ici")
        self.Input_Id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Ajout bouton recherche
        self.Recherche_boutton = QPushButton('Rechercher')
        self.Recherche_boutton.clicked.connect(lambda: self.recherche_Id(self.Input_Id.text()))

        # Ajout d'un field permettant d'afficher le résultat de la recherche
        self.Recherche_result = QLabel()
        self.Recherche_result.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Ajout bouton back
        self.back_button = QPushButton('Retour')
        self.back_button.clicked.connect(self.retour)

        # Créer un QTableView pour afficher le DataFrame
        self.table_view = QTableView()
        self.update_table_view(self.df)

        # Création de mon layout et ajout des éléments au layout
        layout = QVBoxLayout()
        layout.addWidget(self.table_view)
        layout.addWidget(self.Input_Id)
        layout.addWidget(self.Recherche_result)
        layout.addWidget(self.Recherche_boutton)
        layout.addWidget(self.back_button)

        # Créer un widget central
        central_widget = QWidget()
        central_widget.setLayout(layout)

        # Définir le widget central de la fenêtre principale
        self.setLayout(layout)

    def update_table_view(self, dataframe):
        model = PandasModel(dataframe)
        self.table_view.setModel(model)

    def recherche_Id(self, Id):
        Id_str = str(Id)

        # Check if the Id exists in the DataFrame
        if (self.df['Id'].astype(str) == Id_str).any():
            result = self.df[self.df['Id'].astype(str) == Id_str]
            # Imprimer le résultat
            result_txt = ';'.join(result.iloc[0].astype(str).values)
            self.Recherche_result.setText(result_txt)
        else:
            message_erreur = "Id non trouvé"
            self.Recherche_result.setText(message_erreur)

    def retour(self):
        self.close()




#-------------------------- ÉTAPE 4 --------------------------

#-------------------------- ÉTAPE 5 --------------------------

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









# Créer une instance de QApplication
app = QApplication(sys.argv)
# Créer une instance de MainWindow
main_window = MainWindow()
main_window.show()
# Exécuter la boucle de l'application
sys.exit(app.exec())
