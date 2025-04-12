import requests
import json

import pandas
import re

from ExcelManager import *
from PdfManager import *
from SaveDataManager import *

class SentenceGenerator:
    def generateSentences(app, words):
        firstFile = app.getExcel()
        excelFile = []
        
        with open("WordListMaker/Testing/API_KEY/deepseek_key.txt", "r") as file:
            API_KEY = file.read()
        API_URL = 'https://openrouter.ai/api/v1/chat/completions'

        # Define the headers for the API request
        headers = {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        }


        def generateSentence(wordlist):
            #print(wordlist)
            wordstring =""
            for word in wordlist:
                wordstring += "NaN" if pandas.isna(word) else word
            # Define the request payload (data)
            data = {
                "model": "deepseek/deepseek-chat:free",
                "messages": [{"role": "user", "content": """make 1 sentence in japanese for each
                            word in the following list of 20 words. Only output the sentences.
                            if the word is NaN output NaN instead of a sentence. Here is an example of what complete output can look like:
                            回数券を購入しました。  
                            発芽が始まりました。
                            庭が荒れています。
                            彼は嘆いている。
                            技術が普及しています。
                            彼女は時間を惜しむ。
                            面積を計算してください。
                            排出量を減らしましょう。
                            有害な物質を取り除く。
                            NaN
                            出荷が完了しました。
                            旧姓を教えてください。
                            直ちに行動しましょう。
                            体積を測りますよね。
                            一流のサービスを受けたい。
                            ～については後で説明します。
                            若干の修正が必要です。
                            今にも雨が降りそうだ。
                            承諾をお願いします。
                            伝統を受け継ぐ。
                            This is the list: """ + wordstring}]
                }

            # Send the POST request to the DeepSeek API
            response = requests.post(API_URL, json=data, headers=headers)

            # Check if the request was successful
            if response.status_code == 200:
                if "Rate limit exceeded" in response.text:
                    print("ERROR: -------------------------------Rate limit exceeded-------------------------------")
                return  response.json()['choices'][0]['message']['content'].split('\n')
            else:
                print("Failed to fetch data from API. Status Code:", response.status_code)
                return ""

        # No file selected
        if len(firstFile) == 0:
            return

        if firstFile[1] == 'xlsx':
            excelFile = firstFile[0]
        else:
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

        outputList = [[]]
        index = 0

        wordGroupBuffer = []
        lastId = 0

        for i in range(longestList):
            outputList.append([])
            if i == lastId:
                lastId += 20
                wordGroupBuffer = generateSentence(newList[1][lastId-20:lastId])
            part_to_remove = "API Response: "
            wordGroupBuffer[i - (lastId -20)].replace(part_to_remove, "")
            #print(wordGroupBuffer[i - (lastId -20)])
            outputList[index].append(wordGroupBuffer[i - (lastId -20)])
            #outputList[index].append(newList[1][i])
            outputList[index].append("")
            outputList[index].append("")
            index += 1
            app.updateProgressBar(int(i / longestList * 100))
        df = pandas.DataFrame(outputList)
        try:
            df.to_excel(SaveDataManager.read('FileName') + '-Sentences Output.xlsx', sheet_name='output')
        except PermissionError as e:
            print(e)
            app.updateFileStatus(2)
            return
        app.updateFileStatus(2)
        print('Done')


        