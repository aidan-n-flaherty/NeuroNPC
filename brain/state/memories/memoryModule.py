from brain.state.memories.summarizedMemoryModule import SummarizedMemoryModule
from brain.state.memories.observedMemoryModule import ObservedMemoryModule
from brain.state.memories.observedMemory import ObservedMemory
from brain.state.memories.summarizedMemory import SummarizedMemory
from brain.state.memories.evidenceModule import EvidenceModule
from brain.state.memories.testimonyModule import TestimonyModule
from brain.state.memories.evidence import Evidence
import engine.actions.actionManager as ActionManager
import LLM.generator.generator as Generator
import LLM.formatter.formatter as Formatter
import LLM.parser.parser as Parser
from engine.types.statement import Statement
from engine.types.paragraph import Paragraph
from engine.actions.actionType import ActionType
import brain.constants.constants as Constants
import time
from llama_cpp import LlamaGrammar

class MemoryModule:
    def __init__(self) -> None:
        self._summarizedMemoryModule = SummarizedMemoryModule()
        self._observedMemoryModule = ObservedMemoryModule()
        self._evidenceModule = EvidenceModule()
        self._testimonyModule = TestimonyModule()

    def getObserved(self) -> ObservedMemoryModule:
        return self._observedMemoryModule

    def getHistory(self) -> list[ObservedMemory]:
        return self._observedMemoryModule.getShortTermMemories()

    def getSummary(self):
        return self._summarizedMemoryModule.mostRecentMemory()
    
    def addEvidence(self, evidence: Evidence):
        self._evidenceModule.addEvidence(evidence)
    
    def addTestimony(self, knowledgeBase, claim: str, sourceID: int, degree: int) -> int:
        return self._testimonyModule.addClaim(knowledgeBase, claim, sourceID, degree)

    def addMemory(self, agent, knowledgeBase, memory: ObservedMemory, perceptionModule):
        self._observedMemoryModule.addMemory(memory, perceptionModule)

        characters = ""

        for memory in self._observedMemoryModule.getShortTermMemories():
            characters += memory.getDescription()
        
        if Generator.tokenCount(characters) > Constants.HISTORY_LIMIT:
            """statements = self._observedMemoryModule.getShortTermMemories()
            with open('brain/state/memories/prompts/collectTestimony.txt', 'r') as prompt, open('brain/state/memories/prompts/collectTestimony.gnbf', 'r') as grammar:
                prompt = prompt.read().format(identifier=agent.getIdentifier(), backstory=agent.getBackstory(), history=Formatter.formatHistory(agent.getID(), self._summarizedMemoryModule.mostRecentMemory(), self._observedMemoryModule), narrator=Formatter.getNarratorName(), model=Formatter.getModelName())
                grammar = grammar.read().format(agentIDs='({})'.format(' | '.join(['"{}"'.format(memory.getAgentID()) for memory in statements])), statement=Paragraph.getGrammar())
                print(prompt)
                print(grammar)
                result = Generator.create_deterministic_completion(Formatter.generatePrompt(prompt), grammar=grammar)

                for action in Parser.parseFunctionList(result["choices"][0]["text"]):
                    if action.getType() == ActionType("pass"):
                        break
                    elif action.getType() == ActionType("collect_claim"):
                        self.addTestimony(knowledgeBase, action.getParameter(1), action.getParameter(0), 1)
                    elif action.getType() == ActionType("collect_evidence"):
                        self.addEvidence(Evidence(time.time(), agent.getID(), action.getParameter(0)))
                
                print(self._testimonyModule._testimonyArr)"""
            
            self._summarizedMemoryModule.addMemory(SummarizedMemory(agent, self._summarizedMemoryModule.mostRecentMemory(), self._observedMemoryModule))
            offloaded = self._observedMemoryModule.offload()
            #statements = list(filter(lambda memory: memory.getAction().getType() == "SAY" and memory.getAgentID() != agent.getID(), offloaded))
    
    def extract(self, world) -> str:
        observedMemories = [memory for memory in self._observedMemoryModule.getAllMemories() if memory.getAction().getType() == ActionType("say")][-3:]

        with open('brain/state/memories/prompts/extract.txt', 'r') as prompt:
            prompt = prompt.read().format(conversation="\n".join(['{}: {}'.format(world.getAgent(memory.getAgentID()).getIdentifier(), memory.getAction().getParameter(0)) for memory in observedMemories]), claim=observedMemories[-1].getAction().getParameter(0))
            result = Generator.create_deterministic_completion(Formatter.generatePrompt(prompt))
            print(prompt)
            print(result["choices"][0]["text"])

            return result["choices"][0]["text"]
        
    def query(self, agent, query: str) -> str:
        queryEmbedding = Generator.encode(Formatter.removeStopWords(query))

        topSummarizedMemories = sorted(self._summarizedMemoryModule.getAllMemories(), key=lambda elem: Generator.encodedSimilarity(elem.getEmbedding(), queryEmbedding))[-3:]

        topObservedMemories = sorted([memory for memory in self._observedMemoryModule.getLongTermMemories() if memory.getAction().getType() not in ActionManager.getMentalActions()], key=lambda elem: Generator.encodedSimilarity(elem.getEmbedding(), queryEmbedding))[-3:]

        topEvidence = sorted(self._evidenceModule.getEvidence(), key=lambda elem: Generator.encodedSimilarity(elem.getEmbedding(), queryEmbedding))[-3:]

        with open('brain/state/memories/prompts/remember.txt', 'r') as prompt, open('brain/state/memories/prompts/remember.gnbf', 'r') as grammar:
            prompt = prompt.read().format(identifier=agent.getIdentifier(), query=query, summarizedMemories=", ".join(['"{}"'.format(elem.getIdentifier()) for elem in topSummarizedMemories]), observedMemories=", ".join(['"{}"'.format(elem.getIdentifier()) for elem in topObservedMemories]), evidence=", ".join(['"{}"'.format(elem.getIdentifier()) for elem in topEvidence]))
            grammar = grammar.read().format(grammar=Statement.getGrammar())
            print(prompt)
            print(grammar)
            result = Generator.create_deterministic_completion(Formatter.generatePrompt(prompt), grammar=grammar)
            print(result)

            return result["choices"][0]["text"]

    def check(self, knowledgeBase, perceptionModule, claim: str, sourceID: int) -> str:
        assertion = knowledgeBase.getClaim(claim, sourceID, 2)

        return self._testimonyModule.believability(knowledgeBase, perceptionModule, assertion)