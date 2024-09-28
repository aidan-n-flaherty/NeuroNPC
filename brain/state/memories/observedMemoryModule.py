from brain.state.memories.observedMemory import ObservedMemory
import LLM.generator.generator as generator
import LLM.formatter.formatter as formatter
from engine.types.statement import Statement
from llama_cpp import LlamaGrammar

# A class that stores actions witnessed
class ObservedMemoryModule:
    def __init__(self) -> None:
        self._shortTermMemories = []
        self._longTermMemories = []
        self._perceptions = {}
    
    def getShortTermMemories(self) -> list[ObservedMemory]:
        return self._shortTermMemories
    
    def getLongTermMemories(self) -> list[ObservedMemory]:
        return self._longTermMemories
    
    def getAllMemories(self) -> list[ObservedMemory]:
        arr = [memory for memory in self._longTermMemories]
        arr.extend(self._shortTermMemories)

        return arr

    def offload(self):
        self.offloaded = self._shortTermMemories[:-3]

        self._longTermMemories.extend(self._shortTermMemories[:-3])
        self._shortTermMemories = self._shortTermMemories[-3:]

        self._perceptions = {k: v for k, v in self._perceptions.items() if k in [memory.getAgentID() for memory in self._shortTermMemories]}

        return self.offloaded

    def getPerceptionStr(self, agentID: int):
        return self._perceptions[agentID] if agentID in self._perceptions else None

    def addMemory(self, memory: ObservedMemory, perceptionModule):
        if memory.getAgentID() not in self._perceptions:
            self._perceptions[memory.getAgentID()] = perceptionModule.getPerceptionStr(memory.getAgentID())
        
        self._shortTermMemories.append(memory)
    
    def remember(self, query: str) -> str:
        queryEmbedding = generator.encode(formatter.removeStopWords(query))

        for elem in self._memories:
            print(formatter.removeStopWords(elem.getDescription()), generator.encodedSimilarity(elem.getEmbedding(), queryEmbedding))

        topMemories = sorted(self._memories, key=lambda elem: generator.encodedSimilarity(elem.getEmbedding(), queryEmbedding))[-5:]

        with open('brain/state/memories/prompts/remember.txt', 'r') as prompt, open('brain/state/memories/prompts/remember.gnbf', 'r') as grammar:
            prompt = prompt.read().format(query=query, memories="\n".join([ "{}".format(elem.getIdentifier()) for elem in topMemories]))
            grammar = grammar.read().format(grammar=Statement.getGrammar())
            print(prompt)
            print(grammar)
            result = generator.create_deterministic_completion(formatter.generatePrompt(prompt), grammar=LlamaGrammar.from_string(grammar, verbose=False))
            print(result)

            return result["choices"][0]["text"]
