import requests
import pandas

from ExcelManager import *
from PdfManager import *
from SaveDataManager import *

class SentenceGenerator:
    def generateSentences(app):
        excelFile = pd.read_excel(SaveDataManager.read('FileName') + '-Sentences-Output.xlsx', sheet_name='output')
        PdfManager.convertToPdf(app, excelFile, False, "-Sentences-Output", 1)
        return
        API_NAME = "DeepSeek" # OpenAI
        firstFile = app.getExcel()
        excelFile = []

        if API_NAME == "OpenAI":
            with open("WordListMaker/Testing/API_KEY/openai_key.txt", "r") as file:
                API_KEY = file.read()
            API_URL = 'https://api.openai.com/v1/chat/completions'
            headers = {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
            }   

        elif API_NAME == "DeepSeek":
            with open("WordListMaker/Testing/API_KEY/deepseek_key.txt", "r") as file:
                API_KEY = file.read()
            API_URL = 'https://openrouter.ai/api/v1/chat/completions'

            headers = {'Content-Type': 'application/json'
            ,'Authorization': f'Bearer {API_KEY}'
            }

        def generateSentence(wordlist):
            wordstring =""
            for word in wordlist:
                wordstring += "NaN" if pandas.isna(word) else word
                wordstring += "\n" if len(wordstring.splitlines()) != len(wordlist) else ""
            message = """make 1 sentence in japanese for each word in the following list of 20 words. Do not make multiple sentences for one word from the list and 
                                do not put multiple words from the list in one sentence. Only output the sentences.
                                if the word is NaN output NaN instead of a sentence. This will result the output to have exactly 20 lines, even if one of the words from the list is NaN.
                                Here is an example of what complete output can look like:
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
                                This is the list: """ + wordstring

            if API_NAME == "OpenAI":
                data = {
                    'model': 'gpt-3.5-turbo','messages': message
                    }
            elif API_NAME == "DeepSeek":
                data = {
                    "model": "openrouter/optimus-alpha", #"deepseek/deepseek-chat:free",
                    "messages": [{"role": "user", "content": message}]
                    }

            # Send the POST request to the DeepSeek API
            response = requests.post(API_URL, json=data, headers=headers)

            # Check if the request was successful
            if response.status_code == 200:
                #print(response.json())
                if "Rate limit exceeded" in response.text:
                    print("ERROR: -------------------------------Rate limit exceeded-------------------------------")
                    return ""
                return  response.json()['choices'][0]['message']['content']
            else:
                print("Failed to fetch data from API. Status Code:", response.status_code)
                print(response.json()['error']['message'])
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
        #newList.append(excelFile[0])
        newList.append(excelFile[1])
        longestList = len(newList[1])
        #newList.append(excelFile[2])
        #longestList = len(newList[1])
        #if len(newList[2]) > longestList:
           #longestList = len(newList[2])
        #if len(newList[3]) > longestList:
           #longestList = len(newList[3])

        outputList = [[]]
        index = 0
        wordGroupBuffer = []
        lastId = 0
        output = ""
        bufferSize = 20

        for i in range(longestList):
            outputList.append([])
            if i == lastId:
                lastId += bufferSize
                output = generateSentence(newList[1][lastId-bufferSize:lastId])
                wordGroupBuffer = output.split('\n')
            if len(wordGroupBuffer) == 0:
                app.updateFileStatus(2)
                return
            if longestList >= (lastId + bufferSize) and len(wordGroupBuffer) != bufferSize:
                print(f"len == :{len(wordGroupBuffer)} {longestList} < {lastId + bufferSize}")
                print(wordGroupBuffer)
                app.updateFileStatus(2)
                return
            part_to_remove = "API Response: "
            wordGroupBuffer[i - (lastId -bufferSize)].replace(part_to_remove, "")
            outputList[index].append(wordGroupBuffer[i - (lastId -bufferSize)])
            #outputList[index].append("")
            #outputList[index].append("")
            index += 1
            app.updateProgressBar(int(i / longestList * 100))
        df = pandas.DataFrame(outputList)
        try:
            df.to_excel(SaveDataManager.read('FileName') + '-Sentences-Output.xlsx', sheet_name='output')
        except PermissionError as e:
            print(e)
            app.updateFileStatus(2)
            return
        app.updateFileStatus(2)
        excelFile = pd.read_excel(SaveDataManager.read('FileName') + '-Sentences-Output.xlsx', sheet_name='output')
        PdfManager.convertToPdf(app, excelFile, False, "-Sentences-Output")
        print('Done')


        