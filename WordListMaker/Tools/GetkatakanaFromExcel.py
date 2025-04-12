import pandas
import re

fileName = "C:\_Projects\WordListMaker\WordListMaker\Tools\Optimized Kore.xlsx"
list = pandas.read_excel(fileName, sheet_name=0)
lines = []

def WordhasKatakana(word):
      for c in str(word):
        if re.search(u'[\u30A0-\u30FF]', c):
          return True
      return False

words = list["Vocab-expression"]
translations = list["Vocab-meaning"]

for index in range(len(words)):
    word = words[index]
    if WordhasKatakana(word):
        word = word.ljust(500)
        lines.append(word + translations[index] + "\n")
        
f = open("C:\_Projects\WordListMaker\WordListMaker\Tools\/6K-Katakana.txt", "w", encoding="utf-8")
for word in lines:
    f.write(word)
f.close()

print(len(lines))