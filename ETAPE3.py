
import sys  # Importation du module système pour interagir avec les arguments de ligne de commande
import csv  # Importation du module CSV pour lire et manipuler les fichiers CSV

# Importation des classes nécessaires depuis PyQt6 pour l'interface utilisateur
from PyQt6.QtGui import QStandardItem
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QPushButton,
                             QLineEdit, QLabel, QWidget, QMessageBox, QInputDialog, QFileDialog)

# Définition de la classe principale de l'application, héritant de QMainWindow
class NutritionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nutrition App")  # Définir le titre de la fenêtre
        self.setGeometry(100, 100, 600, 500)  # Définir la position et la taille de la fenêtre

        # Création du widget central et du layout
        self.central_widget = QWidget()  # Créer un widget central
        self.setCentralWidget(self.central_widget)  # Définir ce widget central comme widget principal de la fenêtre

        self.layout = QVBoxLayout()  # Créer un layout vertical pour organiser les widgets de manière verticale
        self.central_widget.setLayout(self.layout)  # Appliquer le layout au widget central

        # Création et ajout d'un label qui affiche un texte d'instruction
        self.label = QLabel("Veuillez choisir une option:")
        self.layout.addWidget(self.label)  # Ajouter le label au layout

        # Création et ajout d'un bouton pour afficher toutes les valeurs nutritives
        self.show_all_button = QPushButton("Afficher toutes les valeurs nutritives")
        self.show_all_button.clicked.connect(self.show_all_nutrition)  # Connecter le clic du bouton à la méthode `show_all_nutrition`
        self.layout.addWidget(self.show_all_button)  # Ajouter le bouton au layout

        # Création et ajout d'un bouton pour rechercher un aliment par ID
        self.search_button = QPushButton("Rechercher un aliment par ID")
        self.search_button.clicked.connect(self.search_nutrition_by_id)  # Connecter le clic du bouton à la méthode `search_nutrition_by_id`
        self.layout.addWidget(self.search_button)  # Ajouter le bouton au layout

        # Création et ajout d'un label pour afficher les résultats de la recherche ou d'autres informations
        self.result_label = QLabel("")
        self.layout.addWidget(self.result_label)  # Ajouter le label au layout

        # Chargement des données depuis un fichier CSV
        self.data = self.load_csv_data("nutrition.csv")

    # Méthode pour charger les données depuis un fichier CSV
    def load_csv_data(self, filename):
        data = []  # Initialiser une liste vide pour stocker les données
        with open(filename, newline='', encoding='utf-8') as csvfile:  # Ouvrir le fichier CSV avec encodage UTF-8
            reader = csv.DictReader(csvfile, delimiter=';')  # Créer un lecteur CSV avec un délimiteur de point-virgule
            for row in reader:  # Boucler sur chaque ligne du CSV
                data.append(row)  # Ajouter chaque ligne au tableau `data`
        return data  # Retourner les données chargées

    # Méthode pour afficher toutes les valeurs nutritives
    def show_all_nutrition(self):
        result = "Id;Catégorie;Description;Energ_Kcal;Protéine;gras;Cholestérol;Sodium\n"  # Préparer les en-têtes de colonnes
        for row in self.data:  # Boucler sur chaque ligne de données
            # Ajouter chaque ligne de données au résultat sous forme de chaîne de caractères
            result += f"{row['Id']};{row['Catégorie']};{row['Description']};{row['Energ_Kcal']};{row['Protéine']};{row['gras']};{row['Cholestérol']};{row['Sodium']}\n"
        self.result_label.setText(result)  # Afficher le résultat dans le label `result_label`

    # Méthode pour charger un fichier CSV via une boîte de dialogue
    def load_csv(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Ouvrir le fichier CSV", "", "CSV Files (*.csv);;All Files (*)")
        # Ouvrir une boîte de dialogue pour sélectionner un fichier CSV

        if file_name:  # Si un fichier est sélectionné
            with open(file_name, mode='r', newline='', encoding='utf-8') as file:  # Ouvrir le fichier CSV
                csv_reader = csv.reader(file, delimiter=';')  # Lire le fichier CSV avec un délimiteur de point-virgule
                self.headers = next(csv_reader)  # Lire les en-têtes de colonne
                self.data = [row for row in csv_reader]  # Lire toutes les lignes de données et les stocker dans `self.data`

            # Remplir le modèle de données avec le contenu du fichier CSV
            for row_index, row in enumerate(self.data):
                for col_index, value in enumerate(row):
                    item = QStandardItem(value)  # Créer un élément de modèle pour chaque valeur
                    self.table_model.setItem(row_index, col_index, item)  # Ajouter l'élément au modèle à la position correcte

            self.label.setText("Fichier CSV chargé avec succès.")  # Afficher un message de succès dans le label
            self.file_name = file_name  # Enregistrer le nom du fichier chargé

    # Méthode pour rechercher un aliment par ID
    def search_nutrition_by_id(self):
        id, ok = QInputDialog.getText(self, "Recherche par ID", "Veuillez insérer l'ID d’un aliment:")  # Demander l'ID via une boîte de dialogue
        if ok:  # Si l'utilisateur valide l'entrée
            found = False  # Initialiser une variable pour suivre si l'ID a été trouvé
            for row in self.data:  # Boucler sur chaque ligne de données
                if row['Id'] == id:  # Comparer l'ID entré avec les ID dans les données
                    result = f"Id;Catégorie;Description;Energ_Kcal;Protéine;gras;Cholestérol;Sodium\n"  # Préparer les en-têtes de colonnes
                    result += f"{row['Id']};{row['Catégorie']};{row['Description']};{row['Energ_Kcal']};{row['Protéine']};{row['gras']};{row['Cholestérol']};{row['Sodium']}\n"  # Ajouter les données correspondantes à l'ID
                    self.result_label.setText(result)  # Afficher le résultat dans le label `result_label`
                    found = True  # Marquer que l'ID a été trouvé
                    break  # Sortir de la boucle une fois l'ID trouvé
            if not found:  # Si l'ID n'a pas été trouvé
                QMessageBox.warning(self, "Erreur", "ID invalide. Veuillez essayer de nouveau.")  # Afficher un message d'erreur

# Point d'entrée principal de l'application
if __name__ == "__main__":
    app = QApplication(sys.argv)  # Créer l'application Qt
    window = NutritionApp()  # Créer une instance de la fenêtre principale
    window.show()  # Afficher la fenêtre principale
    sys.exit(app.exec())  # Exécuter l'application Qt et entrer dans la boucle d'événements
