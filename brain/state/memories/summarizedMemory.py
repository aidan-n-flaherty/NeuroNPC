import LLM.generator.generator as Generator
import LLM.formatter.formatter as Formatter
from brain.state.memories.observedMemoryModule import ObservedMemoryModule

class SummarizedMemory:
    def __init__(self, agent, previousMemory, observedMemoryModule: ObservedMemoryModule) -> None:
        self._sourceID = agent.getID()
        self._timeStart = min([memory.getTimestamp() for memory in observedMemoryModule.getShortTermMemories()])
        self._timeEnd = max([memory.getTimestamp() for memory in observedMemoryModule.getShortTermMemories()])
        self._agentsInvolved = list(set([memory.getAgentID() for memory in observedMemoryModule.getShortTermMemories()]))
        
        with open('brain/state/memories/prompts/summarize.txt', 'r') as prompt:
            prompt = prompt.read().format(identifier=agent.getIdentifier(), backstory=agent.getBackstory(), history=Formatter.formatHistory(agent.getID(), previousMemory, observedMemoryModule), narrator=Formatter.getNarratorName(), model=Formatter.getModelName())
            print(prompt)
            result = Generator.create_deterministic_completion(Formatter.generatePrompt(prompt))
            print(result)

            self._description = result["choices"][0]["text"]
            self._embedding = Generator.encode(Formatter.removeStopWords(self._description))

    def getSourceID(self) -> int:
        return self._sourceID

    def getDescription(self):
        return self._description
    
    def withinTimeRange(self, timeStart: int, timeEnd: int) -> bool:
        return self._timeStart < timeEnd and self._timeEnd > timeStart
    
    def referencesAgent(self, agentID: int) -> bool:
        return agentID in self._agentsInvolved
    
    def getEmbedding(self):
        return self._embedding
    
    def getIdentifier(self):
        return "<Memory from {time}: \"{description}\">".format(time=Formatter.timeToString(self._timeStart), description=self._description)