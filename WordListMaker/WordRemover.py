import pandas

class WordRemover():
  def removeWords(app, getWords):
    def wordIsInRemoveList(word):
      return word in wordList
    wordList = getWords().split()
    list = [[]]
    list = app.getExcel()
    if len(list) == 0 or len(wordList) == 0:
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
    index = 0
    for i in range(longestList):
      outputList.append([])
      if not wordIsInRemoveList(newList[2][i]):
        if len(newList[1]) > i:
            outputList[index].append(newList[1][i])
        else:
            outputList[index].append("*")
      if not wordIsInRemoveList(newList[2][i]):
        if len(newList[2]) > i:
            outputList[index].append(newList[2][i])
        else:
            outputList[index].append("*")  
      if not wordIsInRemoveList(newList[2][i]):
        if len(newList[3]) > i:
            outputList[index].append(newList[3][i])
        else:
            outputList[index].append("*")
      if wordIsInRemoveList(newList[2][i]):
        pass
      else:
        index+=1
      app.updateProgressBar(int(i / longestList * 100))
    
    df = pandas.DataFrame(outputList)
    df.to_excel("output.xlsx", sheet_name="output")
    app.updateFileStatus(2)