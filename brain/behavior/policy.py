from engine.types.agentID import AgentID
from engine.types.itemID import ItemID
from engine.events.event import Event
from engine.stimuli.eventType import EventType
from engine.stimuli.notification import Notification
from engine.stimuli.actionType import ActionType
from enum import Enum

class Policy:
    def __init__(self, trigger: EventType | ActionType, triggerParameters: list, response: ActionType, responseParameters: list, activationCondition="") -> None:
        self._triggerType = trigger
        self._responseType = response
        self._triggerParameters = triggerParameters
        self._responseParameters = responseParameters
        self._activationCondition = activationCondition

    def getTriggerType(self) -> EventType | ActionType:
        return self._triggerType
    
    def getResponseType(self) -> ActionType:
        return self._responseType

    def getTriggerParameters(self) -> list:
        return self._triggerParameters
    
    def getTriggerParameter(self, index: int):
        return self._triggerParameters[index]
    
    def getResponseParameters(self) -> list:
        return self._responseParameters
    
    def getResponseParameter(self, index: int):
        return self._responseParameters[index]
    
    def getActivationCondition(self):
        return self._activationCondition
    
    def matches(self, trigger: Notification):
        return self.getTriggerType() == trigger.getType() and all([self._triggerParameters[i] == None or trigger.getParameter(i) == self._triggerParameters[i] for i in range(len(self.getTriggerParameters()))])