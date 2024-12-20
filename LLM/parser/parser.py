import re
import logging
from typing import cast
from enum import Enum

from engine.stimuli.notification import Notification
from engine.stimuli.actionType import ActionType
import engine.stimuli.notificationModule as NotificationModule

# expects a string in the format:
#   funcA(argA, argB)
#   funcB(argA, argB, argC)
#   funcC()
def parseFunctionList(functionListStr: str) -> list[Notification]:
    functionListStr = functionListStr.strip()

    functionCalls = functionListStr.split("\n")

    returnCalls = []

    for functionCall in functionCalls:
        returnCalls.append(parseFunctionCall(functionCall))
    
    return returnCalls

def parseReactionList(functionReactionStr: str) -> list:
    functionReactionStr = functionReactionStr.strip()

    functionCalls = functionReactionStr.split("\n")

    returnCalls = []

    for reaction in functionCalls:
        returnCalls.append(parseReaction(reaction))
    
    return returnCalls

def parseReaction(functionCallStr: str) -> list:
    functionCalls = functionCallStr[3:].split(" then ")
    return [parseFunctionCall(functionCalls[0]), parseFunctionCall(functionCalls[1])]

# expects a string in the format:
#   funcA(argA, argB, argC)
def parseFunctionCall(functionCallStr: str) -> Notification:
    splitIndex = functionCallStr.index('(')

    if not splitIndex:
        return None
    
    functionName = functionCallStr[0:splitIndex]

    if not NotificationModule.validAction(ActionType(functionName)):
        return None

    functionArgs = parse_array(functionCallStr[splitIndex:], NotificationModule.getParameterTypes(ActionType(functionName)))

    return Notification(functionName, functionArgs, functionCallStr, NotificationModule.getDescription(ActionType(functionName)))

def is_array(argStr: str):
    if not argStr:
        return False
    
    return (argStr[0] == '(' and argStr[-1] == ')') or (argStr[0] == '[' and argStr[-1] == ']') or (argStr[0] == '{' and argStr[-1] == '}') or (argStr[0] == '<' and argStr[-1] == '>')

def is_string(argStr: str):
    return len(argStr) >= 2 and argStr[0] in ["\"", "'"] and argStr[-1] in ["\"", "'"] and argStr[0] == argStr[-1]

# given a string containing a list of comma-separated arguments, split by only the top-level commas:
#   "[a, b, [c, d]]" => ["a", "b", "[c, d]"]
# and a list of types that each argument should be cast to:
#   [int, str, [bool, bool]]
def parse_array(arrayStr: str, typeArr):
    while is_array(arrayStr):
        arrayStr = arrayStr[1:-1]

    if len(arrayStr) == 0:
        return []
    
    if arrayStr == "_":
        return None

    inString = None
    bracketQueue = []

    splitIndices = [0]

    openList = ['(', '[', '{', '<']
    closeList = [')', ']', '}', '>']

    for i in range(len(arrayStr)):
        if inString:
            if arrayStr[i] == inString:
                inString = None
        else:
            if arrayStr[i] == '"' or arrayStr[i] == '\'':
                inString = arrayStr[i]
            elif arrayStr[i] in openList:
                bracketQueue.append(arrayStr[i])
            elif arrayStr[i] in closeList and bracketQueue and bracketQueue[-1] == openList[closeList.index(arrayStr[i])]:
                bracketQueue.pop()
            elif arrayStr[i] == ',' and not bracketQueue and not inString:
                splitIndices.append(i)
    
    if len(bracketQueue) > 0:
        logging.exception('Malformed brackets provided to parse_array')
        return None
    
    if inString:
        logging.exception('String not closed in argument passed to parse_array')
        return None

    returnVal = [arrayStr[i + 1 if i > 0 else 0:j].strip() for i,j in zip(splitIndices, splitIndices[1:]+[None])]

    if len(returnVal) != len(typeArr) and len(typeArr) > 1:
        logging.exception('Invalid array provided to parse_array')
        return None
    
    for i in range(len(returnVal)):
        typeCast = typeArr[i] if len(typeArr) > 1 else typeArr[0]

        while is_string(returnVal[i]):
            returnVal[i] = returnVal[i][1:-1]

        returnVal[i] = (parse_array(returnVal[i], typeCast) if is_array(returnVal[i]) else typeCast[returnVal[i].upper()] if issubclass(typeCast, Enum) else typeCast(returnVal[i])) if returnVal[i] != "_" else None

    return returnVal