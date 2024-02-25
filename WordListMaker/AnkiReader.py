import pandas as pd

from JapaneseIdentifier import * 
from PyQt6.QtWidgets import *

class AnkiReader():
    def isInBannedList(part):
        bannedList = ['#separator:tab','#html:true','#tags', 'column:5']
        for word in part.split():
            if word.isnumeric() or word in bannedList:
                return True
        return False

    def setIsFull(newSet):
        return newSet['original'] != None and newSet['Hiragana'] != None and newSet['English'] != None
            
    def convertToExcelFile(app):
        def getAnki(app):
            fileName = QFileDialog.getOpenFileName(app, 'Open file', 
                'WordListMaker',
                'txt files (*.txt)')
            if fileName[0] == '':
                return ''
            app.updateFileStatus(1)
            return fileName[0]
        
        def extractFromText():
            progress = 0
            lineCount = 0
            with open(fileName,'r', encoding='utf-8') as file:
                lines = file.readlines()
                lineCount = len(lines)
                for line in lines:
                    newSet = {'original' : None, 'Hiragana' : None, 'English' : None}
                    progress+=1
                    app.updateProgressBar(int(progress / lineCount * 100))
                    for part in line.split('\t'):
                        if not AnkiReader.isInBannedList(part):
                            if partIsKana(part):
                                if newSet['Hiragana'] != None:
                                    continue
                                newSet['Hiragana'] = getKanaFromLine(part)
                            elif partIsEnglish(part):
                                if newSet['English'] != None:
                                    continue
                                newSet['English'] = part 
                            else:
                                if newSet['original'] != None:
                                    continue
                                newSet['original'] = part
                    if AnkiReader.setIsFull(newSet):
                        list.append((newSet['original'],newSet['Hiragana'],newSet['English']))
                    newSet = {'original' : None, 'Hiragana' : None, 'English' : None}
        
        def convertToExcel():
            df = pd.DataFrame(list)
            df.to_excel('output.xlsx', sheet_name='output')
            app.updateFileStatus(2)

        fileName = getAnki(app)
        if fileName == '':
            return
        list = []
        extractFromText()
        convertToExcel()