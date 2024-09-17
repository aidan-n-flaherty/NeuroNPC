from engine.types.question import Question
from engine.types.statement import Statement

class Sentence(str):
    @staticmethod
    def getGrammar():
        return '(' + Question.getGrammar() + ' | ' + Statement.getGrammar() + ')'