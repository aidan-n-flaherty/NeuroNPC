from engine.actions.actionType import ActionType
import engine.actions.actionManager as ActionManager
from engine.types.sentence import Sentence
from engine.types.question import Question
from engine.types.statement import Statement
from engine.types.paragraph import Paragraph
from enum import Enum

customTypes = [Sentence, Question, Statement, Paragraph]

def generateGrammar(action: ActionType, world, agentID) -> str:
    return '"' + action + '(\" {} \")"'.format(generateParameterGrammar(ActionManager.getParameterTypes(action), world, agentID))

def generateParameterGrammar(parameterTypes: list, world, agentID):
    return "\", \" ".join([generateParameterGrammar(paramType, world, agentID) if type(paramType) is list else generateParamOptions(paramType, world, agentID) for paramType in parameterTypes])

def generateParamOptions(parameterType, world, agentID):
    if parameterType in customTypes:
        return parameterType.getGrammar()

    match type(parameterType):
        case int():
            return '[0-9]+'
        case float():
            return '("0" | ([1-9] [0-9]*)) "." [0-9]+'
        case str():
            return '"\"" [a-zA-Z ]+ "\""'
        case _:
            if issubclass(parameterType, Enum):
                return "({})".format(" | ".join(['"{}"'.format(elem.name) for elem in parameterType]))
            
            return parameterType.getGrammar(world, agentID)

def grammarMissing(action: ActionType, world, agentID) -> bool:
    return anyParameterMissing(ActionManager.getParameterTypes(action), world, agentID)

def anyParameterMissing(parameterTypes: list, world, agentID):
    return any([anyParameterMissing(paramType, world, agentID) if type(paramType) is list else parameterMissing(paramType, world, agentID) for paramType in parameterTypes])

def parameterMissing(parameterType, world, agentID):
    if parameterType in customTypes:
        return False

    match type(parameterType):
        case int():
            return False
        case float():
            return False
        case str():
            return False
        case _:
            if issubclass(parameterType, Enum):
                return False
            
            grammar = parameterType.getGrammar(world, agentID)

            return grammar == "" or grammar == "()"