"""Allows agents to modify default reactions to actions that they witness within their vicinity.

This module should aim to reduce the amount of LLM reasoning required by the NPC, while simultaneously allowing LLM reasoning to be requested under certain situations.
"""

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
    
    def getConversingWith(self):
        return self._conversingWith
    
    def addReaction(self, agent: Agent, action: Action, response: Action) -> None:
        for actionResponse in self._actionResponses:
            if actionResponse.getAction() == action:
                actionResponse.update(agent, action.getType(), response)
                
                return
        
        self._actionResponses.append(ActionResponse(agent, action, response))
    
    def getReaction(self, agent: Agent, action: Action) -> ActionResponse:
        if agent is None or self._conversingWith == agent.getID():
            return ActionResponse(None, action, None)

        for actionResponse in self._actionResponses:
            if action == actionResponse.getAction() and (actionResponse.getAgents() is None or agent in actionResponse.getAgents()):
                return actionResponse

        return None