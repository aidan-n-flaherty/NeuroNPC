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
        self._privateNotes = [note] if note else []
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
                    prompt = prompt.read().format(notes="\n".join(['"{}"'.format(note) for note in self._privateNotes]))
                    result = Generator.create_deterministic_completion(Formatter.generatePrompt(prompt))

                    self._privateNotes = [result["choices"][0]["text"]]
    
    def updateExternalNotes(self, timestamp: int, notes: list[str]) -> None:
        self._timestamp = timestamp

        if notes:
            self._externalNotes += notes

            if sum([len(n) for n in self._externalNotes]) > Constants.MENTAL_NOTE_LIMIT:
                with open('brain/state/perceptions/prompts/reevaluate.txt', 'r') as prompt:
                    prompt = prompt.read().format(notes="\n".join(['"{}"'.format(note) for note in self._externalNotes]))
                    result = Generator.create_deterministic_completion(Formatter.generatePrompt(prompt))

                    self._externalNotes = [result["choices"][0]["text"]]

    def getPrivateNotes(self) -> list:
        return self._privateNotes
    
    def getExternalNotes(self) -> list:
        return self._externalNotes

    def getTimestamp(self) -> int:
        return self._timestamp
    
    def getAgentID(self) -> int:
        return self._agentID
    
    def getIdentifier(self) -> str:
        return "<@{agentID}> -> last profile update: {time}, relationship: {relation}, trustworthiness: {trust}, personal notes [{internal}], external notes [{external}].".format(agentID=self._agentID, time=Formatter.timeToString(self._timestamp), relation=self._relation.name.lower().replace("_", ""), trust=self._trustworthiness.name.lower().replace("_", ""), internal=", ".join(['"{}"'.format(note) for note in self._privateNotes]), external=", ".join(['"{}"'.format(note) for note in self._externalNotes]))