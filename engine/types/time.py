class Time(str):
    @staticmethod
    def getGrammar():
        return '(([1-9] | ("1" [0-2])) ":" ([0-5]? [0-9]) (" AM" | " PM"))'