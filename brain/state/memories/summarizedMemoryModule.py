from brain.state.memories.summarizedMemory import SummarizedMemory
import LLM.generator.generator as generator
import LLM.formatter.formatter as formatter
from engine.types.statement import Statement
from llama_cpp import LlamaGrammar

class SummarizedMemoryModule:
    def __init__(self) -> None:
        self._memories = []

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
