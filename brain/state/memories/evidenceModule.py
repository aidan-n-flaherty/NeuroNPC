from llama_cpp import LlamaGrammar
import LLM.generator.generator as Generator
import LLM.formatter.formatter as Formatter
from brain.state.memories.evidence import Evidence

from enum import Enum

class BeliefClassification(Enum):
    TRUE, FALSE, UNKNOWN = range(3)

class BeliefRanking(Enum):
    SUPPORTS, IRRELEVANT, CONTRADICTS = range(3)

class EvidenceModule:
    def __init__(self):
        self._evidenceArr = []

    def addEvidence(self, evidence: Evidence):
        self._evidenceArr.append(evidence)
    
    def getEvidence(self):
        return self._evidenceArr

    def believes(self, claim: str) -> BeliefClassification:
        claimEmbedding = Generator.encode(Formatter.removeStopWords(claim))
        topEvidence = sorted(self._evidenceArr, key=lambda elem: Generator.encodedSimilarity(elem.getEmbedding(), claimEmbedding))[-5:]

        with open('brain/state/memories/prompts/believe.txt', 'r') as prompt, open('brain/state/memories/prompts/believe.gnbf', 'r') as grammar:
            prompt = prompt.read().format(claim=claim, \
                evidence="\n".join([ "{}. {}".format(topEvidence.index(elem) + 1, elem.getIdentifier()) for elem in topEvidence]) if topEvidence else "There is no matching evidence.", \
                rankingCategories=", ".join([elem.name for elem in BeliefRanking]), resultCategories=", ".join([elem.name for elem in BeliefClassification]))
            grammar = grammar.read().format(statementList=" ".join(["\"Evidence \'{}\': \" statement".format(elem.getDescription()) for elem in topEvidence]), \
                statement=claim, \
                rankingCategories=" | ".join(["\"{}\"".format(elem.name) for elem in BeliefRanking]), \
                resultCategories=" | ".join(["\"{}\"".format(elem.name) for elem in BeliefClassification]))
            
            result = Generator.create_deterministic_completion(Formatter.generatePrompt(prompt, "I would categorize the evidence as the following:\n\n"), grammar=LlamaGrammar.from_string(grammar, verbose=False))
            returnVal = BeliefClassification[result["choices"][0]["text"].split(": ")[-1]]

            return returnVal



