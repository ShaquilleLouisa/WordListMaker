import re

def wordHasRomaji(word):
    for c in word:
        if re.search(u"[\u0000-\u007F]", c):
            return True
    return False

def wordHasKanji(word):
    for c in word:
        if re.search(u"[\u4e00-\u9fff]", c):
            return True
        return False

def wordHasKatakana(word):
    for c in word:
        if re.search(u"[\u30A0-\u30FF]", c):
            return True
        return False

def wordHasHiragana(word):
    for c in word:
        if re.search(u"[\u3040-\u309F]", c):
            return True
    return False

def getKanaFromLine(part):
    hiragana = ''
    for word in part:
        for c in word:
            if re.search(u"[\u3040-\u309F]", c) or re.search(u"[\u30A0-\u30FF]", c):
                hiragana += c
    return hiragana

def partIsEnglish(part):
    for word in part.split():
        if wordHasRomaji(word):
            return True
    return False

def partIsKana(part):
    for word in part.split():
        for c in word:
            if c == '[' and (wordHasHiragana(word) or wordHasKatakana(word)):
                return True
    return False