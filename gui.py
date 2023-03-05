import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QWidget, QLineEdit


class UserInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Simple')
        self.display_button()
        self.show()
        

    def display_widgets(self):
        QLabel("Name", self).move(50, 50)
        name_label = QLabel("Name:", self)

    def display_button(self):
        self.name_label = QLabel(self)
        self.name_label.setText("Name")
        self.name_label.move(50, 50)
        button = QPushButton("Click Me", self)
        button.clicked.connect(self.button_clicked)
    
    def button_clicked(self):
        self.name_label.setText("You clicked the button!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UserInterface()
    sys.exit(app.exec_())
