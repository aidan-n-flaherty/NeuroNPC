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
from brain.state.memories.evidence import Evidence
from engine.actions.action import Action
import engine.actions.actionManager as ActionManager
import LLM.formatter.formatter as Formatter
import LLM.generator.generator as Generator
import LLM.formatter.parser as Parser
import LLM.formatter.grammar as Grammar
import LLM.constants.constants as LLMConstants
import time

class NPC(Agent):
    def __init__(self, id: int, name: tuple[str, str], locationID: int, coordinates: tuple[float, float, float], inventory: list[int], backstory: str, longTermGoals: str, personalityModule: PersonalityModule) -> None:
        super().__init__(True, id, name, locationID, coordinates, inventory)
        self._backstory = backstory
        self._emotionModule = EmotionModule()
        self._reactionModule = ReactionModule()
        self._memoryModule = MemoryModule()
        self._personalityModule = personalityModule
        self._perceptionModule = PerceptionModule()
        self._motivationModule = MotivationModule(time.time(), None, longTermGoals)

    def getBackstory(self):
        return self._backstory

    def conversationStart(self, agentID: int):
        self._reactionModule.startConversingWith(agentID)
    
    def conversationEnd(self, agentID: int):
        self._reactionModule.endConversation(agentID)

    def react(self, world: World, agent: Agent, action: Action, timestamp: int, description: str, embedding) -> list[Action]:
        actionResponse = self._reactionModule.getReaction(agent, action)

        responseArr = None

        if actionResponse:
            if action:
                self._memoryModule.addMemory(self, world.getKnowledgeBase(), ObservedMemory(timestamp, agent.getID() if agent is not None else -1, action, "", description, action.getObservedDescription(world, agent.getID(), self.getID()) if agent is not None else "", embedding), self._perceptionModule)

            if actionResponse.getResponse():
                responseArr = [actionResponse.getResponse()]
            else:
                responseArr = self.recalculate(world)
        
        if responseArr:
            returnArr = [action for action in responseArr]

            for response in responseArr:
                responseDescription = response.getDescription(world, self.getID())
                selfDescription = response.getSelfDescription(world, self.getID())
                observedDescription = response.getObservedDescription(world, self.getID(), self.getID())
                self._memoryModule.addMemory(self, world.getKnowledgeBase(), ObservedMemory(timestamp, self.getID(), response, selfDescription, responseDescription, observedDescription, Generator.encode(Formatter.removeStopWords(responseDescription))), self._perceptionModule)

                if response.getName() in ActionManager.getMentalActionNames():
                    returnArr += self.processSelf(world, agent, response, timestamp, description, embedding)
                if response.getName() == "MOVE_TO_LOCATION":
                    self._locationID = response.getParameter(0)
                    returnArr += self.react(world, None, None, timestamp, description, embedding)

            return returnArr
        
        return []
    
    def processSelf(self, world: World, agent: Agent, action: Action, timestamp: int, description: str, embedding) -> list[Action]:
        if action.getName() == "RAISE_EMOTION":
            self._emotionModule.increaseEmotion(action.getParameter(0))
        elif action.getName() == "LOWER_EMOTION":
            self._emotionModule.decreaseEmotion(action.getParameter(0))
        elif action.getName() == "UPDATE_PERCEPTION_OF":
            self._perceptionModule.addNote(time.time(), action.getParameter(0), action.getParameter(1))
        elif action.getName() == "COLLECT_CLAIM":
            self._memoryModule.addEvidence(Evidence(timestamp, action.getParameter(0), action.getParameter(1)))
        elif action.getName() == "CHECK_CLAIM":
            response = Action("NONE", [self._memoryModule.check(world.getKnowledgeBase(), self._perceptionModule, action.getParameter(0), self._reactionModule.getConversingWith())], "You evaluate the statement as: {0}.", "You evaluate the statement as: {0}.")
            description = response.getDescription(world, self.getID())
            embedding = Generator.encode(Formatter.removeStopWords(description))
            return self.react(world, None, response, timestamp, description, embedding)
        elif action.getName() == "QUERY_MEMORY_DATABASE":
            response = Action("NONE", [self._memoryModule.query(self, action.getParameter(0))], "From your memories: {0}.", "From your memories: {0}.")
            description = response.getDescription(world, self.getID())
            embedding = Generator.encode(Formatter.removeStopWords(description))
            return self.react(world, None, response, timestamp, description, embedding)
        
        return []

    def recalculate(self, world: World) -> list[Action]:
        with open('brain/core/prompts/recalculate.txt', 'r') as prompt, open('brain/core/prompts/recalculate.gnbf', 'r') as grammar:
            prompt = prompt.read().format(\
                identifier=self.getIdentifier(),
                backstory=self._backstory, \
                narrator=LLMConstants.NARRATOR_NAME, \
                functionDescriptions="\n".join(["{}: {}".format(ActionManager.getFunctionStr(action), ActionManager.getDocumentation(action)) for action in ActionManager.getActionNames()]), \
                history=Formatter.formatHistory(self.getID(), self._memoryModule.getSummary(), self._memoryModule.getObserved()), \
                emotions=str(self._emotionModule), \
                functionList=", ".join(ActionManager.getActionNames()), \
                inventory='[{}]'.format(', '.join([world.getItem(itemID).getIdentifier() for itemID in self.getInventory()])), \
                agents='[{}]'.format(', '.join([world.getAgent(agentID).getIdentifier() for agentID in world.getInteractableAgents(self.getID())])), \
                objects='[{}]'.format(', '.join([world.getItem(itemID).getIdentifier() for itemID in world.getInteractableItems(self.getID())])), \
                currentLocation=world.getLocation(self.getLocationID()).getIdentifier(), \
                adjacentLocations='[{}]'.format(', '.join([world.getLocation(locationID).getIdentifier() for locationID in world.getAccessibleLocations(self.getID())])), \
                personality=str(self._personalityModule))
            
            grammar = grammar.read().format(\
                mainActionList=" | ".join([name.replace("_", "") for name in ActionManager.getMainActionNames()]), \
                actionList=" | ".join([name.replace("_", "") for name in ActionManager.getActionNames() if name not in ActionManager.getSingleActionNames()]), \
                singleActionList=" | ".join([name.replace("_", "") for name in ActionManager.getSingleActionNames()]), \
                functionGrammars="\n\n".join(['{} ::= {}'.format(action.name.replace("_", ""), Grammar.generateGrammar(action, world, self.getID())) for action in ActionManager.getActions()]))
            
            print(Formatter.generatePrompt(prompt))
            print(grammar)
            result = Generator.create_completion(Formatter.generatePrompt(prompt), grammar=LlamaGrammar.from_string(grammar, verbose=False))

            returnVal = Parser.parseFunctionList(result["choices"][0]["text"])

            return returnVal