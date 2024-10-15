from engine.types.agentID import AgentID
from engine.types.itemID import ItemID
from engine.events.event import Event
from engine.stimuli.eventType import EventType
from engine.stimuli.notification import Notification
from engine.stimuli.actionType import ActionType
from enum import Enum

class ScheduledBehavior:
    def __init__(self, time: int, action: ActionType, actionParameters: list, repeating=False) -> None:
        self._time = time
        self._action = action
        self._actionParameters = actionParameters
        self._repeating = repeating
        self._activated = False

    def getTime(self) -> int:
        return self._time
    
    def getActionType(self) -> ActionType:
        return self._actionType

    def getActionParameters(self) -> list:
        return self._actionParameters
    
    def getRepeating(self) -> bool:
        return self._repeating
    
    def getActivated(self) -> bool:
        return self._activated
    
    def activate(self) -> bool:
        self._activated = True

    def reset(self) -> bool:
        self._activated = False