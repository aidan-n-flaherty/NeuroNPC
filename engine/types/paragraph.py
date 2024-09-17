from engine.types.wordList import WordList

class Paragraph(str):
    @staticmethod
    def getGrammar():
        return '"\\"" (' + WordList.getGrammar() + ' [\\\\.!?]) (" " ' + WordList.getGrammar() + ' [\\\\.!?])? "\\""'