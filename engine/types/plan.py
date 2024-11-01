class Plan(str):
    @staticmethod
    def getGrammar():
        return '("\\"It would make sense to call the following function names: 1. " [^\\\\"\\\\(\\\\)\\n]+ "\\"")'