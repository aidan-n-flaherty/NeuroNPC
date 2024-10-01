import LLM.generator.generator as Generator
import LLM.formatter.formatter as Formatter
from engine.actions.action import Action

class ObservedMemory:
    def __init__(self, timestamp: int, agentID: int, action: Action, selfDescription: str, description: str, observedDescription: str, embedding, note=None) -> None:
        self._timestamp = timestamp
        self._agentID = agentID
        self._description = description
        self._selfDescription = selfDescription
        self._observedDescription = observedDescription
        self._embedding = embedding
        self._action = action
        self._note = note

    def setNote(self, note: str):
        self._note = note

    def getAction(self):
        return self._action

    def getDescription(self):
        return self._description
    
    def getObservedDescription(self):
        return self._observedDescription
    
    def getFunctionCall(self):
        return self._action.getFunctionCall()
    
    def getSelfDescription(self):
        return self._selfDescription

    def withinTimeRange(self, timeStart: int, timeEnd: int) -> bool:
        return self._timestamp < timeEnd and self._timestamp > timeStart
    
    def referencesAgent(self, agentID: int) -> bool:
        return agentID == self._agentID
    
    def getAgentID(self) -> int:
        return self._agentID

    def getEmbedding(self):
        return self._embedding
    
    def getTimestamp(self):
        return self._timestamp

    def getDescription(self):
        return self._description
    
    def getNote(self):
        return "({})".format(self._note) if self._note else None
    
    def getIdentifier(self):
        return "<Memory from {time}: \"{description}\">".format(time=Formatter.timeToString(self._timestamp), description=self._description)