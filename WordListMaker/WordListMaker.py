import japanize_matplotlib
import pandas as pd
import sys

from functools import partial
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from AnkiReader import *
from AnkiDeckGenerator import *
from ExcelManager import *
from KatakanaRemover import *
from PdfManager import *
from SaveDataManager import *
from WordRemover import *
from SentenceGenerator import *

class MainWindow(QMainWindow):
    japanize_matplotlib.japanize()
    shuffleAndNewPdf = True

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle('WordListMaker')
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

        fileNameWidget = QWidget()
        layout.addWidget(fileNameWidget)
        fileNameLayout = QHBoxLayout()
        fileNameWidget.setLayout(fileNameLayout)
        fileNameLabel = QLabel('File name')
        fileNameLayout.addWidget(fileNameLabel)
        fileNameField = QTextEdit(self)
        fileNameField.setMaximumSize(192, 26)
        fileNameField.setText(SaveDataManager.read('FileName'))
        fileNameField.textChanged.connect(
            partial(SaveDataManager.save, 'FileName', fileNameField.toPlainText)
        )
        fileNameLayout.addWidget(fileNameField)

        buttons = []

        buttons.append(QPushButton('Convert AnkiDeck to Excel file'))
        buttons[0].clicked.connect(partial(AnkiReader.convertToExcelFile, self))
        #layout.addWidget(buttons[0])

        buttons.append(QPushButton('Convert Pdf to Excel file'))
        buttons[1].clicked.connect(partial(PdfManager.convertToExcelFile, self))
        #layout.addWidget(buttons[1])

        buttons.append(QPushButton('Convert to Pdf file'))
        buttons[2].clicked.connect(partial(PdfManager.convertToPdf, self, [], True, "-NoKatakanaShuffleRemoved-interactive"))
        #layout.addWidget(buttons[2])

        buttons.append(QPushButton('Remove katakana words'))
        buttons[3].clicked.connect(partial(KatakanaRemover.removeKatakana, self))
        #layout.addWidget(buttons[3])

        buttons.append(QPushButton('Shuffle Excel list'))
        buttons[4].clicked.connect(partial(ExcelManager.shuffleList, self, []))
        #layout.addWidget(buttons[4])

        #buttons.append(QPushButton('Generate Anki deck'))
        #buttons[5].clicked.connect(partial(AnkiDeckGenerator.GenerateAnkiDeck, self))
        #layout.addWidget(buttons[5])

        buttons.append(QPushButton('Generate Sentences'))
        buttons[5].clicked.connect(
            partial(SentenceGenerator.generateSentences, self)#, input.toPlainText)
        )
        layout.addWidget(buttons[5])
        
        input = QTextEdit(self)
        
        buttons.append(QPushButton('Remove Words'))
        buttons[6].clicked.connect(
            partial(WordRemover.removeWords, self, input.toPlainText, False)#, input.toPlainText, False)
        )
        layout.addWidget(buttons[6])

        #buttons.append(QPushButton('Inverse Remove Words '))
        #buttons[7].clicked.connect(
            #partial(WordRemover.removeWords, self, input.toPlainText, True)
        #)
        #layout.addWidget(buttons[7])

        shuffleRadio = QRadioButton('Shufffle list after removing words and make new PDF')
        shuffleRadio.setChecked(True)
        def toggleShuffleAndNewPdf():
            MainWindow.shuffleAndNewPdf = not MainWindow.shuffleAndNewPdf
            SaveDataManager.save('ShuffleAndNewPdf', str(MainWindow.shuffleAndNewPdf))
        shuffleRadio.clicked.connect(toggleShuffleAndNewPdf)
        layout.addWidget(shuffleRadio)
        input = QTextEdit(self)
        #layout.addWidget(input)

    def getExcel(self):
        fname = QFileDialog.getOpenFileName(
            self,
            'Open file',
            'WordListMaker',
            'Excel files (*.xlsx)',
        )
        if fname[0] == '':
            return []
        return pd.read_excel(fname[0], sheet_name=0)

    def getExcelOrPdfTxt(self):
        fname = QFileDialog.getOpenFileName(
            self,
            'Open file',
            'WordListMaker',
            'Pdf files (*.pdf);;Pdf text files (*.txt);;Excel files (*.xlsx)',
        )
        if fname[0] == '':
            return []
        if fname[1] == 'Pdf files (*.pdf)':
            return [open(fname[0],'rb'),'pdf']
        elif fname[1] == 'Excel files (*.xlsx)':
            return [pd.read_excel(fname[0], sheet_name=0), 'xlsx', fname[0]]
        
    def getExcel(self):
        fname = QFileDialog.getOpenFileName(
            self,
            'Open file',
            'WordListMaker',
            'Excel files (*.xlsx)',
        )
        if fname[0] == '':
            return []
        elif fname[1] == 'Excel files (*.xlsx)':
            return [pd.read_excel(fname[0], sheet_name=0), 'xlsx', fname[0]]

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
