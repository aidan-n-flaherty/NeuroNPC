from engine.types.sentence import Sentence
from engine.types.paragraph import Paragraph
from engine.types.agentID import AgentID
from engine.types.locationID import LocationID
from engine.types.itemID import ItemID
from engine.types.inventoryItemID import InventoryItemID
from brain.state.emotions.emotionModule import Emotion, Degree
from engine.core.world import World
from enum import Enum
import logging

class Action(Enum):
    SAY, PASS, REMAIN_SILENT, GIVE_ITEM, PICKUP_ITEM, ATTACK, MOVE_TO_LOCATION, ACCOMPANY_USER, ADD_LONG_TERM_GOAL, ADD_SHORT_TERM_GOAL, COLLECT_CLAIM, QUERY_MEMORY_DATABASE, RAISE_EMOTION, LOWER_EMOTION, UPDATE_PERCEPTION_OF, END_CONVERSATION = range(16)

actionParameters = {}
actionDescriptions = {}
actionDocumentation = {}
singleActions = []
mainActions = []
emittedActions = []
mentalActions = []

actionParameters[Action.PASS] = []
actionDescriptions[Action.PASS] = ''
actionDocumentation[Action.PASS] = 'Do nothing this turn. You may not take any other actions.'
singleActions.append(Action.PASS)

actionParameters[Action.SAY] = [("dialogue", Paragraph)]
actionDescriptions[Action.SAY] = '{agent} said "{0}"'
actionDocumentation[Action.SAY] = 'Say a single sentence or paragraph out loud, then wait for the other person to respond. Do not cut your dialogue short unless you want the other person to respond to something you said. Once you call this function, you will pass control of the conversation to the other person. You can call this function multiple times per turn.'
mainActions.append(Action.SAY)
emittedActions.append(Action.SAY)

actionParameters[Action.REMAIN_SILENT] = []
actionDescriptions[Action.REMAIN_SILENT] = '{agent} remained silent.'
actionDocumentation[Action.REMAIN_SILENT] = 'Say nothing, and wait for the other person to continue.'
mainActions.append(Action.REMAIN_SILENT)

actionParameters[Action.ATTACK] = [("user_id", AgentID)]
actionDescriptions[Action.ATTACK] = '{agent} attacked {0}.'
actionDocumentation[Action.ATTACK] = 'Attack another user. Only use this when you want to use physical violence against another person.'
mainActions.append(Action.ATTACK)
emittedActions.append(Action.ATTACK)

actionParameters[Action.MOVE_TO_LOCATION] = [("location", LocationID)]
actionDescriptions[Action.MOVE_TO_LOCATION] = '{agent} left the area.'
actionDocumentation[Action.MOVE_TO_LOCATION] = 'Walk to another location. This will terminate any conversations that you were having at this location.'
mainActions.append(Action.MOVE_TO_LOCATION)
emittedActions.append(Action.MOVE_TO_LOCATION)

actionParameters[Action.ACCOMPANY_USER] = [("user_id", AgentID)]
actionDescriptions[Action.ACCOMPANY_USER] = '{agent} is now following {0}.'
actionDocumentation[Action.ACCOMPANY_USER] = 'Follow where the user takes you. Use this when you would like to accompany the user to a destination.'
mainActions.append(Action.ACCOMPANY_USER)
emittedActions.append(Action.ACCOMPANY_USER)

actionParameters[Action.RAISE_EMOTION] = [("emotion", Emotion)]
actionDescriptions[Action.RAISE_EMOTION] = '{agent} raised their {0}.'
actionDocumentation[Action.RAISE_EMOTION] = 'Increases the strength of a certain emotion, and should be used whenever your emotions change.'
mentalActions.append(Action.RAISE_EMOTION)

actionParameters[Action.LOWER_EMOTION] = [("emotion", Emotion)]
actionDescriptions[Action.LOWER_EMOTION] = '{agent} lowered their {0}.'
actionDocumentation[Action.LOWER_EMOTION] = 'Decreases the strength of a certain emotion, and should be used whenever your emotions change.'
mentalActions.append(Action.LOWER_EMOTION)

actionParameters[Action.ADD_LONG_TERM_GOAL] = [("goal", Sentence)]
actionDescriptions[Action.ADD_LONG_TERM_GOAL] = '{agent} added {0} to long term goals.'
actionDocumentation[Action.ADD_LONG_TERM_GOAL] = 'Adds a goal to your long term goals.'
mentalActions.append(Action.ADD_LONG_TERM_GOAL)

