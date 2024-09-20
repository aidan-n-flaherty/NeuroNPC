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
    SAY, PASS, REMAIN_SILENT, GIVE_ITEM, PICKUP_ITEM, ATTACK, MOVE_TO_LOCATION, ACCOMPANY_USER, ADD_LONG_TERM_GOAL, ADD_SHORT_TERM_GOAL, COLLECT_CLAIM, COLLECT_EVIDENCE, CHECK_CLAIM, QUERY_MEMORY_DATABASE, RAISE_EMOTION, LOWER_EMOTION, UPDATE_PERCEPTION_OF, END_CONVERSATION = range(18)

# actions accessible to the NPC
external = [Action.SAY, Action.PASS, Action.REMAIN_SILENT, Action.GIVE_ITEM, Action.PICKUP_ITEM, Action.ATTACK, Action.MOVE_TO_LOCATION, Action.ACCOMPANY_USER, Action.ADD_LONG_TERM_GOAL, Action.ADD_SHORT_TERM_GOAL, Action.CHECK_CLAIM, Action.QUERY_MEMORY_DATABASE, Action.RAISE_EMOTION, Action.LOWER_EMOTION, Action.END_CONVERSATION]

# actions of which at least one must be called per turn
mainActions = [Action.SAY, Action.GIVE_ITEM, Action.PICKUP_ITEM, Action.ATTACK, Action.MOVE_TO_LOCATION, Action.ACCOMPANY_USER, Action.CHECK_CLAIM, Action.QUERY_MEMORY_DATABASE, Action.END_CONVERSATION]

# actions that cannot be called together with other actions
singleActions = [Action.PASS]

# actions that other agents will have an opportunity to listen for
emittedActions = [Action.SAY, Action.GIVE_ITEM, Action.PICKUP_ITEM, Action.ATTACK]

# actions that can be immediately processed server-side due to only affecting the mental state
mentalActions = [Action.ADD_LONG_TERM_GOAL, Action.ADD_SHORT_TERM_GOAL, Action.CHECK_CLAIM, Action.QUERY_MEMORY_DATABASE, Action.RAISE_EMOTION, Action.LOWER_EMOTION, Action.END_CONVERSATION]

# validate
assert([action in external for action in mainActions])
assert([action in external for action in singleActions])
assert([action in external for action in emittedActions])
assert([action in external for action in mentalActions])

actionParameters = {}
actionDescriptions = {}
actionDocumentation = {}

actionParameters[Action.PASS] = []
actionDescriptions[Action.PASS] = ''
actionDocumentation[Action.PASS] = 'Do nothing this turn. You may not take any other actions.'

actionParameters[Action.SAY] = [("dialogue", Paragraph)]
actionDescriptions[Action.SAY] = '{agent} said "{0}"'
actionDocumentation[Action.SAY] = 'Say a single sentence or paragraph out loud, then wait for the other person to respond. Do not cut your dialogue short unless you want the other person to respond to something you said. Once you call this function, you will pass control of the conversation to the other person. You can call this function multiple times per turn.'

actionParameters[Action.REMAIN_SILENT] = []
actionDescriptions[Action.REMAIN_SILENT] = '{agent} remained silent.'
actionDocumentation[Action.REMAIN_SILENT] = 'Say nothing, and wait for the other person to continue.'

actionParameters[Action.ATTACK] = [("user_id", AgentID)]
actionDescriptions[Action.ATTACK] = '{agent} attacked {0}.'
actionDocumentation[Action.ATTACK] = 'Attack another user. Only use this when you want to use physical violence against another person.'

actionParameters[Action.MOVE_TO_LOCATION] = [("location", LocationID)]
actionDescriptions[Action.MOVE_TO_LOCATION] = '{agent} left the area.'
actionDocumentation[Action.MOVE_TO_LOCATION] = 'Walk to another location. This will terminate any conversations that you were having at this location.'

actionParameters[Action.ACCOMPANY_USER] = [("user_id", AgentID)]
actionDescriptions[Action.ACCOMPANY_USER] = '{agent} is now following {0}.'
actionDocumentation[Action.ACCOMPANY_USER] = 'Follow where the user takes you. Use this when you would like to accompany the user to a destination.'

actionParameters[Action.RAISE_EMOTION] = [("emotion", Emotion)]
actionDescriptions[Action.RAISE_EMOTION] = '{agent} raised their {0}.'
actionDocumentation[Action.RAISE_EMOTION] = 'Increases the strength of a certain emotion, and should be used whenever your emotions change.'

