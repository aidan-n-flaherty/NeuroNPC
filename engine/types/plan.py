class Plan(str):
    @staticmethod
    def getGrammar():
        return '("\\"" [^\\\\"\\\\)]+ "\\"")'