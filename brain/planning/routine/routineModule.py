from brain.planning.routine.actionResponse import ActionResponse
from engine.actions.action import Action
from engine.classes.agent import Agent

class ReactionModule:
    def __init__(self):
        self._actionResponses = []
        self._conversingWith = None

    def startConversingWith(self, agent: Agent):
        self._conversingWith = agent.getID()

    def isConversing(self):
        return not self._conversingWith is None
    
    def endConversation(self):
        self._conversingWith = None
    
    def addReaction(self, agent: Agent, action: Action, response: Action) -> None:
        for actionResponse in self._actionResponses:
            if actionResponse.getAction() == action:
                actionResponse.update(agent, action, response)
                
                return
        
        self._actionResponses.append(ActionResponse(agent, action, response))
    
    def getReaction(self, agent: Agent, action: Action) -> ActionResponse:
        if agent is None or self._conversingWith == agent.getID():
            return ActionResponse(None, action, None)

        for actionResponse in self._actionResponses:
            if action == actionResponse.getAction() and (actionResponse.getAgents() is None or agent in actionResponse.getAgents()):
                return actionResponse

        return None