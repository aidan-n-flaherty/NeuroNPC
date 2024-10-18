from engine.stimuli.notification import Notification
from engine.classes.agent import Agent
from engine.types.agentID import AgentID
from engine.types.itemID import ItemID
from engine.types.time import Time
from engine.stimuli.actionType import ActionType
import engine.stimuli.notificationModule as NotificationModule
from brain.state.personality.personalityModule import PersonalityModule
from brain.state.perceptions.perceptionModule import PerceptionModule
import LLM.constants.constants as LLMConstants
import LLM.formatter.grammar as Grammar
import LLM.formatter.formatter as Formatter
import LLM.generator.generator as Generator
import LLM.parser.parser as Parser
from brain.behavior.policy import Policy
from brain.behavior.scheduledBehavior import ScheduledBehavior
import re

class BehaviorModule:
    def __init__(self):
        self._conversingWith = None
        self._policies = set()
        self._scheduledBehaviors = set()

    def startConversingWith(self, agent: Agent):
        self._conversingWith = agent.getID()

    def isConversing(self):
        return not self._conversingWith is None
    
    def getReplacements(self):
        return [(AgentID, "self"), (AgentID, "caller"), (ItemID, "caller"), (None, "_")]
    
    def createSchedule(self, agent, world):
        with open('brain/behavior/prompts/createSchedule.txt', 'r') as prompt, open('brain/behavior/prompts/createSchedule.gnbf', 'r') as grammar:
            prompt = prompt.read().format(
                role=agent.getBackstory(),
                identifier=agent.getIdentifier() + " (name: " + agent.getName() + ")",
                narrator=LLMConstants.NARRATOR_NAME,
                actionDescriptions="\n".join(["{}: {}".format(NotificationModule.getFunctionStr(action), NotificationModule.getDocumentation(action)) for action in NotificationModule.getMainActions()]))
            
            grammar = grammar.read().format(
                time=Time.getGrammar(),
                actionList=" | ".join([action.replace("_", "") for action in NotificationModule.getMainActions() if not Grammar.grammarMissing(action, world, agent.getID())]),
                functionGrammars="\n\n".join(['{} ::= {}'.format(func.replace("_", ""), Grammar.generateGrammar(func, world, agent.getID())) for func in NotificationModule.getNotifications()]))
            print(Formatter.generatePrompt(prompt))
            
            result = Generator.create_deterministic_completion(Formatter.generatePrompt(prompt), grammar=grammar)
            print(result["choices"][0]["text"])
            for policyStr in result["choices"][0]["text"].split("\n"):
                time = re.split(r'[: ]', re.search(r'time\(([^\(\)]*)\)', policyStr).group(1))
                time = int(time[0]) * 60 + int(time[1]) + (12 * 60 if time[2] == 'PM' else 0)

                action = Parser.parseFunctionCall(policyStr.split(" then ")[1])
                self._scheduledBehaviors.add(ScheduledBehavior(time, action.getType(), action.getParameters(), True))

    def createScheduleException(self, agent, exception: str, world):
        with open('brain/behavior/prompts/createScheduleException.txt', 'r') as prompt, open('brain/behavior/prompts/createScheduleException.gnbf', 'r') as grammar:
            prompt = prompt.read().format(
                role=agent.getBackstory(),
                exception=exception,
                identifier=agent.getIdentifier() + " (name: " + agent.getName() + ")",
                narrator=LLMConstants.NARRATOR_NAME,
                actionDescriptions="\n".join(["{}: {}".format(NotificationModule.getFunctionStr(action), NotificationModule.getDocumentation(action)) for action in NotificationModule.getMainActions()]))
            
            grammar = grammar.read().format(
                time=Time.getGrammar(),
                actionList=" | ".join([action.replace("_", "") for action in NotificationModule.getMainActions() if not Grammar.grammarMissing(action, world, agent.getID())]),
                functionGrammars="\n\n".join(['{} ::= {}'.format(func.replace("_", ""), Grammar.generateGrammar(func, world, agent.getID())) for func in NotificationModule.getNotifications()]))
            print(Formatter.generatePrompt(prompt))
            
            result = Generator.create_deterministic_completion(Formatter.generatePrompt(prompt), grammar=grammar)
            print(result["choices"][0]["text"])
            for policyStr in result["choices"][0]["text"].split("\n"):
                exp = re.search(r'time\(([^\(\),]*), ([^\(\),]*)\)', policyStr)
                day = int(exp.group(1)) * 60 * 60
                time = re.split(r'[: ]', exp.group(2))
                time = int(time[0]) * 60 + int(time[1]) + (12 * 60 if time[2] == 'PM' else 0) + 24 * 60 * 60 * day

                print(policyStr.split(" then ")[1][1:-1].replace(', ', '\n'))
                actions = Parser.parseFunctionList(policyStr.split(" then ")[1][1:-1].replace('), ', ')\n'))
                for action in actions:
                    self._scheduledBehaviors.add(ScheduledBehavior(time, action.getType(), action.getParameters(), False))

    def addPolicy(self, agent, policy: str, world):
        with open('brain/behavior/prompts/createPolicy.txt', 'r') as prompt, open('brain/behavior/prompts/createPolicy.gnbf', 'r') as grammar:
            prompt = prompt.read().format(\
                policy=policy,
                identifier=agent.getIdentifier() + " (name: " + agent.getName() + ")",
                narrator=LLMConstants.NARRATOR_NAME, \
                actionDescriptions="\n".join(["{}: {}".format(NotificationModule.getFunctionStr(action), NotificationModule.getDocumentation(action)) for action in NotificationModule.getActions()]), \
                eventDescriptions="\n".join(["{}: {}".format(NotificationModule.getFunctionStr(event), NotificationModule.getDocumentation(event)) for event in NotificationModule.getEvents()]))
            
            grammar = grammar.read().format(\
                eventList=" | ".join([event.replace("_", "") for event in NotificationModule.getEvents() if not Grammar.grammarMissing(event, world, agent.getID(), self.getReplacements())]), \
                actionList=" | ".join([action.replace("_", "") for action in NotificationModule.getActions() if not Grammar.grammarMissing(action, world, agent.getID(), self.getReplacements())]), \
                actionEventList=" | ".join([action.replace("_", "") + "Event" for action in NotificationModule.getActions() if not Grammar.grammarMissing(action, world, agent.getID(), self.getReplacements())]), \
                functionGrammars="\n\n".join(['{} ::= {}'.format(func.replace("_", ""), Grammar.generateGrammar(func, world, agent.getID(), [pair for pair in self.getReplacements() if pair[1] != '_'])) for func in NotificationModule.getNotifications()]), \
                functionEventGrammars="\n\n".join(['{} ::= {}'.format(func.replace("_", "") + "Event", Grammar.generateGrammar(func, world, agent.getID(), self.getReplacements())) for func in NotificationModule.getNotifications()]))
            
            result = Generator.create_deterministic_completion(Formatter.generatePrompt(prompt), grammar=grammar)

            for policyStr in result["choices"][0]["text"].split("\n"):
                print(policyStr)
                self._policies.add(policyStr)

    def getPolicies(self):
        return self._policies

    def getReaction(self, selfAgent: Agent, personalityModule: PersonalityModule, perceptionModule: PerceptionModule, agent: Agent, notification: Notification) -> Notification:
        if agent is None:
            return Notification(ActionType("recalculate"))
        
        for policyStr in self._policies:
            policyStr = policyStr.replace("self", str(selfAgent.getID())).replace("caller", str(agent.getID()))
            reactions = Parser.parseReactionList(policyStr)

            policy = Policy(reactions[0][0].getType(), reactions[0][0].getParameters(), reactions[0][1].getType(), reactions[0][1].getParameters(), "")

            if policy.matches(notification):
                return Notification(policy.getResponseType(), policy.getResponseParameters(), policyStr[3:].split(" then ")[1], NotificationModule.getDescription(reactions[0][1].getType()))
    
        if agent is None or self._conversingWith == agent.getID():
            return Notification(ActionType("recalculate"))

        return None
    
    def getScheduledActions(self, time: int):
        actions = []

        for scheduledBehavior in self._scheduledBehaviors:
            if scheduledBehavior.getTime() <= time and not scheduledBehavior.getActivated():
                action = Notification(ActionType(scheduledBehavior.getActionType(), scheduledBehavior.getActionParameters()))
                scheduledBehavior.activate()

                actions.append(action)
        
        return actions