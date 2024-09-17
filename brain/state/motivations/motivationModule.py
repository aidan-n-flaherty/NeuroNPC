from llama_cpp import LlamaGrammar
import LLM.generator.generator as Generator
import LLM.formatter.formatter as Formatter
from brain.state.autocondenser.autoCondenser import AutoCondenser

from enum import Enum

class MotivationModule:
    def __init__(self, timestamp: int, shortTerm: str, longTerm: str):
        self._shortTermMotivations = AutoCondenser(timestamp, shortTerm, "brain/state/motivations/reevaluate.txt")
        self._longTermMotivations = AutoCondenser(timestamp, longTerm, "brain/state/motivations/reevaluate.txt")
    
    def addShortTerm(self, timestamp: int, motivation: str):
        self._shortTermMotivations.update(timestamp, motivation)
    
    def addLongTerm(self, timestamp: int, motivation: str):
        self._longTermMotivations.update(timestamp, motivation)

    def __str__(self):
        return '{{\nLONG_TERM: [{longTerm}],\nSHORT_TERM: [{shortTerm}]\n}}'.format(longTerm=', '.join(self._longTermMotivations.getNotes()), shortTerm=', '.join(self._shortTermMotivations.getNotes()))

