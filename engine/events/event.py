from engine.types.agentID import AgentID
from engine.types.itemID import ItemID
from engine.stimuli.eventType import EventType
from enum import Enum

class Event:
    def __init__(self, eventType: EventType, actionParameters=[], unparsedStr="", descriptionStr="") -> None:
        self._eventType = eventType
        self._notificationParameters = actionParameters
        self._descriptionStr = descriptionStr
        self._unparsedStr = unparsedStr

    def getType(self) -> EventType:
        return self._eventType

    def getParameters(self) -> list:
        return self._notificationParameters
    
    def getParameter(self, index: int):
        return self._notificationParameters[index]
    
    def getDescription(self, world, agentID: int) -> str:
        if self._descriptionStr.find("{agent}") == -1:
            return self._descriptionStr.format(*[world.getAgent(param).getIdentifier() if isinstance(param, AgentID) else world.getItem(param).getName() if isinstance(param, ItemID) else param.name if isinstance(param, Enum) else param for param in self._notificationParameters])

        return self._descriptionStr.format(agent=world.getAgent(agentID).getIdentifier(), *[world.getAgent(param).getIdentifier() if isinstance(param, AgentID) else world.getItem(param).getName() if isinstance(param, ItemID) else param.name if isinstance(param, Enum) else param for param in self._notificationParameters])
    
    def getSelfDescription(self, world, agentID: int) -> str:
        return self._descriptionStr.format(agent="You", *[world.getAgent(param).getIdentifier() if isinstance(param, AgentID) else world.getItem(param).getName() if isinstance(param, ItemID) else param.name if isinstance(param, Enum) else param for param in self._notificationParameters])
    
    def getObservedDescription(self, world, agentID: int, observerID: int) -> str:
        if self._descriptionStr.find("{agent}") == -1:
            return self._descriptionStr.format(*[(world.getAgent(param).getIdentifier() if param != observerID else "you") if isinstance(param, AgentID) else world.getItem(param).getName() if isinstance(param, ItemID) else param.name if isinstance(param, Enum) else param for param in self._notificationParameters])

        return self._descriptionStr.format(agent=world.getAgent(agentID).getIdentifier(), *[(world.getAgent(param).getIdentifier() if param != observerID else "you") if isinstance(param, AgentID) else world.getItem(param).getName() if isinstance(param, ItemID) else param.name if isinstance(param, Enum) else param for param in self._notificationParameters])
    
    def getFunctionCall(self):
        return self._unparsedStr

    def __str__(self):
        return "({}, {}, {})".format(self._eventType, self._notificationParameters, self._descriptionStr)