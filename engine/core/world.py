from engine.classes.agent import Agent
from engine.classes.item import Item
from engine.classes.item import ShopItem #added here by chriss - testing shop items
from engine.classes.container import Container  #added by chris - testing containers
from engine.classes.location import Location
import engine.stimuli.notificationModule as NotificationModule
from engine.stimuli.notification import Notification
from engine.stimuli.actionType import ActionType
from engine.core.knowledgeBase import KnowledgeBase
from engine.classes.assertion import Assertion
import LLM.generator.generator as Generator
import time
from difflib import SequenceMatcher
from threading import Lock
import traceback

class World:
    def __init__(self, emitActionToClient):
        self._knowledgeBase = KnowledgeBase()
        self._agents = {}
        self._items = {}
        self._locations = {}
        self._reactionQueue = []
        self._processingLock = Lock()
        self._emitActionToClient = emitActionToClient
    
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

    def getAgent(self, agentID: int) -> Agent:
        return self._agents[agentID] if agentID in self._agents else None
    
    def getItem(self, itemID: int):
        return self._items[itemID] if itemID in self._items else None

    def getLocation(self, locationID: int):
        return self._locations[locationID] if locationID in self._locations else None
    
    def updateAgent(self, data: dict):
        self._agents[data['id']].update(data)
    
    def updateItem(self, data: dict):
        self._items[data['id']].update(data)

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
    
    def emitNotification(self, agentID: int, notification: Notification) -> bool:
        description = notification.getDescription(self, agentID)
        encoding = Generator.encode(description)

        if notification.getType() == ActionType('say'):
            found = False

            for (_, a) in self._agents.items():
                if a.isArtificial() and a.isConversingWith(agentID):
                    found = True
                    break

            if not found:
                agent = self.getAgent(agentID)
                closest = -1
                closestAgent = None

                for (_, a) in self._agents.items():
                    if a.isArtificial() and (closest < 0 or agent.distance(a) < closest):
                        closest = agent.distance(a)
                        closestAgent = a
            
                if closestAgent:
                    closestAgent.conversationStart(agent)

        self._processingLock.acquire()
        for (aID, agent) in self._agents.items():
            if aID != agentID and agent.isArtificial():
                self._reactionQueue.append((aID, agentID, description, encoding, notification))
        self._processingLock.release()

        return True
    
    def tick(self):
        while len(self._reactionQueue) > 0:
            agentID, sourceID, description, encoding, notification = self._reactionQueue.pop(0)
            agent = self._agents[agentID]
            actionAgent = self._agents[sourceID]

            self._processingLock.acquire()
            try:
                actions = agent.react(self, actionAgent, notification, time.time(), description, encoding)
                
                for a in actions:
                    if NotificationModule.shouldEmit(a.getType()):
                        self._emitActionToClient(agentID, a)

                print('\n'.join([str(a.getFunctionCall()) for a in actions]))
            except Exception:
                print(traceback.format_exc())
            self._processingLock.release()