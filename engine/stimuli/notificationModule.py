from engine.types.sentence import Sentence
from engine.types.paragraph import Paragraph
from engine.types.agentID import AgentID
from engine.types.locationID import LocationID
from engine.types.itemID import ItemID
from engine.types.inventoryItemID import InventoryItemID
from brain.state.emotions.emotionModule import Emotion, Degree
from engine.stimuli.actionType import ActionType
from engine.stimuli.eventType import EventType
from engine.stimuli.notificationDetails import NotificationDetails
from enum import Enum
import logging
import json
import re

supportedActions = {}

supportedEvents = {}

supportedNotifications = {}

supportedClasses = {
    "str": str,
    "int": int,
    "float": float,
    "bool": bool
}

import glob
import importlib
import importlib, inspect
filepaths = glob.glob("engine/classes/*.py") + glob.glob("engine/types/*.py") + glob.glob("engine/enums/*.py")

for filepath in filepaths:
    if filepath.endswith("__init__.py"):
        continue

    args = re.split(r'[/\\]', filepath)
    filename = args[-1].split('.py')[0]

    module = importlib.import_module('.'.join(args[:-1]) + '.' + filename)

    for name, classObj in inspect.getmembers(module, inspect.isclass):
        supportedClasses[name.lower()] = classObj

def substituteClasses(json):
    if type(json) is list:
        for i in range(len(json)):
            json[i] = substituteClasses(json[i])
        
        return json
    elif type(json) is dict:
        for key in json:
            json[key] = substituteClasses(json[key])
        
        return json
    elif str(json).lower() in supportedClasses.keys():
        return supportedClasses[str(json).lower()]
    else:
        return json

with open("engine/stimuli/default/defaultEvents.json", "r") as file:
    obj = json.loads(file.read())
    for action in obj[0]:
        content = obj[0][action]
        parameters = content["parameters"]
        documentation = content["documentation"]
        description = content["description"]
        tags = [tag.upper() for tag in content["tags"]]
        classifications = [classification.upper() for classification in content["classification"]] if "classification" in content else []

        supportedEvents[EventType(action)] = NotificationDetails(EventType(action), substituteClasses(parameters), documentation, description, tags, classifications)
        supportedNotifications[EventType(action)] = supportedEvents[EventType(action)]


with open("engine/stimuli/default/defaultActions.json", "r") as file:
    obj = json.loads(file.read())
    for action in obj[0]:
        content = obj[0][action]
        parameters = content["parameters"]
        documentation = content["documentation"]
        description = content["description"]
        tags = [tag.upper() for tag in content["tags"]]
        classifications = [classification.upper() for classification in content["classification"]] if "classification" in content else []

        supportedActions[ActionType(action)] = NotificationDetails(ActionType(action), substituteClasses(parameters), documentation, description, tags, classifications)
        supportedNotifications[EventType(action)] = supportedActions[EventType(action)]

def getNotifications() -> list[EventType | ActionType]:
    return supportedNotifications.keys()

def getActions() -> list[ActionType]:
    return supportedActions.keys()

def getEvents() -> list[EventType]:
    return supportedEvents.keys()

def getMainActions() -> list[ActionType]:
    return [action for action, details in supportedActions.items() if details.hasTag("CORE") and details.hasTag("EXTERNAL")]

def getSingleActions() -> list[ActionType]:
    return [action for action, details in supportedActions.items() if details.hasTag("SINGLE") and details.hasTag("EXTERNAL")]

def getNonMentalActions() -> list[ActionType]:
    return [action for action, details in supportedActions.items() if not details.hasTag("MENTAL") and details.hasTag("EXTERNAL")]

def getMentalActions() -> list[ActionType]:
    return [action for action, details in supportedActions.items() if details.hasTag("MENTAL") and details.hasTag("EXTERNAL")]

def getActionDescriptions() -> list[str]:
    return [getFunctionStr(action) for action, details in supportedActions.items() if details.hasTag("EXTERNAL")]

def isEphemeral(notificationType: ActionType | EventType):
    return supportedNotifications[notificationType].hasTag("EPHEMERAL")

def shouldEmit(notificationType: ActionType | EventType):
    return supportedNotifications[notificationType].hasTag("EMITTED")

def isHostile(notificationType: ActionType | EventType):
    return supportedNotifications[notificationType].hasClassification("HOSTILE")

def getParameterTypes(notificationType: ActionType | EventType):
    return [parameter for parameter in supportedNotifications[notificationType].getParameters().values()]

def getFunctionStr(notificationType: ActionType | EventType):
    return "{}({})".format(str(notificationType), ", ".join(["{}: {}".format(param, paramType.__name__) for param, paramType in supportedNotifications[notificationType].getParameters().items()]))

def validAction(notificationType: ActionType | EventType):
    if notificationType in supportedNotifications:
        return True
    else:
        print("ERROR: {} is not a valid type".format(notificationType))
        return False

def getDescription(notificationType: ActionType | EventType):
    return supportedNotifications[notificationType].getDescription()

def getDocumentation(notificationType: ActionType | EventType):
    return supportedNotifications[notificationType].getDocumentation()