import LLM.generator.generator as Generator
import LLM.formatter.formatter as Formatter
from engine.core.world import World

class Evidence:
    def __init__(self, timestamp: int, witnessID: int, description: str) -> None:
        self._timestamp = timestamp
        self._witness = witnessID
        self._description = description
        self._embedding = Generator.encode(Formatter.removeStopWords(description))

    def getDescription(self):
        return self._description
    
    def withinTimeRange(self, timeStart: int, timeEnd: int) -> bool:
        return self._timestamp < timeEnd and self._timestamp > timeStart
    
    def referencesAgent(self, agentID: int) -> bool:
        return agentID == self._witnessID
    
    def getEmbedding(self):
        return self._embedding
    
    def getIdentifier(self):
        return "<Evidence collected {time}: \"{description}\">".format(time=Formatter.timeToString(self._timestamp), description=self._description)