from engine.types.wordList import WordList

class Statement(WordList):
    @staticmethod
    def getGrammar():
        return '"\\"" ' + WordList.getGrammar() + ' ".\\""'