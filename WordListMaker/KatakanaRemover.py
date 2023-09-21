import pandas
import re

class KatakanaRemover():
  def removeKatakana(app):
    def WordhasKatakana(word):
      for c in str(word):
        if re.search(u"[\u30A0-\u30FF]", c):
          return True
      return False
    
    list = [[]]
    list = app.getExcel()
    app.updateFileStatus(1)
    newList = [[]]
    newList.append(list[0])
    newList.append(list[1])
    newList.append(list[2])
    longestList = len(newList[1])
    if len(newList[2]) > longestList:
        longestList = len(newList[2])
    if len(newList[3]) > longestList:
        longestList = len(newList[3])
        
    outputList = [[]]
    index = 0
    for i in range(longestList):
      outputList.append([])
      if not WordhasKatakana(newList[2][i]):
        if len(newList[1]) > i:
            outputList[index].append(newList[1][i])
        else:
            outputList[index].append("*")
      if not WordhasKatakana(newList[2][i]):
        if len(newList[2]) > i:
            outputList[index].append(newList[2][i])
        else:
            outputList[index].append("*")  
      if not WordhasKatakana(newList[2][i]):
        if len(newList[3]) > i:
            outputList[index].append(newList[3][i])
        else:
            outputList[index].append("*")
      if WordhasKatakana(newList[2][i]):
        pass
      else:
        index+=1
      app.updateProgressBar(int(i / longestList * 100))
    
    df = pandas.DataFrame(outputList)
    df.to_excel("WordListMaker//output.xlsx", sheet_name="output")
    app.updateFileStatus(2)
    
    