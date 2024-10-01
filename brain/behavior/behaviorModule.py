from engine.actions.action import Action
from engine.classes.agent import Agent
from brain.behavior.policy import Policy
from engine.actions.actionType import ActionType
import engine.actions.actionManager as ActionManager
from brain.state.personality.personalityModule import PersonalityModule
from brain.state.perceptions.perceptionModule import PerceptionModule

class BehaviorModule:
    def __init__(self):
        self._conversingWith = None
        self._policies = set()

    def startConversingWith(self, agent: Agent):
        self._conversingWith = agent.getID()

    def isConversing(self):
        return not self._conversingWith is None
    
    def addPolicy(self, policy: Policy):
        self._policies.add(policy)

    def getPolicies(self):
        return self._policies
    
    def hasPolicy(self, policy: Policy):
        return policy in self._policies

    def getReaction(self, personalityModule: PersonalityModule, perceptionModule: PerceptionModule, agent: Agent, action: Action) -> Action:
        if agent is None or self._conversingWith == agent.getID():
            return Action(ActionType("recalculate"))
        
        if self.hasPolicy(Policy("self_preservation")) and ActionManager.isHostile(action.getType()):
            return Action(ActionType("attack"), [agent.getID()])

        

        return None