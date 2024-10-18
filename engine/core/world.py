from engine.classes.agent import Agent
from engine.classes.item import Item
from engine.classes.item import ShopItem #added here by chriss - testing shop items
from engine.classes.container import Container  #added by chris - testing containers
from engine.classes.location import Location
from engine.stimuli.notification import Notification
from engine.core.knowledgeBase import KnowledgeBase
from engine.classes.assertion import Assertion
import LLM.generator.generator as Generator
import time
from difflib import SequenceMatcher

class World:
    def __init__(self):
        self._knowledgeBase = KnowledgeBase()
        self._agents = {}
        self._items = {}
        self._locations = {}
    
    def getKnowledgeBase(self):
        return self._knowledgeBase

    def getClaim(self, claim: str, sourceID: int, degree: int):
        return self._knowledgeBase.getClaim(claim, sourceID, degree)
    
    def getContradictions(self, assertion: Assertion):
        return self._knowledgeBase.getContradictions(assertion)
    
    def getAgentByName(self, agentName: str):
        options = sorted(self._agents.values(), key=lambda agent: max([SequenceMatcher(None, name, agentName).ratio() for name in [agent.getName(), agent.getFirstName(), agent.getLastName()]]))

        if max([SequenceMatcher(None, name, agentName).ratio() for name in [options[-1].getName(), options[-1].getFirstName(), options[-1].getLastName()]]) > 0.5:
            return options[-1]
        return None

    def getAgent(self, agentID: int):
        return self._agents[agentID] if agentID in self._agents else None
    
    def getItem(self, itemID: int):
        return self._items[itemID] if itemID in self._items else None

    def getLocation(self, locationID: int):
        return self._locations[locationID] if locationID in self._locations else None

    def registerAgent(self, agent: Agent):
        self._agents[agent.getID()] = agent

    def registerItem(self, item: Item):
        self._items[item.getID()] = item
    
    def registerShopItem(self, item: ShopItem):
        self._items[item.getID()] = item
    
    def registerContainer(self, item: Container):
        self._items[item.getID()] = item

    
    def registerLocation(self, location: Location):
        self._locations[location.getID()] = location
    
    def getAccessibleLocations(self, agentID: int):
        if agentID not in self._agents:
            return []

        agent = self._agents[agentID]

        return self.getLocation(agent.getLocationID()).getAdjacentIDs()

    def getInteractableAgents(self, agentID: int) -> list[int]:
        if agentID not in self._agents:
            return []

        agent = self._agents[agentID]
        interactable = []

        for (id, a) in self._agents.items():
            if id == agentID:
                continue

            if agent.canInteract(a):
                interactable.append(id)
        
        return interactable
    
    def getInteractableItems(self, agentID: int) -> list[int]:
        if agentID not in self._agents:
            return []
        
        agent = self._agents[agentID]
        interactable = []

        for (id, a) in self._items.items():
            if agent.canInteract(a):
                interactable.append(id)
        
        return interactable
    
    def emitAction(self, agentID: int, notification: Notification) -> bool:
        actionAgent = self._agents[agentID]
        
        description = notification.getDescription(self, agentID)
        encoding = Generator.encode(description)

        for (aID, agent) in self._agents.items():
            if aID != agentID and agent.isArtificial():
                print([str(a) for a in agent.react(self, actionAgent, notification, time.time(), description, encoding)])