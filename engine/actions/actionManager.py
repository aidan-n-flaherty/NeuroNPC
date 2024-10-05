from engine.types.sentence import Sentence
from engine.types.paragraph import Paragraph
from engine.types.agentID import AgentID
from engine.types.locationID import LocationID
from engine.types.itemID import ItemID
from engine.types.inventoryItemID import InventoryItemID
from brain.state.emotions.emotionModule import Emotion, Degree
from engine.actions.actionType import ActionType
from engine.actions.actionDetails import ActionDetails
from enum import Enum
import logging
import json
import re

supportedActions = {}

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

with open("engine/actions/default/defaultActions.json", "r") as file:
    obj = json.loads(file.read())
    for action in obj[0]:
        content = obj[0][action]
        parameters = content["parameters"]
        documentation = content["documentation"]
        description = content["description"]
        tags = [tag.upper() for tag in content["tags"]]
        classifications = [classification.upper() for classification in content["classification"]] if "classification" in content else []

        supportedActions[ActionType(action)] = ActionDetails(ActionType(action), substituteClasses(parameters), documentation, description, tags, classifications)

def getActions() -> list[ActionType]:
    return supportedActions.keys()

def getMainActions() -> list[ActionType]:
    return [action for action, details in supportedActions.items() if details.hasTag("CORE") and details.hasTag("EXTERNAL")]

def getSingleActions() -> list[ActionType]:
    return [action for action, details in supportedActions.items() if details.hasTag("SINGLE") and details.hasTag("EXTERNAL")]

def getMentalActions() -> list[ActionType]:
    return [action for action, details in supportedActions.items() if details.hasTag("MENTAL") and details.hasTag("EXTERNAL")]

def getActionDescriptions() -> list[str]:
    return [getFunctionStr(action) for action, details in supportedActions.items() if details.hasTag("EXTERNAL")]

def shouldEmit(action: ActionType):
    return supportedActions[action].hasTag("EMIT")

def isHostile(action: ActionType):
    return supportedActions[action].hasClassification("HOSTILE")

def getParameterTypes(action: ActionType):
    return [parameter for parameter in supportedActions[action].getParameters().values()]

def getFunctionStr(action: ActionType):
    return "{}({})".format(str(action), ", ".join(["{}: {}".format(param, paramType.__name__) for param, paramType in supportedActions[action].getParameters().items()]))

def validAction(action: ActionType):
    if action in supportedActions:
        return True
    else:
        print("ERROR: {} is not a valid type".format(action))
        return False

def getDescription(action: ActionType):
    return supportedActions[action].getDescription()

def getDocumentation(action: ActionType):
    return supportedActions[action].getDocumentation()