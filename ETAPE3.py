
########ETAPE-3#############
import sys
import csv    # pour lire et ecrire des fichiers cvs
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QTableWidget, QLineEdit, QPushButton,QGridLayout, QVBoxLayout, QTableWidgetItem
def afficher():
  print(edit_etape3.text())


App = QApplication([])    # Creation de l'objet App de la classe QApplication

fen_etape3 = QWidget() # Creation de l'objet fen de la classe QWidget
fen_etape3.setGeometry(100, 100, 700, 300)
fen_etape3.setWindowTitle("Application de Nutrition")

#QGridLayout
grid_etape3 = QGridLayout()
fen_etape3.setLayout(grid_etape3)

# QLineEdit
edit_etape3 = QLineEdit(fen_etape3)
grid_etape3.addWidget(edit_etape3, 0, 0)


#QLabel
qlbl = QLabel(fen_etape3)
qlbl.setText("Veuillez insérer l'ID d'un aliment")
grid_etape3.addWidget(qlbl, 0, 0)


#QPushButton
afficher_etape3 = QPushButton(fen_etape3)
afficher_etape3.setText("Afficher les valeurs nutritives")
afficher_etape3.clicked.connect(afficher)
grid_etape3.addWidget(afficher_etape3, 1, 0)







fen_etape3.show()
App.exec()



