import pandas
import random
from SaveDataManager import *

class ExcelManager():
  def shuffleList(app, list):
    if len(list) == 0:
        list = app.getExcel()
    if len(list) == 0:
        return
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
    for i in range(longestList):
      outputList.append([])
      if len(newList[1]) > i:
          outputList[i].append(newList[1][i])
      else:
          outputList[i].append('*')
      if len(newList[2]) > i:
          outputList[i].append(newList[2][i])
      else:
          outputList[i].append('*')  
      if len(newList[3]) > i:
          outputList[i].append(newList[3][i])
      else:
          outputList[i].append('*')
      app.updateProgressBar(int(i / longestList * 100))
      
    random.shuffle(outputList)
    df = pandas.DataFrame(outputList)
    try:
        df.to_excel(SaveDataManager.read('FileName') + '-Output.xlsx', sheet_name='output')
    except PermissionError as e:
        print(e)
        app.updateFileStatus(2)
        return
    app.updateFileStatus(2)