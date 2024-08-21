import sys
import pandas as pd
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QMessageBox, QDialog, QTableWidget, QTableWidgetItem, QVBoxLayout


fichier_csv = ("/Users/Charles/Desktop/nutrition.csv")

########################## Etape 0 : ############################

# Afficher l'ensemble des aliments depuis le fichier nutrition.csv

class MainWindow(QMainWindow):
    def __init__(self):
        super(). __init__()
        self.setWindowTitle("Nutrition")
        self.setGeometry(100,100,800,600)

        self.df = pd.read_csv(fichier_csv, sep=";")

        layout = QVBoxLayout()

        self.show_button = QPushButton("Voir les aliments")
        self.show_button.clicked.connect(self.show_data)
        layout.addWidget(self.show_button)

        self.show_button1 = QPushButton("Valeur nutritive")
        self.show_button1.clicked.connect(self.show_data)
        layout.addWidget(self.show_button1)

        self.show_button2 = QPushButton("ID")
        self.show_button2.clicked.connect(self.show_data)
        layout.addWidget(self.show_button2)

        self.show_button3 = QPushButton("Modifier")
        self.show_button3.clicked.connect(self.show_data)
        layout.addWidget(self.show_button3)

        self.show_button4 = QPushButton("Ajouter")
        self.show_button4.clicked.connect(self.show_data)
        layout.addWidget(self.show_button4)

        self.show_button5 = QPushButton("Quitter")
        self.show_button5.clicked.connect(self.show_data)
        layout.addWidget(self.show_button5)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def show_data(self):
        self.df_viewer(self.df, "Afficher les aliments")

    def df_viewer(self, df_show, title):
        viewer = Client(df_show, title)
        viewer.exec()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
