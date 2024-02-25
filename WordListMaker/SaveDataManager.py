class SaveDataManager():
    def load():
        data = []
        fileIsEmpty = True
        with open('SaveData.txt','r', encoding='utf-8') as file:
            for line in file:
                fileIsEmpty = False
                data.append(line.split())
        if fileIsEmpty:
            with open('SaveData.txt', 'w') as f:
                f.write('FileName output' + '\n' +
                        'ShuffleAndNewPdf True')
        return data
                
    def getData(dataName):
        data = SaveDataManager.load()
        for dataPoint in data:
            if dataPoint[0] == dataName:
                return dataPoint[1]
            
    def read(dataName):
        return SaveDataManager.getData(dataName)
    
    def save(dataName, newValue):
        data = SaveDataManager.load()
        new = ''
        if callable(newValue):
            new = newValue().split()[0]
        else: 
            new = newValue.split()[0]
        open('SaveData.txt', 'w').close()
        with open('SaveData.txt', 'w') as f:
            for dataPoint in data:
                if dataPoint[0] == dataName and not dataPoint[1] == new:
                    f.write(dataName + ' ' + new + '\n')
                else: 
                    f.write(dataPoint[0] + ' ' + dataPoint[1] + '\n')
        
