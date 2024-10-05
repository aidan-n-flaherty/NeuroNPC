from llama_cpp import LlamaGrammar

from engine.classes.agent import Agent
from engine.core.world import World
from brain.state.emotions.emotionModule import EmotionModule
from brain.planning.routine.reactionModule import ReactionModule
from brain.state.memories.memoryModule import MemoryModule
from brain.state.memories.observedMemory import ObservedMemory
from brain.state.personality.personalityModule import PersonalityModule
from brain.state.perceptions.perceptionModule import PerceptionModule
from brain.state.motivations.motivationModule import MotivationModule
from brain.behavior.behaviorModule import BehaviorModule
from brain.state.memories.evidence import Evidence
from engine.actions.action import Action
from engine.actions.actionType import ActionType
import engine.actions.actionManager as ActionManager
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
        self._reactionModule = ReactionModule()
        self._behaviorModule = BehaviorModule()
        self._memoryModule = MemoryModule()
        self._personalityModule = personalityModule
        self._perceptionModule = PerceptionModule()
        self._motivationModule = MotivationModule(time.time(), None, longTermGoals)

    def getBackstory(self):
        return self._backstory

    def conversationStart(self, agentID: int):
        self._behaviorModule.startConversingWith(agentID)
    
    def conversationEnd(self, agentID: int):
        self._behaviorModule.endConversation(agentID)

    def react(self, world: World, agent: Agent, action: Action, timestamp: int, description: str, embedding) -> list[Action]:
        response = self._behaviorModule.getReaction(self._personalityModule, self._perceptionModule, agent, action)

        responseArr = None

        if response:
            if action:
                memory = ObservedMemory(timestamp, agent.getID() if agent is not None else -1, action, "", description, action.getObservedDescription(world, agent.getID(), self.getID()) if agent is not None else action.getObservedDescription(world, -1, self.getID()), embedding)
                self._memoryModule.addMemory(self, world.getKnowledgeBase(), memory, self._perceptionModule)

                if action.getType() == ActionType("say"):
                    classification = Generator.classify("A: " + action.getParameter(0), ['claim', 'desire', 'speculation', 'question', 'rhetorical question', 'conditional', 'sarcasm', 'joke', 'threat', 'suggestion', 'promise', 'small talk', 'other'])
                    print(classification)
                    if 'claim' == classification:
                        extracted = self._memoryModule.extract(world)
                        id = self._memoryModule.addTestimony(world.getKnowledgeBase(), extracted, agent.getID(), 2)
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
                self._memoryModule.addMemory(self, world.getKnowledgeBase(), ObservedMemory(timestamp, self.getID(), response, selfDescription, responseDescription, observedDescription, Generator.encode(Formatter.removeStopWords(responseDescription))), self._perceptionModule)

                if response.getType() in ActionManager.getMentalActions():
                    returnArr += self.processSelf(world, agent, response, timestamp, description, embedding)

                if response.getType() == ActionType("move_to_location"):
                    self._locationID = response.getParameter(0)
                    returnArr += self.react(world, None, None, timestamp, description, embedding)

            return returnArr
        
        return []
    
    def processSelf(self, world: World, agent: Agent, action: Action, timestamp: int, description: str, embedding) -> list[Action]:
        if action.getType() == ActionType("raise_emotion"):
            self._emotionModule.increaseEmotion(action.getParameter(0))
        elif action.getType() == ActionType("lower_emotion"):
            self._emotionModule.decreaseEmotion(action.getParameter(0))
        elif action.getType() == ActionType("update_perception_of"):
            self._perceptionModule.addNote(time.time(), action.getParameter(0), action.getParameter(1))
        elif action.getType() == ActionType("check_claim"):
            response = Action("NONE", [self._memoryModule.check(world.getKnowledgeBase(), self._perceptionModule, action.getParameter(0), self._reactionModule.getConversingWith())], "You evaluate the statement as: {0}.", "You evaluate the statement as: {0}.")
            description = response.getDescription(world, self.getID())
            embedding = Generator.encode(Formatter.removeStopWords(description))
            return self.react(world, None, response, timestamp, description, embedding)
        elif action.getType() == ActionType("query_memory_database"):
            response = Action(ActionType("NONE"), [self._memoryModule.query(self, action.getParameter(0))], "From your memories: {0}.", "From your memories: {0}.")
            description = response.getDescription(world, self.getID())
            embedding = Generator.encode(Formatter.removeStopWords(description))
            return self.react(world, None, response, timestamp, description, embedding)
        
        return []

    def recalculate(self, world: World) -> list[Action]:
        with open('brain/core/prompts/recalculate.txt', 'r') as prompt, open('brain/core/prompts/recalculate.gnbf', 'r') as grammar:
            prompt = prompt.read().format(\
                identifier=self.getIdentifier() + " (name: " + self.getName() + ")",
                backstory=self._backstory, \
                narrator=LLMConstants.NARRATOR_NAME, \
                functionDescriptions="\n".join(["{}: {}".format(ActionManager.getFunctionStr(action), ActionManager.getDocumentation(action)) for action in ActionManager.getActions()]), \
                history=Formatter.formatHistory(self.getID(), self._memoryModule.getSummary(), self._memoryModule.getObserved()), \
                emotions=str(self._emotionModule), \
                functionList=", ".join(ActionManager.getActions()), \
                inventory='[{}]'.format(', '.join([world.getItem(itemID).getIdentifier() for itemID in self.getInventory()])), \
                agents='[{}]'.format(', '.join([world.getAgent(agentID).getIdentifier() for agentID in world.getInteractableAgents(self.getID())])), \
                objects='[{}]'.format(', '.join([world.getItem(itemID).getIdentifier() for itemID in world.getInteractableItems(self.getID())])), \
                currentLocation=world.getLocation(self.getLocationID()).getIdentifier(), \
                adjacentLocations='[{}]'.format(', '.join([world.getLocation(locationID).getIdentifier() for locationID in world.getAccessibleLocations(self.getID())])), \
                personality=str(self._personalityModule))
            
            grammar = grammar.read().format(\
                mainActionList=" | ".join([action.replace("_", "") for action in ActionManager.getMainActions() if not Grammar.grammarMissing(action, world, self.getID())]), \
                actionList=" | ".join([action.replace("_", "") for action in ActionManager.getActions() if action not in ActionManager.getSingleActions() and not Grammar.grammarMissing(action, world, self.getID())]), \
                singleActionList=" | ".join([action.replace("_", "") for action in ActionManager.getSingleActions() if not Grammar.grammarMissing(action, world, self.getID())]), \
                functionGrammars="\n\n".join(['{} ::= {}'.format(action.replace("_", ""), Grammar.generateGrammar(action, world, self.getID())) for action in ActionManager.getActions()]))
            
            print(Formatter.generatePrompt(prompt))
            result = Generator.create_completion(Formatter.generatePrompt(prompt), grammar=grammar)

            returnVal = Parser.parseFunctionList(result["choices"][0]["text"])

            return returnVal