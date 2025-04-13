import pandas
import re

from ExcelManager import *
from PdfManager import *
from SaveDataManager import *

class WordRemover:
    def removeWords(app, isInverse):#getWords, isInverse):
        wordList = []#getWords().split()
        firstFile = app.getExcelOrPdfTxt()
        PdfTxtFile = []
        excelFile = []
        
        def wordIsInRemoveList(word):
            return word in wordList
        
        def findMarkedWords(PdfTxtFile, excelFile):
            app.updateFileStatus(1)
            wordIDs = []
            for word in PdfTxtFile:
                if '/Type/Annot/V/Yes' in str(word):
                    string = str(word)
                    start = string.find('checkbox')
                    checkBoxNumber = int(re.findall(r'\d+', string[start + 8:start+10])[0])
                    pageNumber = int(re.findall(r'\d+', string[start + 12:start+16])[0])
                    pNumber = (pageNumber * 20 if pageNumber > 0 else 1)
                    cNumber = (checkBoxNumber if pageNumber > 0 else checkBoxNumber -1)
                    wordIDs.append(pNumber + cNumber)
                    print(pNumber)
            id = 0
            for word in excelFile[1]:
                if id in wordIDs:
                    wordList.append(word)
                id += 1
        
        # No file selected
        if len(firstFile) == 0:
            return
        
        if firstFile[1] == 'pdf':
            PdfTxtFile = firstFile[0]
            excelFile = app.getExcel()
            if len(excelFile) == 0:
                return
            findMarkedWords(PdfTxtFile, excelFile)
        elif firstFile[1] == 'xlsx':
            excelFile = firstFile[0]
        
        # No words in inputField or found in pdf/xlsx
        if len(wordList) == 0:
            if firstFile[1] == 'pdf':
                print("The pdf file has not been read correctly or there are no marked words in the file." + "\n" + 
                      "saving the pdf file with changes could fix this.")
            return
        
        app.updateFileStatus(1)
        newList = [[]]
        newList.append(excelFile[0])
        newList.append(excelFile[1])
        newList.append(excelFile[2])
        longestList = len(newList[1])
        if len(newList[2]) > longestList:
            longestList = len(newList[2])
        if len(newList[3]) > longestList:
            longestList = len(newList[3])

        def includeWord(i):
            return (wordIsInRemoveList(newList[2][i]) and isInverse) or (
                not wordIsInRemoveList(newList[2][i]) and not isInverse)
        
        outputList = [[]]
        index = 0
        for i in range(longestList):
            if includeWord(i):
                outputList.append([])
            if includeWord(i):
                if len(newList[1]) > i:
                    outputList[index].append(newList[1][i])
                else:
                    outputList[index].append('*')
            if includeWord(i):
                if len(newList[2]) > i:
                    outputList[index].append(newList[2][i])
                else:
                    outputList[index].append('*')
            if includeWord(i):
                if len(newList[3]) > i:
                    outputList[index].append(newList[3][i])
                else:
                    outputList[index].append('*')
            if includeWord(i):
                index += 1
            app.updateProgressBar(int(i / longestList * 100))
        df = pandas.DataFrame(outputList)
        try:
            df.to_excel(SaveDataManager.read('FileName') + '-Output.xlsx', sheet_name='output')
        except PermissionError as e:
            print(e)
            app.updateFileStatus(2)
            return
        app.updateFileStatus(2)
        print(wordList)
        print('Removed words count: ' + (str(longestList - len(wordList)) if isInverse else str(len(wordList))) + ' in ' + SaveDataManager.read('FileName') + '-Output.xlsx')
        
        if app.shuffleAndNewPdf:
            print("Shuffle")
            excelFile = pd.read_excel(SaveDataManager.read('FileName') + '-Output.xlsx', sheet_name='output')
            ExcelManager.shuffleList(app, excelFile)
            excelFile = pd.read_excel(SaveDataManager.read('FileName') + '-Output.xlsx', sheet_name='output')
            PdfManager.convertToPdf(app, excelFile, True, "-NoKatakanaShuffleRemoved-interactive")
        