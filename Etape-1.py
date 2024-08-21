import sys
import pandas as pd
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QMessageBox, QDialog, QTableWidget, QTableWidgetItem, QVBoxLayout


fichier_csv = ("./nutrition.csv")



# Afficher l'ensemble des aliments depuis le fichier nutrition.csv

class MainWindow(QMainWindow):
    def __init__(self):
        super(). __init__()
        self.setWindowTitle("Nutrition")
        self.setGeometry(100,100,800,600)

        self.df = pd.read_csv(fichier_csv, sep=";")

        layout = QVBoxLayout()

        self.show_button = QPushButton("voir les aliments")
        self.show_button.clicked.connect(self.show_data)
        layout.addWidget(self.show_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def show_data(self):
        self.df_viewer(self.df, "Afficher les aliments")

    def df_viewer(self, df_show, title):
        viewer = Dataviewer(df_show, title)
        viewer.exec()

class Dataviewer(QDialog):
    def __init__(self, df_show, title):
        super().__init__()
        self.setWindowTitle(title)
        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setRowCount(df_show.shape[0])
        self.table.setColumnCount(df_show.shape[1])
        self.table.setHorizontalHeaderLabels(df_show.columns)

        for i in range(df_show.shape[0]):
            for j in range(df_show.shape[1]):
                self.table.setItem(i, j, QTableWidgetItem(str(df_show.iat[i, j])))

        layout.addWidget(self.table)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
