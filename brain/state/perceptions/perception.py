from enum import Enum
import LLM.formatter.formatter as Formatter
import LLM.generator.generator as Generator
import brain.constants.constants as Constants
from engine.enums.degree import Degree
from engine.enums.relation import Relation

class Perception:
    def __init__(self, timestamp: int, agentID: int, note="", trustworthiness=Degree.NEUTRAL, relation=Relation.STRANGER) -> None:
        self._timestamp = timestamp
        self._agentID = agentID
        self._privateNotes = [note]
        self._externalNotes = []
        self._trustworthiness = trustworthiness
        self._relation = relation

    def getTrustworthiness(self) -> Degree:
        return self._trustworthiness
    
    def updateTrustworthiness(self, timestamp: int, trustworthiness: Degree):
        self._timestamp = timestamp
        self._trustworthiness = trustworthiness
    
    def updateRelation(self, timestamp: int, relation: Relation):
        self._timestamp = timestamp
        self._relation = relation

    def updateNotes(self, timestamp: int, note: str) -> None:
        self._timestamp = timestamp

        if note:
            self._privateNotes.append(note)

            if sum([len(n) for n in self._privateNotes]) > Constants.MENTAL_NOTE_LIMIT:
                with open('brain/state/perceptions/prompts/reevaluate.txt', 'r') as prompt:
                    prompt = prompt.read().format(internal_notes="\n".join(['"{}"'.format(note) for note in self._privateNotes]), external_notes="\n".join(['"{}"'.format(note) for note in self._externalNotes]))
                    print(prompt)
                    result = Generator.create_deterministic_completion(Formatter.generatePrompt(prompt))
                    print(result)

                    self._privateNotes = [result["choices"][0]["text"]]
                    self._externalNotes = []

    
    def getAgentID(self) -> int:
        return self._agentID
    
    def getIdentifier(self) -> str:
        return "Perception of person (id: {agentID}) from {time}: relationship: {relation}, trustworthiness: {trust}, personal notes [{internal}], external notes [{external}].".format(agentID=self._agentID, time=Formatter.timeToString(self._timestamp), relation=self._relation, trust=self._trustworthiness, internal=", ".join(['"{}"'.format(note) for note in self._privateNotes]), external=", ".join(['"{}"'.format(note) for note in self._externalNotes]))