import japanize_matplotlib
import pandas as pd
import sys

from functools import partial
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from AnkiDeckGenerator import *
from ExcelManager import *
from PdfManager import *
from KatakanaRemover import *
from WordRemover import *


class MainWindow(QMainWindow):
    japanize_matplotlib.japanize()
    kanji = []
    hiragana = []
    english = []

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("WordListMaker")
        self.setMinimumWidth(256)
        layout = QVBoxLayout()

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.progressBar = QProgressBar()
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        layout.addWidget(self.progressBar)
        self.updateFileStatus(0)

        btn = QPushButton("Convert to Excel file")
        btn.clicked.connect(partial(PdfManager.convertToExcelFile, self))
        layout.addWidget(btn)

        btn2 = QPushButton("Convert to Pdf file")
        btn2.clicked.connect(partial(PdfManager.convertToPdf, self))
        layout.addWidget(btn2)
        
        btn3 = QPushButton("Remove katakana words")
        btn3.clicked.connect(partial(KatakanaRemover.removeKatakana, self))
        layout.addWidget(btn3)
        
        btn4 = QPushButton("Shuffle Excel list")
        btn4.clicked.connect(partial(ExcelManager.shuffleList, self))
        layout.addWidget(btn4)
        
        btn5 = QPushButton("Generate Anki deck")
        btn5.clicked.connect(partial(AnkiDeckGenerator.GenerateAnkiDeck, self))
        layout.addWidget(btn5)
        
        input = QTextEdit(self)
        btn6 = QPushButton("Remove words")
        btn6.clicked.connect(partial(WordRemover.removeWords, self, input.toPlainText))
        layout.addWidget(btn6)
        
        input.resize(200, 32)
        layout.addWidget(input)

    def getExcel(self):
        fname = QFileDialog.getOpenFileName(
            self,
            "Open file",
            "WordListMaker",
            "Excel files (*.xlsx)",
        )
        if fname[0] == "":
            return []
        return pd.read_excel(fname[0], sheet_name=0)

    def updateProgressBar(self, value):
        if value < 100:
            self.progressBar.setValue(int(value))
        else:
            self.updateFileStatus(2)

    def updateFileStatus(self, status):
        if status == 0:
            self.progressBar.hide()
        elif status == 1:
            self.progressBar.show()
        elif status == 2:
            self.progressBar.hide()
            self.progressBar.setValue(0)
        self.progressBar.repaint()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()