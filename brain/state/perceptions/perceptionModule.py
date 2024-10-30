from brain.state.perceptions.perception import Perception
from engine.enums.relation import Relation
from engine.enums.degree import Degree
import time

class PerceptionModule:
    def __init__(self) -> None:
        self._perceptions = {}
    
    def exchange(self, perceptionModule: 'PerceptionModule'):
        for agentID, perception in perceptionModule._perceptions.items():
            if agentID not in self._perceptions:
                self._perceptions[agentID] = Perception(perception.getTimestamp(), agentID)
                self._perceptions[agentID].updateExternalNotes(perception.getTimestamp(), perception.getPrivateNotes() + perception.getExternalNotes())
        
        for agentID, perception in self._perceptions.items():
            if agentID not in perceptionModule._perceptions:
                perceptionModule._perceptions[agentID] = Perception(perception.getTimestamp(), agentID)
                perceptionModule._perceptions[agentID].updateExternalNotes(perception.getTimestamp(), perception.getPrivateNotes() + perception.getExternalNotes())
            
    
    def updateRelation(self, timestamp: int, agentID: int, relation: Relation):
        if agentID in self._perceptions:
            self._perceptions[agentID].updateRelation(timestamp, relation)
                
            return
        
        self._perceptions[agentID] = Perception(timestamp, agentID, relation=relation)

    def addNote(self, timestamp: int, agentID: int, note: str) -> None:
        if agentID in self._perceptions:
            self._perceptions[agentID].updateNotes(timestamp, note)
                
            return
        
        self._perceptions[agentID] = Perception(timestamp, agentID, note=note)

    def setTrustworthiness(self, timestamp: int, agentID: int, trustworthiness: Degree) -> None:
        if agentID in self._perceptions:
            self._perceptions[agentID].updateTrustworthiness(timestamp, trustworthiness)
                
            return
        
        self._perceptions[agentID] = Perception(timestamp, agentID, trustworthiness=trustworthiness)
    
    def getPerception(self, agentID: int):
        if agentID not in self._perceptions:
            self.updateRelation(time.time(), agentID, Relation.STRANGER)
        
        return self._perceptions[agentID]

    def getPerceptionStr(self, agentID: int) -> str:
        return self.getPerception(agentID).getIdentifier()
