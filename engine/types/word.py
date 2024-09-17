class Word(str):
    @staticmethod
    def getGrammar():
        return '("(")? (([a-z\']+ ("-" [a-z\']+)?) | ([A-Z\'] [a-z\']* ("-" [a-z\']+)?) | [0-9]+ | ([0-9]+ "." [0-9]+) | "-") (")")?'