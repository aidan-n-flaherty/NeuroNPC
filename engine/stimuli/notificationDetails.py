from engine.stimuli.actionType import ActionType
from engine.stimuli.eventType import EventType

class NotificationDetails:
    def __init__(self, actionType: ActionType | EventType, parameters, documentation: str, description: str, tags: list[str], classifications: list[str]) -> None:
        self._notificationType = actionType
        self._parameters = parameters
        self._documentation = documentation
        self._description = description
        self._tags = tags
        self._classifications = classifications
    
    def getType(self) -> ActionType | EventType:
        return self._notificationType
    
    def getParameters(self):
        return self._parameters
    
    def getDocumentation(self):
        return self._documentation
    
    def getDescription(self):
        return self._description
    
    def getTags(self):
        return self._tags
    
    def getClassifications(self):
        return self._classifications
    
    def hasTag(self, tag: str):
        return tag in self._tags
    
    def hasClassification(self, classification: str):
        return classification in self._classifications