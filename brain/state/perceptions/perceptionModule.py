from brain.state.perceptions.perception import Perception

class PerceptionModule:
    def __init__(self) -> None:
        self._perceptions = {}
    
    def addNote(self, timestamp: int, agentID: int, note: str) -> None:
        if agentID in self._perceptions:
            self._perceptions[agentID].update(timestamp, note)
                
            return
        
        self._perceptions[agentID] = Perception(timestamp, agentID, note)
    
    def getPerception(self, agentID: int) -> str:
        if agentID in self._perceptions:
            return self._perceptions[agentID].getIdentifier()
                
        return "The person (id: {}) is a stranger to you.".format(agentID)