actionParameters[Action.ADD_SHORT_TERM_GOAL] = [("goal", Sentence)]
actionDescriptions[Action.ADD_SHORT_TERM_GOAL] = '{agent} added {0} to short term goals.'
actionDocumentation[Action.ADD_SHORT_TERM_GOAL] = 'Adds a goal to your short term goals'
mentalActions.append(Action.ADD_SHORT_TERM_GOAL)

actionParameters[Action.COLLECT_CLAIM] = [("source_user_id", AgentID), ("sentence", Sentence)]
actionDescriptions[Action.COLLECT_CLAIM] = '{agent} learned the fact "{1}" from {0}.'
actionDocumentation[Action.COLLECT_CLAIM] = 'When someone tells you an interesting piece of information, whether it is believable or not, immediately store their claim using this function. Since it is passed to a database as a standalone statement, use full names and IDs when referring to things. Write it in the 3rd person (i.e. refer to yourself using your full name and ID).'
mentalActions.append(Action.COLLECT_CLAIM)

actionParameters[Action.QUERY_MEMORY_DATABASE] = [("sentence", Sentence)]
actionDescriptions[Action.QUERY_MEMORY_DATABASE] = '{agent} consulted their memory about "{0}"'
actionDocumentation[Action.QUERY_MEMORY_DATABASE] = 'Use this function only when you feel that you need to remember something about your (the NPC\'s) past actions or encounters, or something that specifically requires knowledge about the game world. Since it is passed to a search engine as a standalone search query, use full names and IDs when referring to things. Only use this function when necessary, and avoid using it too often.'
mentalActions.append(Action.QUERY_MEMORY_DATABASE)
mainActions.append(Action.QUERY_MEMORY_DATABASE)

actionParameters[Action.UPDATE_PERCEPTION_OF] = [("user_id", AgentID), ("note", Sentence)]
actionDescriptions[Action.UPDATE_PERCEPTION_OF] = '{agent} added "{1}" to their notes about {0}.'
actionDocumentation[Action.UPDATE_PERCEPTION_OF] = 'Whenever you change your opinion about someone else, make sure to call this function.'
mentalActions.append(Action.UPDATE_PERCEPTION_OF)

actionParameters[Action.GIVE_ITEM] = [("target_user_id", AgentID), ("item_id", InventoryItemID)]
actionDescriptions[Action.GIVE_ITEM] = '{agent} gave {1} to {0}.'
actionDocumentation[Action.GIVE_ITEM] = 'Give an item to another user. You can only give items that you have in your inventory, so only call this function when you actually have the item you want to give. Whenever you say you\'re giving the user something, you MUST call this function so that you actually give it.'
mainActions.append(Action.GIVE_ITEM)
emittedActions.append(Action.GIVE_ITEM)

actionParameters[Action.PICKUP_ITEM] = [("item_id", ItemID)]
actionDescriptions[Action.PICKUP_ITEM] = '{agent} picked up {0}.'
actionDocumentation[Action.PICKUP_ITEM] = 'Pick up an item that is within your sight.'
mainActions.append(Action.PICKUP_ITEM)
emittedActions.append(Action.PICKUP_ITEM)

actionParameters[Action.END_CONVERSATION] = []
actionDescriptions[Action.END_CONVERSATION] = '{agent} ended the conversation.'
actionDocumentation[Action.END_CONVERSATION] = 'Once you feel like you tire of the conversation or there is nothing productive left to say, call this function.'
mainActions.append(Action.END_CONVERSATION)
emittedActions.append(Action.END_CONVERSATION)

for action in Action:
    if not action in actionParameters:
        logging.error(action.name + ' not implemented')

def getActions() -> Action:
    return Action

def getActionNames() -> list[str]:
    return [action.name for action in Action]

def getMainActionNames() -> list[str]:
    return [action.name for action in mainActions]

def getSingleActionNames() -> list[str]:
    return [action.name for action in singleActions]

def getMentalActions() -> list[Action]:
    return mentalActions

def getMentalActionNames() -> list[str]:
    return [action.name for action in mentalActions]

def getActionDescriptions() -> list[str]:
    return [getFunctionStr(action.name) for action in Action]

def shouldEmit(action: str):
    return Action[action.upper()] in singleActions

def getParameterTypes(action: str):
    return [pair[1] for pair in actionParameters[Action[action.upper()]]]

def getFunctionStr(action: str):
    return "{}({})".format(Action[action.upper()].name, ", ".join(["{}: {}".format(pair[0], pair[1].__name__) for pair in actionParameters[Action[action.upper()]]]))

def validAction(action: str):
    return action.upper() in [a.name for a in actionParameters.keys()]

def getDescription(action: str):
    return actionDescriptions[Action[action.upper()]]

def getDocumentation(action: str):
    return actionDocumentation[Action[action.upper()]]