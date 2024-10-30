from brain.state.memories.summarizedMemory import SummarizedMemory
import LLM.generator.generator as generator
import LLM.formatter.formatter as formatter
from engine.types.statement import Statement
from llama_cpp import LlamaGrammar

class SummarizedMemoryModule:
    def __init__(self, agentID: int) -> None:
        self._agentID = agentID
        self._memories = []
        self._externalMemories = []
    
    def exchange(self, summarizedMemoryModule: 'SummarizedMemoryModule'):
        self._externalMemories += [memory for memory in summarizedMemoryModule._memories if not any([memory.getDescription() == m.getDescription() for m in self._externalMemories])] + [memory for memory in summarizedMemoryModule._externalMemories if not any([memory.getDescription() == m.getDescription() for m in self._externalMemories])]
        self._externalMemories = [memory for memory in self._externalMemories if memory.getSourceID() != self._agentID]
        summarizedMemoryModule._externalMemories += [memory for memory in self._memories if not any([memory.getDescription() == m.getDescription() for m in summarizedMemoryModule._externalMemories])] + [memory for memory in self._externalMemories if not any([memory.getDescription() == m.getDescription() for m in summarizedMemoryModule._externalMemories])]
        summarizedMemoryModule._externalMemories = [memory for memory in summarizedMemoryModule._externalMemories if memory.getSourceID() != summarizedMemoryModule._agentID]

    def getAllMemories(self):
        return self._memories

    def mostRecentMemory(self):
        return self._memories[-1] if len(self._memories) else None

    def addMemory(self, memory: SummarizedMemory):
        self._memories.append(memory)
    
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
            result = generator.create_deterministic_completion(formatter.generatePrompt(prompt), grammar=grammar)
            print(result)

            return result["choices"][0]["text"]
