from engine.stimuli.actionType import ActionType
from engine.stimuli.eventType import EventType
import engine.stimuli.notificationModule as NotificationModule
from engine.types.sentence import Sentence
from engine.types.question import Question
from engine.types.statement import Statement
from engine.types.paragraph import Paragraph
from enum import Enum

customTypes = [Sentence, Question, Statement, Paragraph]

def generateGrammar(notification: ActionType | EventType, world, agentID: int, substitutions=[]) -> str:
    return '"' + notification + '(\" {} \")"'.format(generateParameterGrammar(NotificationModule.getParameterTypes(notification), world, agentID, substitutions))

def generateParameterGrammar(parameterTypes: list, world, agentID: int, substitutions: list):
    return "\", \" ".join([generateParameterGrammar(paramType, world, agentID, substitutions) if type(paramType) is list else generateParamOptions(paramType, world, agentID, substitutions) for paramType in parameterTypes])

def generateParamOptions(parameterType, world, agentID: int, substitutions: list):
    formattedStr = '({} | ' + ' | '.join(['"{}"'.format(substitution[1]) for substitution in substitutions if not substitution[0] or issubclass(parameterType, substitution[0])]) + ')' if substitutions and any([True for substitution in substitutions if not substitution[0] or issubclass(parameterType, substitution[0])]) else '{}'

    if parameterType in customTypes:
        return formattedStr.format(parameterType.getGrammar())

    match type(parameterType):
        case int():
            return formattedStr.format('[0-9]+')
        case float():
            return formattedStr.format('("0" | ([1-9] [0-9]*)) "." [0-9]+')
        case str():
            return formattedStr.format('"\"" [a-zA-Z ]+ "\""')
        case _:
            if issubclass(parameterType, Enum):
                return formattedStr.format("({})".format(" | ".join(['"{}"'.format(elem.name.lower()) for elem in parameterType])))
            
            return formattedStr.format(parameterType.getGrammar(world, agentID))

def grammarMissing(notificationType: ActionType | EventType, world, agentID, substitutions=[]) -> bool:
    return anyParameterMissing(NotificationModule.getParameterTypes(notificationType), world, agentID, substitutions)

def anyParameterMissing(parameterTypes: list, world, agentID, substitutions: list):
    return any([anyParameterMissing(paramType, world, agentID, substitutions) if type(paramType) is list else parameterMissing(paramType, world, agentID, substitutions) for paramType in parameterTypes])

def parameterMissing(parameterType, world, agentID, substitutions: list):
    if any([substitution[0] == None or issubclass(parameterType, substitution[0]) for substitution in substitutions]):
        return False

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