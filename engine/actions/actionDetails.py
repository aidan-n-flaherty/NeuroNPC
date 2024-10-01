from engine.actions.actionType import ActionType

class ActionDetails:
    def __init__(self, actionType: ActionType, parameters, documentation: str, description: str, tags: list[str], classifications: list[str]) -> None:
        self._actionType = actionType
        self._parameters = parameters
        self._documentation = documentation
        self._description = description
        self._tags = tags
        self._classifications = classifications
    
    def getActionType(self):
        return self._actionType
    
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