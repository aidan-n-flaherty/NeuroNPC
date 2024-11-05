from llama_cpp import LlamaGrammar

from engine.classes.agent import Agent
from engine.core.world import World
from brain.state.emotions.emotionModule import EmotionModule
from brain.state.memories.memoryModule import MemoryModule
from brain.state.memories.observedMemory import ObservedMemory
from brain.state.personality.personalityModule import PersonalityModule
from brain.state.perceptions.perceptionModule import PerceptionModule
from brain.state.motivations.motivationModule import MotivationModule
from brain.behavior.behaviorModule import BehaviorModule
from brain.state.memories.evidence import Evidence
from engine.stimuli.notification import Notification
from engine.stimuli.actionType import ActionType
import engine.stimuli.notificationModule as NotificationModule
import LLM.formatter.formatter as Formatter
import LLM.generator.generator as Generator
import LLM.parser.parser as Parser
import LLM.formatter.grammar as Grammar
import LLM.constants.constants as LLMConstants
import time

class NPC(Agent):
    def __init__(self, id: int, name: tuple[str, str], locationID: int, coordinates: tuple[float, float, float], inventory: list[int], backstory: str, longTermGoals: str, personalityModule: PersonalityModule) -> None:
        super().__init__(True, id, name, locationID, coordinates, inventory)
        self._backstory = backstory
        self._emotionModule = EmotionModule()
        self._behaviorModule = BehaviorModule()
        self._memoryModule = MemoryModule(id)
        self._personalityModule = personalityModule
        self._perceptionModule = PerceptionModule()
        self._motivationModule = MotivationModule(time.time(), None, longTermGoals)
    
    def getBackstory(self):
        return self._backstory

    def conversationStart(self, agent: Agent):
        self._behaviorModule.startConversingWith(agent)
        
        if isinstance(agent, NPC):
            agent._behaviorModule.startConversingWith(self)
    
    def conversationEnd(self):
        self._behaviorModule.stopConversing()

    def shareInformation(self, npc: 'NPC'):
        self._perceptionModule.exchange(npc._perceptionModule)

    def react(self, world: World, agent: Agent, notification: Notification, timestamp: int, description: str, embedding) -> list[Notification]:
        response = self._behaviorModule.getReaction(self, self._personalityModule, self._perceptionModule, agent, notification)

        responseArr = None

        if response:
            if notification:
                if agent:
                    self.conversationStart(agent)
                    
                memory = ObservedMemory(timestamp, agent.getID() if agent is not None else -1, notification, "", description, notification.getObservedDescription(world, agent.getID(), self.getID()) if agent is not None else notification.getObservedDescription(world, -1, self.getID()), embedding)
                self._memoryModule.addMemory(self, world.getKnowledgeBase(), memory, self._perceptionModule)

                if notification.getType() == ActionType("say"):
                    classification = Generator.classify("A: " + notification.getParameter(0), ['claim', 'desire', 'speculation', 'question', 'rhetorical question', 'conditional', 'sarcasm', 'joke', 'threat', 'suggestion', 'promise', 'small talk', 'other'])
                    print(classification)
                    if 'claim' == classification:
                        extracted = self._memoryModule.extract(world)
                        id = self._memoryModule.addTestimony(world.getKnowledgeBase(), extracted, agent.getID(), 2)
                        self._perceptionModule.setTrustworthiness(time.time(), agent.getID(), self._memoryModule.getSelfConsistency(world.getKnowledgeBase(), agent.getID()))
                        memory.setNote(self._memoryModule.check(world.getKnowledgeBase(), self._perceptionModule, world.getKnowledgeBase().getExistingClaim(id).getClaim(), agent.getID()))

            if response.getType() == ActionType("recalculate"):
                responseArr = self.recalculate(world)
            else:
                responseArr = [response]
        
        if responseArr:
            returnArr = [action for action in responseArr]

            for response in responseArr:
                responseDescription = response.getDescription(world, self.getID())
                selfDescription = response.getSelfDescription(world, self.getID())
                observedDescription = response.getObservedDescription(world, self.getID(), self.getID())
                
                if not NotificationModule.isEphemeral(response.getType()):
                    self._memoryModule.addMemory(self, world.getKnowledgeBase(), ObservedMemory(timestamp, self.getID(), response, selfDescription, responseDescription, observedDescription, Generator.encode(Formatter.removeStopWords(responseDescription))), self._perceptionModule)

                if response.getType() in NotificationModule.getMentalActions():
                    returnArr += self.processSelf(world, agent, response, timestamp, description, embedding)

                if response.getType() == ActionType("move_to_location"):
                    self._locationID = response.getParameter(0)
                    returnArr += self.react(world, None, None, timestamp, description, embedding)

            return returnArr
        
        return []
    
    def processSelf(self, world: World, agent: Agent, notification: Notification, timestamp: int, description: str, embedding) -> list[Notification]:
        if notification.getType() == ActionType("end_conversation"):
            self._behaviorModule.stopConversing()
        elif notification.getType() == ActionType("raise_emotion"):
            self._emotionModule.increaseEmotion(notification.getParameter(0))
        elif notification.getType() == ActionType("lower_emotion"):
            self._emotionModule.decreaseEmotion(notification.getParameter(0))
        elif notification.getType() == ActionType("report"):
            self._perceptionModule.addNote(time.time(), notification.getParameter(0), notification.getParameter(1))
        elif notification.getType() == ActionType("update_relationship"):
            self._perceptionModule.updateRelation(time.time(), notification.getParameter(0), notification.getParameter(1))
        elif notification.getType() == ActionType("add_policy"):
            self._behaviorModule.addPolicy(self, notification.getParameter(0), world)
        elif notification.getType() == ActionType("schedule_behavior"):
            self._behaviorModule.createScheduleException(self, notification.getParameter(0), world)
        elif notification.getType() == ActionType("check_claim"):
            response = Notification("NONE", [self._memoryModule.check(world.getKnowledgeBase(), self._perceptionModule, notification.getParameter(0), self._reactionModule.getConversingWith())], "You evaluate the statement as: {0}.", "You evaluate the statement as: {0}.")
            description = response.getDescription(world, self.getID())
            embedding = Generator.encode(Formatter.removeStopWords(description))
            return self.react(world, None, response, timestamp, description, embedding)
        elif notification.getType() == ActionType("query_memory_database"):
            response = Notification(ActionType("NONE"), [self._memoryModule.query(self, notification.getParameter(0))], "From your memories: {0}.", "From your memories: {0}.")
            description = response.getDescription(world, self.getID())
            embedding = Generator.encode(Formatter.removeStopWords(description))
            return self.react(world, None, response, timestamp, description, embedding)
        
        return []

    def recalculate(self, world: World) -> list[Notification]:
        with open('brain/core/prompts/recalculate.txt', 'r') as prompt, open('brain/core/prompts/recalculate.gnbf', 'r') as grammar:
            prompt = prompt.read().format(\
                identifier=self.getIdentifier() + " (name: " + self.getName() + ")",
                backstory=self._backstory, \
                narrator=LLMConstants.NARRATOR_NAME, \
                physicalFunctionDescriptions="\n".join(["{}: {}".format(NotificationModule.getFunctionStr(action), NotificationModule.getDocumentation(action)) for action in NotificationModule.getNonMentalActions()]), \
                mentalFunctionDescriptions="\n".join(["{}: {}".format(NotificationModule.getFunctionStr(action), NotificationModule.getDocumentation(action)) for action in NotificationModule.getMentalActions()]), \
                history=Formatter.formatHistory(self.getID(), self._memoryModule.getSummary(), self._memoryModule.getObserved()), \
                emotions=str(self._emotionModule), \
                functionList=", ".join(NotificationModule.getActions()), \
                inventory='[{}]'.format(', '.join([world.getItem(itemID).getIdentifier() for itemID in self.getInventory()])), \
                jobs= '{}'.format(self.getJob().getIdentifier()),
                agents=', '.join([self._perceptionModule.getPerceptionStr(agentID) for agentID in world.getInteractableAgents(self.getID())]) if world.getInteractableAgents(self.getID()) else "There is no one in your current location. If you were interacting with a user previously, you must return to your previous location to interact with them again.", \
                objects='[{}]'.format(', '.join([world.getItem(itemID).getIdentifier() for itemID in world.getInteractableItems(self.getID())])), \
                currentLocation=world.getLocation(self.getLocationID()).getIdentifier(), \
                adjacentLocations='[{}]'.format(', '.join([world.getLocation(locationID).getIdentifier() for locationID in world.getAccessibleLocations(self.getID())])), \
                personality=str(self._personalityModule))
            
            grammar = grammar.read().format(\
                mainActionList=" | ".join([action.replace("_", "") for action in NotificationModule.getMainActions() if not Grammar.grammarMissing(action, world, self.getID())]), \
                actionList=" | ".join([action.replace("_", "") for action in NotificationModule.getActions() if action not in NotificationModule.getSingleActions() and not Grammar.grammarMissing(action, world, self.getID())]), \
                singleActionList=" | ".join([action.replace("_", "") for action in NotificationModule.getSingleActions() if not Grammar.grammarMissing(action, world, self.getID())]), \
                functionGrammars="\n\n".join(['{} ::= {}'.format(action.replace("_", ""), Grammar.generateGrammar(action, world, self.getID())) for action in NotificationModule.getActions()]))
            
            print(Formatter.generatePrompt(prompt))
            result = Generator.create_completion(Formatter.generatePrompt(prompt), grammar=grammar)
            print(result["choices"][0]["text"])

            returnVal = Parser.parseFunctionList(result["choices"][0]["text"])

            return returnVal