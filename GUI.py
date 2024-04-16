import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QTableWidget, QTableWidgetItem, QTextEdit, QPushButton, QLabel
from PyQt5.QtGui import QColor
import Ochroniarz

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ochroniarz")
        self.setGeometry(100, 100, 800, 600)
        self.setFixedSize(900, 600)


        self.label1 = QLabel("Wpisz tekst", self)
        self.label1.move(20, 0)
        self.text_widget = QTextEdit(self)
        self.text_widget.setGeometry(20, 20, 500, 100)
        self.label1.adjustSize()

        self.label2 = QLabel("Tekst", self)
        self.label2.move(20, 120)
        self.text_widget2 = QTextEdit(self)
        self.text_widget2.setGeometry(20, 140, 500, 100)
        self.label2.adjustSize()


        self.label3 = QLabel("Dane wrażliwe", self)
        self.label3.move(550, 0)
        self.table = QTableWidget(self)
        self.table.setGeometry(550, 20, 300, 300)
        self.label3.adjustSize()

        self.button1 = QPushButton("Sprawdź", self)
        self.button1.move(250, 350)
        self.button1.clicked.connect(self.process_text)
        self.button1.setStyleSheet("QPushButton:pressed { background-color: red; }")

        self.button2 = QPushButton("Konwersja", self)
        self.button2.move(350, 350)
        self.button2.clicked.connect(self.conversion)
        self.button2.setStyleSheet("QPushButton:pressed { background-color: green; }")


    def get_text(self):
        text = self.text_widget.toPlainText()
        if len(text.strip()) < 2:
            print("wprowadź tekst")
            return None
        return text

    def process_text(self):
        text = self.get_text()
        if text is None:
            return None

        zmiana_danych, wiadomosc, przetworzony_tekst  = Ochroniarz.ochrona(text)
        print(zmiana_danych)
        self.wiadomosc = wiadomosc
        self.przetworzony_tekst = przetworzony_tekst

        self.text_widget2.setText(przetworzony_tekst)
        self.load_data_to_table(zmiana_danych)
        self.wyswietla_wiadomosc = False

    def conversion(self):
        try:
            try:
                if self.wyswietla_wiadomosc is True:
                    self.text_widget2.setText(self.przetworzony_tekst)
                    self.wyswietla_wiadomosc = False
                else:
                    self.text_widget2.setText(self.wiadomosc)
                    self.wyswietla_wiadomosc = True
            except:
                pass
        except:
            print("najpierw sprawdź tekst")

    def load_data_to_table(self, data):
        self.table.setRowCount(len(data))
        self.table.setColumnCount(2)

        for row, row_data in enumerate(data):
            for col, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.table.setItem(row, col, item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
