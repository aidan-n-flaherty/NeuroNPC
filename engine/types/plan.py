class Plan(str):
    @staticmethod
    def getGrammar():
        return '("\\"Names of functions I\'ll call this turn: " [^\\\\"\\\\)\\n]+ "\\"")'