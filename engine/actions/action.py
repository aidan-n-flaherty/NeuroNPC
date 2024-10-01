from engine.types.agentID import AgentID
from engine.types.itemID import ItemID
from engine.actions.actionType import ActionType
from enum import Enum

class Action:
    def __init__(self, actionType: ActionType, actionParameters=[], unparsedStr="", descriptionStr="") -> None:
        self._actionType = actionType
        self._actionParameters = actionParameters
        self._descriptionStr = descriptionStr
        self._unparsedStr = unparsedStr

    def getType(self) -> ActionType:
        return self._actionType

    def getParameters(self) -> list:
        return self._actionParameters
    
    def getParameter(self, index: int):
        return self._actionParameters[index]
    
    def getDescription(self, world, agentID: int) -> str:
        if self._descriptionStr.find("{agent}") == -1:
            return self._descriptionStr.format(*[world.getAgent(param).getIdentifier() if isinstance(param, AgentID) else world.getItem(param).getName() if isinstance(param, ItemID) else param.name if isinstance(param, Enum) else param for param in self._actionParameters])

        return self._descriptionStr.format(agent=world.getAgent(agentID).getIdentifier(), *[world.getAgent(param).getIdentifier() if isinstance(param, AgentID) else world.getItem(param).getName() if isinstance(param, ItemID) else param.name if isinstance(param, Enum) else param for param in self._actionParameters])
    
    def getSelfDescription(self, world, agentID: int) -> str:
        return self._descriptionStr.format(agent="You", *[world.getAgent(param).getIdentifier() if isinstance(param, AgentID) else world.getItem(param).getName() if isinstance(param, ItemID) else param.name if isinstance(param, Enum) else param for param in self._actionParameters])
    
    def getObservedDescription(self, world, agentID: int, observerID: int) -> str:
        if self._descriptionStr.find("{agent}") == -1:
            return self._descriptionStr.format(*[(world.getAgent(param).getIdentifier() if param != observerID else "you") if isinstance(param, AgentID) else world.getItem(param).getName() if isinstance(param, ItemID) else param.name if isinstance(param, Enum) else param for param in self._actionParameters])

        return self._descriptionStr.format(agent=world.getAgent(agentID).getIdentifier(), *[(world.getAgent(param).getIdentifier() if param != observerID else "you") if isinstance(param, AgentID) else world.getItem(param).getName() if isinstance(param, ItemID) else param.name if isinstance(param, Enum) else param for param in self._actionParameters])
    
    def getFunctionCall(self):
        return self._unparsedStr

    def __str__(self):
        return "({}, {}, {})".format(self._actionType, self._actionParameters, self._descriptionStr)