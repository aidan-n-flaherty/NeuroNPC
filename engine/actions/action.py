from engine.types.agentID import AgentID
from engine.types.itemID import ItemID
from enum import Enum

class Action:
    def __init__(self, actionName: str, actionParameters: list, unparsedStr: str, descriptionStr: str) -> None:
        self._actionName = actionName
        self._actionParameters = actionParameters
        self._descriptionStr = descriptionStr
        self._unparsedStr = unparsedStr

    def getName(self) -> str:
        return self._actionName

    def getParameters(self) -> list:
        return self._actionParameters
    
    def getParameter(self, index: int):
        return self._actionParameters[index]
    
    def getDescription(self, world, agentID: int) -> str:
        if self._descriptionStr.find("{agent}") == -1:
            return self._descriptionStr.format(*[world.getAgent(param).getName() if isinstance(param, AgentID) else world.getItem(param).getName() if isinstance(param, ItemID) else param.name if isinstance(param, Enum) else param for param in self._actionParameters])

        return self._descriptionStr.format(agent=world.getAgent(agentID).getName(), *[world.getAgent(param).getName() if isinstance(param, AgentID) else world.getItem(param).getName() if isinstance(param, ItemID) else param.name if isinstance(param, Enum) else param for param in self._actionParameters])
    
    def getSelfDescription(self, world, agentID: int) -> str:
        return self._descriptionStr.format(agent="You", *[world.getAgent(param).getName() if isinstance(param, AgentID) else world.getItem(param).getName() if isinstance(param, ItemID) else param.name if isinstance(param, Enum) else param for param in self._actionParameters])
    
    def getObservedDescription(self, world, agentID: int, observerID: int) -> str:
        if self._descriptionStr.find("{agent}") == -1:
            return self._descriptionStr.format(*[(world.getAgent(param).getName() if param != observerID else "you") if isinstance(param, AgentID) else world.getItem(param).getName() if isinstance(param, ItemID) else param.name if isinstance(param, Enum) else param for param in self._actionParameters])

        return self._descriptionStr.format(agent=world.getAgent(agentID).getName(), *[(world.getAgent(param).getName() if param != observerID else "you") if isinstance(param, AgentID) else world.getItem(param).getName() if isinstance(param, ItemID) else param.name if isinstance(param, Enum) else param for param in self._actionParameters])
    
    def getFunctionCall(self):
        return self._unparsedStr

    def __str__(self):
        return "({}, {}, {})".format(self._actionName, self._actionParameters, self._descriptionStr)