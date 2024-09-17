from engine.types.word import Word

class WordList(str):
    @staticmethod
    def getGrammar():
        return Word.getGrammar() + ' (([:;,])? " " ' + Word.getGrammar() + ')*'