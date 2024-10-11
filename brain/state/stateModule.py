from brain.planning.routine.actionResponse import NotificationResponse
from engine.stimuli.notification import Notification
from engine.classes.agent import Agent
from brain.state.beliefs.beliefModule import BeliefModule
from brain.state.emotions.emotionModule import EmotionModule
from brain.state.memories.summarizedMemoryModule import MemoryModule
from brain.state.perceptions.perceptionModule import PerceptionModule
from brain.state.personality.personalityModule import PersonalityModule

class StateModule:
    def __init__(self):
        self._personalityModule = PersonalityModule()
        self._beliefModule = BeliefModule()
        self._emotionModule = EmotionModule()
        self._memoryModule = MemoryModule()
        self._perceptionModule = PerceptionModule()
    
    def getPersonalityModule(self):
        return self._personalityModule
    
    def getBeliefModule(self):
        return self._beliefModule
    
    def getEmotionModule(self):
        return self._emotionModule
    
    def getMemoryModule(self):
        return self._memoryModule
    
    def getPerceptionModule(self):
        return self._perceptionModule