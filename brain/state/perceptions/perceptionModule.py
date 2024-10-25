from brain.state.perceptions.perception import Perception
from engine.enums.relation import Relation
import time

class PerceptionModule:
    def __init__(self) -> None:
        self._perceptions = {}
    
    def updateRelation(self, timestamp: int, agentID: int, relation: Relation):
        if agentID in self._perceptions:
            self._perceptions[agentID].updateRelation(timestamp, relation)
                
            return
        
        self._perceptions[agentID] = Perception(timestamp, agentID, relation=relation)

    def addNote(self, timestamp: int, agentID: int, note: str) -> None:
        if agentID in self._perceptions:
            self._perceptions[agentID].update(timestamp, note)
                
            return
        
        self._perceptions[agentID] = Perception(timestamp, agentID, note=note)
    
    def getPerception(self, agentID: int):
        return self._perceptions[agentID] if agentID in self._perceptions else None

    def getPerceptionStr(self, agentID: int) -> str:
        if agentID not in self._perceptions:
            self.updateRelation(time.time(), agentID, Relation.STRANGER)

        return self._perceptions[agentID].getIdentifier()
