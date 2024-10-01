class Policy(str):
    def __new__(cls, string):
        instance = super().__new__(cls, string.lower())
        return instance

    def __hash__(self):
        return hash(self.lower())
    
    def __eq__(self, other):
        return self.lower() == other.lower()