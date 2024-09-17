import LLM.generator.generator as Generator
import LLM.formatter.formatter as Formatter

class Assertion:
    def __init__(self, id: int, timestamp: int, sourceID: int, claim: str, degree: int) -> None:
        self._id = id
        self._timestamp = timestamp
        self._sourceID = sourceID
        self._claim = claim
        self._degree = degree
        self._embedding = Generator.encode(Formatter.removeStopWords(claim))

    def getID(self):
        return self._id

    def getClaim(self):
        return self._claim
    
    def getSourceID(self):
        return self._sourceID
    
    def withinTimeRange(self, timeStart: int, timeEnd: int) -> bool:
        return self._timestamp < timeEnd and self._timestamp > timeStart
    
    def referencesAgent(self, sourceID: int) -> bool:
        return sourceID == self._sourceID
    
    def getDegree(self):
        return self._degree
    
    def getEmbedding(self):
        return self._embedding
    
    def getIdentifier(self, world):
        return "<Assertion collected {time}: {agent} claimed that \"{claim}\">".format(time=Formatter.timeToString(self._timestamp), agent=world.getAgent(self._sourceID).name, claim=self._claim)