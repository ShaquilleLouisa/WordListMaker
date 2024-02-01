class SaveDataManager():
    data = []
    def load():
        fileIsEmpty = True
        with open('SaveData.txt','r', encoding="utf-8") as file:
            for line in file:
                fileIsEmpty = False
                SaveDataManager.data.append(line.split())
        if fileIsEmpty:
            with open('SaveData.txt', 'w') as f:
                f.write('FileName output')
                
    def getData(dataName):
        for data in SaveDataManager.data:
            if data[0] == dataName:
                return data[1]
            
    def read(dataName):
        SaveDataManager.load()
        return SaveDataManager.getData(dataName)
    
    def save(dataName, newValue):
        SaveDataManager.load()
        new = newValue().split()[0]
        open('SaveData.txt', 'w').close()
        with open('SaveData.txt', 'w') as f:
            for data in SaveDataManager.data:
                if data[0] == dataName and not data[1] == new:
                    f.write(dataName + ' ' + new)
        
