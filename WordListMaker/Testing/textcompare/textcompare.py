import re

def findMarkedWords():
    count = 0
    print('start')
    with open('Testing/textcompare/JLPT-N2-Edited.txt','rb') as file:
        for word in file:
            if '/Type/Annot/V/Yes' in str(word):
                string = str(word)
                start = string.find('checkbox')
                checkBoxNumber = int(re.findall(r'\d+', string[start + 8:start+10])[0]) + 1
                pageNumber = int(re.findall(r'\d+', string[start + 12:start+14])[0])
                wordNumber = (pageNumber * 21 if pageNumber > 0 else 1) + checkBoxNumber
                print(wordNumber)

findMarkedWords()