import io
import japanize_matplotlib
import re
import math
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.backends.backend_pdf import PdfPages
from PyPDF2 import PdfReader
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from matplotlib.widgets import RadioButtons

    
class PdfManager():
  japanize_matplotlib.japanize()
  usePageLimit = True
  pageLimit = 95
  currentWord = ""
  DoingKanji = False
  DoingHiragana = False
  DoingEnglish = False
  kanji = []
  hiragana = []
  english = []
  
  def convertToExcelFile(app):
    def WordhasKanji(word):
      for c in word:
        if re.search(u"[\u4e00-\u9fff]", c):
          return True
      return False
    
    def WordhasRomaji(word):
      for c in word:
        if re.search(u"[\u0000-\u007F]", c):
          return True
      return False

    def WordhasHiragana(word):
      for c in word:
        if re.search(u"[\u3040-\u309F]", c):
          return True
      return False

    def WordhasKatakana(word):
      for c in word:
        if re.search(u"[\u30A0-\u30FF]", c):
          return True
      return False
  
    def WordIsInBlackList(word):
        blackList = ["JLPTResources–http://www.tanos.co.uk/jlpt/1JLPTN3VocabListThisisnotacumulativelist.(Itdoesn'tcontainthevocabneededbyJLPTN4andbelow).KanjiHiraganaEnglish",
              "JLPT Resources–http://www.tanos.co.uk/jlpt/"]
        for item in blackList:
          if word.replace(" ", "") == item.replace(" ", "") or item.replace(" ", "") in word.replace(" ", ""):
            return True
        return False
      
    def AddWord(word, kanjiHiraganaEnglish):      
      if WordIsInBlackList(PdfManager.currentWord):
        if len(PdfManager.english) > 0:
          PdfManager.english.append(PdfManager.currentWord.split(" ")[0])
        PdfManager.currentWord = ""
      if PdfManager.DoingKanji and len(PdfManager.currentWord) > 0:
        PdfManager.kanji.append(PdfManager.currentWord)
      elif PdfManager.DoingHiragana and len(PdfManager.currentWord) > 0:
        PdfManager.hiragana.append(PdfManager.currentWord)
        if kanjiHiraganaEnglish == 1 and PdfManager.currentWord:
          PdfManager.english.append("*")
      elif PdfManager.DoingEnglish and len(PdfManager.currentWord) > 0:
        PdfManager.english.append(PdfManager.currentWord)
        if kanjiHiraganaEnglish == 2:
          PdfManager.kanji.append("*")
      PdfManager.DoingKanji = kanjiHiraganaEnglish == 1
      PdfManager.DoingHiragana = kanjiHiraganaEnglish == 2
      PdfManager.DoingEnglish = kanjiHiraganaEnglish == 3
      PdfManager.currentWord = word
      
    def Load(app, fileName):
      reader = PdfReader(fileName)
      progress = 0
      PdfManager.kanji.append("*")
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
              PdfManager.currentWord = PdfManager.currentWord + " " + word
            else:
              AddWord(word, 1)
          elif (WordhasHiragana(word) or WordhasKatakana(word)) and not WordhasRomaji(word):
            if PdfManager.DoingHiragana:
              PdfManager.currentWord = PdfManager.currentWord + " " + word
            else:
              AddWord(word, 2)
          else:
            if PdfManager.DoingEnglish:
              PdfManager.currentWord = PdfManager.currentWord + " " + word
            else:
              AddWord(word, 3)
      return [PdfManager.kanji,PdfManager.hiragana,PdfManager.english]
    
    def getPdf(app):
      fname = QFileDialog.getOpenFileName(app, "Open file", 
          "WordListMaker",
          "Pdf files (*.pdf)")
      if fname[0] == "":
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
            newList[i].append("*")
        if len(originalList[1]) > i:
            newList[i].append(originalList[1][i])
        else:
            newList[i].append("*")  
        if len(originalList[2]) > i:
            newList[i].append(originalList[2][i])
        else:
            newList[i].append("*")
    df = pd.DataFrame(newList)
    df.to_excel("output.xlsx", sheet_name="output")
    app.updateFileStatus(2)
  
  def convertToPdf(app):
    def Copy(pdf, content, size):
      fig, ax = plt.subplots()
      fig.patch.set_visible(False)
      ax.axis("off")
      ax.axis("tight")
      data = {"":"O",
          "Kanji":content[0],
          "Hiragana":content[1],
          "English":content[2]}
      df = pd.DataFrame(data)
      table = 0
      table = ax.table(cellText=df.values, colLabels=df.columns, loc="center", cellLoc="left")
      table.auto_set_font_size(False)
      table.auto_set_column_width(False)
      table.set_fontsize(12)
      fig.set_size_inches(8.5, 11)
      table.scale(1.2,1.3)
      fig.subplots_adjust(left=0.1)
      
      for y in range(4):
          table.get_celld()[(0, y)].set_facecolor("lightgrey")
          table.get_celld()[(0, y)].set_fontsize(20)
          
      for y in range(size):
          for x in range(4):
              table.get_celld()[(20 - y,x)].set_alpha(0)
              table.get_celld()[(20 - y,x)].get_text().set_color("white")
              
      for y in range(21):
        table.get_celld()[(y, 0)].set_width(0.07)
        table.get_celld()[(y, 0)].get_text().set_color("white")
        table.get_celld()[(y, 0)].set_fontsize(35)
        table.get_celld()[(y, 3)].set_width(0.43)
        
      
      pdf.savefig()
      plt.close()
    
    def DivideList():
      originalList = app.getExcel()
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
                      newList[page][y].append("*")
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
    pageCount = newList
    with PdfPages("output.pdf") as pdf:
      for page in range(len(pageCount)-2):
          if page == len(pageCount)-3:
              Copy(pdf,newList[page],20 - newList[len(pageCount)-1])
          else:
            Copy(pdf,newList[page],0)
          app.updateProgressBar(int(page / (len(pageCount)-2) * 50) + 50)
    app.updateFileStatus(2)
  