import csv
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QInputDialog, QLabel, QPushButton, QVBoxLayout, \
    QWidget, QTableView, QHeaderView, QAbstractItemView
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt


class NutritionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des Valeurs Nutritionnelles")
        self.setGeometry(100, 100, 1000, 600)  # Taille et position de la fenêtre

        self.headers = []  # Liste pour stocker les en-têtes du fichier CSV
        self.data = []  # Liste pour stocker les données du fichier CSV
        self.file_name = ''  # Variable pour stocker le nom du fichier chargé

        self.init_ui()  # Initialisation de l'interface utilisateur

    def init_ui(self):
        # Création des widgets
        self.label = QLabel("Choisissez une option dans le menu")  # Label pour afficher les messages
        self.button_load = QPushButton("Charger CSV")  # Bouton pour charger le fichier CSV
        self.button_load.clicked.connect(self.load_csv)  # Connexion du bouton à la méthode load_csv

        self.button_modify = QPushButton("Modifier Valeur Nutritive")  # Bouton pour modifier les valeurs nutritives
        self.button_modify.clicked.connect(self.modify_value)  # Connexion du bouton à la méthode modify_value

        self.table_view = QTableView()  # Widget pour afficher les données sous forme de tableau
        self.table_model = QStandardItemModel()  # Modèle pour gérer les données du tableau
        self.table_view.setModel(self.table_model)  # Associer le modèle au widget

        # Permettre l'édition des cellules
        self.table_view.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)

        # Création de la disposition verticale
        layout = QVBoxLayout()
        layout.addWidget(self.label)  # Ajouter le label à la disposition
        layout.addWidget(self.button_load)  # Ajouter le bouton de chargement à la disposition
        layout.addWidget(self.button_modify)  # Ajouter le bouton de modification à la disposition
        layout.addWidget(self.table_view)  # Ajouter le tableau à la disposition

        container = QWidget()  # Créer un widget conteneur
        container.setLayout(layout)  # Définir la disposition du conteneur
        self.setCentralWidget(container)  # Définir le widget central de la fenêtre

    def load_csv(self):
        # Ouvrir une boîte de dialogue pour sélectionner un fichier CSV
        file_name, _ = QFileDialog.getOpenFileName(self, "Ouvrir le fichier CSV", "",
                                                   "CSV Files (*.csv);;All Files (*)")

        if file_name:
            # Lire le fichier CSV
            with open(file_name, mode='r', newline='', encoding='utf-8') as file:
                csv_reader = csv.reader(file, delimiter=';')  # Spécifie le délimiteur utilisé dans le CSV
                self.headers = next(csv_reader)  # Lire les en-têtes
                self.data = [row for row in csv_reader]  # Lire les données

            # Mettre à jour le modèle de la table avec les nouvelles données
            self.table_model.setHorizontalHeaderLabels(self.headers)  # Définir les en-têtes du tableau
            self.table_model.setRowCount(len(self.data))  # Définir le nombre de lignes
            self.table_model.setColumnCount(len(self.headers))  # Définir le nombre de colonnes

            # Remplir le modèle avec les données du fichier CSV
            for row_index, row in enumerate(self.data):
                for col_index, value in enumerate(row):
                    item = QStandardItem(value)  # Créer un item pour chaque valeur
                    self.table_model.setItem(row_index, col_index, item)  # Ajouter l'item au modèle

            self.label.setText("Fichier CSV chargé avec succès.")  # Afficher un message de succès
            self.file_name = file_name  # Enregistrer le nom du fichier chargé

    def modify_value(self):
        # Vérifier si des données ont été chargées
        if not self.data:
            self.label.setText("Aucun fichier CSV chargé.")
            return

        # Demander à l'utilisateur l'ID de l'aliment à modifier
        id_str, ok = QInputDialog.getText(self, 'ID de l\'aliment',
                                          'Veuillez insérer l\'ID du nutriment pour lequel vous voulez faire des modifications :')
        if not ok or not id_str.isdigit():  # Vérifier que l'ID est un nombre entier
            self.label.setText("ID invalide.")
            return

        id_value = int(id_str)  # Convertir l'ID en entier
        # Vérifier si l'ID est valide en le comparant aux IDs présents dans les données
        if not numeroDeIDValide(id_value, [int(row[0]) for row in self.data if row[0].isdigit()]):
            self.label.setText("ID invalide.")
            return

        # Trouver la ligne correspondant à l'ID
        row_index = next((i for i, row in enumerate(self.data) if row[0].isdigit() and int(row[0]) == id_value), None)
        if row_index is None:
            self.label.setText("ID non trouvé dans les données.")
            return

        # Options pour les nutriments
        nutrient_options = {
            1: 'Energ_Kcal',
            2: 'Protéine',
            3: 'gras',
            4: 'Cholestérol',
            5: 'Sodium'
        }
        nutriments_valides = list(nutrient_options.keys())  # Liste des nutriments valides

        # Demander à l'utilisateur quel nutriment il souhaite modifier
        choix_str, ok = QInputDialog.getText(self, 'Choix du nutriment',
                                             'Veuillez saisir le numéro correspondant au nutriment :\n1- Energ_Kcal\n2- Protéine\n3- gras\n4- Cholestérol\n5- Sodium')
        if not ok or not choix_str.isdigit() or not valeurNutritiveValides(int(choix_str), nutriments_valides):
            self.label.setText("Choix de nutriment invalide.")
            return

        nutrient_index = int(choix_str)  # Convertir le choix en entier
        nutrient_name = nutrient_options[nutrient_index]  # Obtenir le nom du nutriment
        cur_value = self.data[row_index][self.headers.index(nutrient_name)]  # Obtenir la valeur actuelle du nutriment

        # Afficher la valeur actuelle et demander si elle doit être modifiée
        modify_value, ok = QInputDialog.getText(self, 'Modifier la valeur',
                                                f'{nutrient_name} est : {cur_value}\nVoulez-vous conserver cette valeur (Oui) ou modifier la valeur (Non) :')
        if not ok:
            self.label.setText("Opération annulée.")
            return

        if modify_value.lower() == 'non':  # Si l'utilisateur souhaite modifier la valeur
            new_value_str, ok = QInputDialog.getText(self, 'Nouvelle valeur', 'Veuillez saisir la nouvelle valeur :')
            if not ok or not new_value_str.isdigit():
                self.label.setText("Valeur invalide.")
                return

            new_value = new_value_str  # Nouvelle valeur saisie par l'utilisateur
            self.data[row_index][self.headers.index(nutrient_name)] = new_value  # Mettre à jour les données
            self.table_model.setItem(row_index, self.headers.index(nutrient_name),
                                     QStandardItem(new_value))  # Mettre à jour le tableau
            self.label.setText(f"Validation de la nouvelle valeur et modification --> OK")

            # Sauvegarder les modifications dans le fichier CSV
            with open(self.file_name, mode='w', newline='', encoding='utf-8') as file:
                csv_writer = csv.writer(file, delimiter=';')  # Spécifie le délimiteur utilisé dans le CSV
                csv_writer.writerow(self.headers)  # Écrire les en-têtes
                csv_writer.writerows(self.data)  # Écrire les données modifiées
        else:
            self.label.setText("Valeur conservée.")  # Si l'utilisateur conserve la valeur


def ChoixMenuValide(choix, options_valides):
    """
    Vérifie si le choix de l'utilisateur est valide.
    :param choix: L'entrée de l'utilisateur (entier ou chaîne de caractères)
    :param options_valides: Liste des options valides
    :return: True si le choix est valide, False sinon
    """
    return choix in options_valides


def numeroDeIDValide(id, liste_ids):
    """
    Vérifie si un ID est valide.
    :param id: L'ID à vérifier
    :param liste_ids: Liste des IDs valides
    :return: True si l'ID est valide, False sinon
    """
    return id in liste_ids


def valeurNutritiveValides(nutriment, nutriments_valides):
    """
    Vérifie si la valeur nutritive est valide.
    :param nutriment: Le numéro correspondant au nutriment à vérifier
    :param nutriments_valides: Liste des nutriments valides
    :return: True si la valeur nutritive est valide, False sinon
    """
    return nutriment in nutriments_valides


if __name__ == "__main__":
    app = QApplication([])
    window = NutritionApp()
    window.show()
    app.exec()
