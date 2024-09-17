from engine.types.wordList import WordList

class Question(WordList):
    @staticmethod
    def getGrammar():
        return '"\\"" ' + WordList.getGrammar() + ' "?\\""'