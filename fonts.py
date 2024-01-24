from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QFontDatabase, QFont

app = QApplication([])

# Get the available font families
font_families = QFontDatabase().families()

# Create a QLabel and set its font to one of the available fonts
label = QLabel("Hello, World!")
if font_families:
    label.setFont(QFont("Poppins Thin", 12))  # Use the first available font family

label.show()

app.exec_()
print(QFontDatabase().families())
