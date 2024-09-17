from engine.actions.actionManager import Action
import engine.actions.actionManager
from engine.classes.agent import Agent

class ActionResponse:
    def __init__(self, agent: Agent, action: Action, response: Action) -> None:
        self._agents = []
        self._action = None
        self._response = None

        self.update(agent, action, response)
    
    def update(self, agent: Agent, action: Action, response: Action) -> None:
        if self._agents == None:
            self._agents = []
        
        if agent:
            self._agents.append(agent)
        else:
            self._agents = None
        
        self._action = action
        self._response = response

    def getAction(self):
        return self._action

    def getResponse(self):
        return self._response
    
    def getAgents(self):
        return self._agents