actionParameters[Action.LOWER_EMOTION] = [("emotion", Emotion)]
actionDescriptions[Action.LOWER_EMOTION] = '{agent} lowered their {0}.'
actionDocumentation[Action.LOWER_EMOTION] = 'Decreases the strength of a certain emotion, and should be used whenever your emotions change.'

actionParameters[Action.ADD_LONG_TERM_GOAL] = [("goal", Sentence)]
actionDescriptions[Action.ADD_LONG_TERM_GOAL] = '{agent} added {0} to long term goals.'
actionDocumentation[Action.ADD_LONG_TERM_GOAL] = 'Adds a goal to your long term goals.'

actionParameters[Action.ADD_SHORT_TERM_GOAL] = [("goal", Sentence)]
actionDescriptions[Action.ADD_SHORT_TERM_GOAL] = '{agent} added {0} to short term goals.'
actionDocumentation[Action.ADD_SHORT_TERM_GOAL] = 'Adds a goal to your short term goals'

actionParameters[Action.COLLECT_CLAIM] = [("source_user_id", AgentID), ("sentence", Sentence)]
actionDescriptions[Action.COLLECT_CLAIM] = '{agent} learned the fact "{1}" from {0}.'
actionDocumentation[Action.COLLECT_CLAIM] = 'When someone tells you an interesting piece of information, whether it is believable or not, immediately store their claim using this function. Since it is passed to a database as a standalone statement, use full names and IDs when referring to things. Write it in the 3rd person (i.e. refer to yourself using your full name and ID).'

actionParameters[Action.COLLECT_EVIDENCE] = [("sentence", Sentence)]
actionDescriptions[Action.COLLECT_EVIDENCE] = '{agent} stored information about "{0}".'
actionDocumentation[Action.COLLECT_EVIDENCE] = 'When someone does something, whether it is believable or not, immediately store their claim using this function. Since it is passed to a database as a standalone statement, use full names and IDs when referring to things. Write it in the 3rd person (i.e. refer to yourself using your full name and ID).'

actionParameters[Action.CHECK_CLAIM] = [("sentence", Sentence)]
actionDescriptions[Action.CHECK_CLAIM] = '{agent} consulted their memory about "{0}"'
actionDocumentation[Action.CHECK_CLAIM] = 'Use this function whenever the user claims or implies something that might not be true, or is definitely not true.'

actionParameters[Action.QUERY_MEMORY_DATABASE] = [("sentence", Sentence)]
actionDescriptions[Action.QUERY_MEMORY_DATABASE] = '{agent} consulted their memory about "{0}"'
actionDocumentation[Action.QUERY_MEMORY_DATABASE] = 'Use this function only when you feel that you need to remember something about your (the NPC\'s) past actions or encounters, or something that specifically requires knowledge about the game world. Since it is passed to a search engine as a standalone search query, use full names and IDs when referring to things. Only use this function when necessary, and avoid using it too often.'

actionParameters[Action.UPDATE_PERCEPTION_OF] = [("user_id", AgentID), ("note", Sentence)]
actionDescriptions[Action.UPDATE_PERCEPTION_OF] = '{agent} added "{1}" to their notes about {0}.'
actionDocumentation[Action.UPDATE_PERCEPTION_OF] = 'Whenever you change your opinion about someone else, make sure to call this function.'

actionParameters[Action.GIVE_ITEM] = [("target_user_id", AgentID), ("item_id", InventoryItemID)]
actionDescriptions[Action.GIVE_ITEM] = '{agent} gave {1} to {0}.'
actionDocumentation[Action.GIVE_ITEM] = 'Give an item to another user. You can only give items that you have in your inventory, so only call this function when you actually have the item you want to give. Whenever you say you\'re giving the user something, you MUST call this function so that you actually give it.'

actionParameters[Action.PICKUP_ITEM] = [("item_id", ItemID)]
actionDescriptions[Action.PICKUP_ITEM] = '{agent} picked up {0}.'
actionDocumentation[Action.PICKUP_ITEM] = 'Pick up an item that is within your sight.'

actionParameters[Action.END_CONVERSATION] = []
actionDescriptions[Action.END_CONVERSATION] = '{agent} ended the conversation.'
actionDocumentation[Action.END_CONVERSATION] = 'Once you feel like you tire of the conversation or there is nothing productive left to say, call this function.'

for action in Action:
    if not action in actionParameters:
        logging.error(action.name + ' not implemented')

def getActions() -> Action:
    return Action

def getActionNames() -> list[str]:
    return [action.name for action in external]

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