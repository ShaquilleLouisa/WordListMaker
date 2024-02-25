import japanize_matplotlib
import math
import matplotlib.pyplot as plt
import pandas as pd
import re

from matplotlib.backends.backend_pdf import PdfPages
from PyPDF2 import PdfReader, PdfWriter
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from reportlab.pdfgen import canvas
from reportlab.lib.colors import transparent
    
from SaveDataManager import *

class PdfManager():
    japanize_matplotlib.japanize()
    usePageLimit = True
    pageLimit = 95
    currentWord = ''
    DoingKanji = False
    DoingHiragana = False
    DoingEnglish = False
    kanji = []
    hiragana = []
    english = []
  
    def convertToExcelFile(app):
        def WordhasKanji(word):
            for c in word:
                if re.search(u'[\u4e00-\u9fff]', c):
                    return True
            return False
    
        def WordhasRomaji(word):
            for c in word:
                if re.search(u'[\u0000-\u007F]', c):
                    return True
            return False

        def WordhasHiragana(word):
            for c in word:
                if re.search(u'[\u3040-\u309F]', c):
                    return True
            return False

        def WordhasKatakana(word):
            for c in word:
                if re.search(u'[\u30A0-\u30FF]', c):
                    return True
            return False
    
        def WordIsInBlackList(word):
            blackList = ['JLPTResources–http://www.tanos.co.uk/jlpt/1JLPTN3VocabListThisisnotacumulativelist.(Itdoesn\'tcontainthevocabneededbyJLPTN4andbelow).KanjiHiraganaEnglish',
                'JLPT Resources–http://www.tanos.co.uk/jlpt/']
            for item in blackList:
                if word.replace(' ', '') == item.replace(' ', '') or item.replace(' ', '') in word.replace(' ', ''):
                    return True
            return False
      
        def AddWord(word, kanjiHiraganaEnglish):      
            if WordIsInBlackList(PdfManager.currentWord):
                if len(PdfManager.english) > 0:
                    PdfManager.english.append(PdfManager.currentWord.split(' ')[0])
                    PdfManager.currentWord = ''
            if PdfManager.DoingKanji and len(PdfManager.currentWord) > 0:
                PdfManager.kanji.append(PdfManager.currentWord)
            elif PdfManager.DoingHiragana and len(PdfManager.currentWord) > 0:
                PdfManager.hiragana.append(PdfManager.currentWord)
                if kanjiHiraganaEnglish == 1 and PdfManager.currentWord:
                    PdfManager.english.append('*')
            elif PdfManager.DoingEnglish and len(PdfManager.currentWord) > 0:
                PdfManager.english.append(PdfManager.currentWord)
                if kanjiHiraganaEnglish == 2:
                    PdfManager.kanji.append('*')
            PdfManager.DoingKanji = kanjiHiraganaEnglish == 1
            PdfManager.DoingHiragana = kanjiHiraganaEnglish == 2
            PdfManager.DoingEnglish = kanjiHiraganaEnglish == 3
            PdfManager.currentWord = word
      
        def Load(app, fileName):
            reader = PdfReader(fileName)
            progress = 0
            PdfManager.kanji.append('*')
            for page in reader.pages:
                progress +=1
                if PdfManager.usePageLimit:
                    app.updateProgressBar(int(progress/PdfManager.pageLimit * 100))
                else:
                    app.updateProgressBar(int(progress/len(reader.pages) * 100))
                if PdfManager.usePageLimit and progress == PdfManager.pageLimit:
                    break
                text = page.extract_text()
                for word in text.split():
                    if WordhasKanji(word):
                        if PdfManager.DoingKanji:
                            PdfManager.currentWord = PdfManager.currentWord + ' ' + word
                        else:
                            AddWord(word, 1)
                    elif (WordhasHiragana(word) or WordhasKatakana(word)) and not WordhasRomaji(word):
                        if PdfManager.DoingHiragana:
                            PdfManager.currentWord = PdfManager.currentWord + ' ' + word
                        else:
                            AddWord(word, 2)
                    else:
                        if PdfManager.DoingEnglish:
                            PdfManager.currentWord = PdfManager.currentWord + ' ' + word
                        else:
                            AddWord(word, 3)
            return [PdfManager.kanji,PdfManager.hiragana,PdfManager.english]
    
        def getPdf(app):
            fname = QFileDialog.getOpenFileName(app, 'Open file', 
                'WordListMaker',
                'Pdf files (*.pdf)')
            if fname[0] == '':
                return []
            app.updateFileStatus(1)
            return Load(app, fname[0])
  
        originalList = getPdf(app)
        if len(originalList) == 0:
            return
        longestList = len(originalList[0])
        if len(originalList[1]) > longestList:
            longestList = len(originalList[1])
        if len(originalList[2]) > longestList:
            longestList = len(originalList[2])
        newList = [[]]
        for i in range(longestList):
            newList.append([])
            if len(originalList[0]) > i:
                newList[i].append(originalList[0][i])
            else:
                newList[i].append('*')
            if len(originalList[1]) > i:
                newList[i].append(originalList[1][i])
            else:
                newList[i].append('*')  
            if len(originalList[2]) > i:
                newList[i].append(originalList[2][i])
            else:
                newList[i].append('*')
        df = pd.DataFrame(newList)
        df.to_excel('output.xlsx', sheet_name='output')
        app.updateFileStatus(2)
  
    def convertToPdf(app, excelFile):
        # Function to create an interactive checkbox
        x = 37
        y_interval = 35.75
        y = y_interval * 19 + 17.25
        size = 35
        def create_checkbox(c, x, y, size, field_name):
            c.acroForm.checkbox(
                name=field_name,
                tooltip=field_name,
                x=x,
                y=y,
                checked=False,
                borderWidth=0,
                fillColor=transparent,
                textColor=transparent,
                buttonStyle='circle',
                size=size,
            )
            c.setFillColorRGB(1, 0, 0)
        
        def Copy(pdf, content, size, page, pageCount):
            fig, ax = plt.subplots()
            fig.patch.set_visible(False)
            ax.axis('off')
            ax.axis('tight')
            data = {str(page + 1) + '/' + str(pageCount) : 'O',
                'Kanji':content[0],
                'Hiragana':content[1],
                'English':content[2]}
            df = pd.DataFrame(data)
            #df.insert(loc = 0,column = 'PPA',value = '<input type='checkbox' />')
            table = 0
            table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='left')
            table.auto_set_font_size(False)
            table.auto_set_column_width(False)
            table.set_fontsize(12)
            fig.set_size_inches(8.5, 11)
            table.scale(1.2,1.3)
            fig.subplots_adjust(left=0.1)
            
            for y in range(4):
                table.get_celld()[(0, y)].set_facecolor('lightgrey')
                table.get_celld()[(0, y)].set_fontsize(20)
                
            for y in range(size):
                for x in range(4):
                    table.get_celld()[(20 - y,x)].set_alpha(0)
                    table.get_celld()[(20 - y,x)].get_text().set_color('white')
                    
            for y in range(21):
                table.get_celld()[(y, 0)].set_width(0.07)
                #table.get_celld()[(y, 0)].get_text().set_color('white')
                table.get_celld()[(y, 0)].set_fontsize(11)#35
                table.get_celld()[(y, 3)].set_width(0.43)
                
            pdf.savefig()
            plt.close()
        
        def DivideList():
            if len(excelFile) == 0:
                originalList = app.getExcel()
            else:
                originalList = excelFile
            if len(originalList) == 0:
                return []
            app.updateFileStatus(1)
            newList = [[[]]]
            pageCount = math.ceil(len(originalList[0]) / 20.0)
            lastPageSize = 0
            lastWord = pageCount * 20
            for page in range(pageCount):
                newList.append([])
                for y in range(3):
                    newList[page].append([])
            for page in range(pageCount):
                for y in range(3):
                    for x in range(20):
                        if (page * 20) + x >= len(originalList[y]):
                            newList[page][y].append('*')
                            if lastPageSize == 0:
                                lastPageSize = x
                        else:
                            newList[page][y].append(originalList[y][(page * 20) + x])
                        app.updateProgressBar(int((page * 20 + x) / lastWord * 50))
            newList.append(lastPageSize)
            return newList
        
        newList = DivideList()
        if len(newList) == 0:
            return
        
        x = 37
        y_interval = 35.75
        y = y_interval * 19 + 17.25
        size = 35
        overlay_pdf_path = 'overlay.pdf'
        c = canvas.Canvas(overlay_pdf_path)
        pageCount = len(newList)-2
        with PdfPages('output.pdf') as pdf:
            for page in range(pageCount):
                if page == pageCount-1:
                    Copy(pdf,newList[page],20 - newList[pageCount+1],page,pageCount)
                else:
                    Copy(pdf,newList[page],0,page,pageCount)
                count = newList[pageCount+1] if page == pageCount-1 else 20
                for i in range(count):
                    create_checkbox(
                        c, x, y + i * -y_interval, size, 'checkbox' + str(i) + ' - ' + str(page)
                    )
                c.showPage()
                app.updateProgressBar(int(page / pageCount * 50) + 50)
        c.save()

        existing_pdf_path = 'output.pdf'
        output_pdf_path = SaveDataManager.read('FileName') + '-NoKatakanaShuffleRemoved-interactive.pdf'

        existing_pdf = PdfReader(open(existing_pdf_path, 'rb'))

        # Merge the overlay with the existing PDF
        output = PdfWriter()
        overlay_pdf = PdfReader(overlay_pdf_path)
        output.add_metadata({
            '/Author': 'Shaquille Louisa',
            '/Title': SaveDataManager.read('FileName') + '-NoKatakanaShuffleRemoved-interactive'
        })
        for i in range(len(existing_pdf.pages)):
            page = existing_pdf.pages[i]
            page.merge_page(overlay_pdf.pages[i])
            
            output.add_page(page)

        # Save the final interactive PDF
        with open(output_pdf_path, 'wb') as out_pdf:
            output.write(out_pdf)

        print('Interactive PDF saved to:', SaveDataManager.read('FileName') + '-NoKatakanaShuffleRemoved-interactive.pdf')

        app.updateFileStatus(2)
  