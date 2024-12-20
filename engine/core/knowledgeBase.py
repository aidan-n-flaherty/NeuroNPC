import LLM.generator.generator as Generator
import LLM.formatter.formatter as Formatter
import LLM.parser.parser as Parser
from engine.classes.assertion import Assertion

from llama_cpp import LlamaGrammar
import numpy as np
import time
import re

class KnowledgeBase:
    def __init__(self):
        self._idCounter = 0
        self._assertions = {}
        self._strToAssertion = {}
        self._supportNetwork = {}

    def getSimilarClaims(self, embedding) -> list:
        similar = []

        for assertion in self._assertions.values():
            similarity = Generator.encodedSimilarity(embedding, assertion.getEmbedding())
            if similarity > 0.4:
                similar.append((similarity, assertion.getID()))
        
        return similar
    
    def _createAssertion(self, claim: str, sourceID: int, degree: int) -> Assertion:
        assertion = Assertion(self._idCounter, time.time(), sourceID, claim, degree)
        self._idCounter += 1

        return assertion

    def addClaim(self, claim: str, sourceID: int, degree: int):
        assertion = self._createAssertion(claim, sourceID, degree)
        self._strToAssertion[claim] = assertion.getID()
        
        self._addConnections(assertion)
        self._assertions[assertion.getID()] = assertion

        return assertion
    
    def getExistingClaim(self, claimID: int):
        return self._assertions[claimID]

    def getClaim(self, claim: str, sourceID=-1, degree=1):
        claim = re.sub(r'^"(.*)"$', r'\g<1>', claim)
        claim = claim.replace('"', "'")

        if claim in self._strToAssertion:
            return self._assertions[self._strToAssertion[claim]]

        potentialDuplicates = [(pair[0], self._assertions[pair[1]]) for pair in self.getSimilarClaims(Generator.encode(claim))]

        if len(potentialDuplicates) == 0:
            return self.addClaim(claim, sourceID, degree)

        with open('engine/core/prompts/findDuplicates.txt', 'r') as prompt, open('engine/core/prompts/findDuplicates.gnbf', 'r') as grammar:
            prompt = prompt.read().format(claim=claim, closestMatches="\n".join(["Index {} [similarity {similarity:.2f}]: \"{claim}\"".format(i + 1, similarity=potentialDuplicates[i][0], claim=potentialDuplicates[i][1].getClaim()) for i in range(len(potentialDuplicates))]))
            grammar = grammar.read().format(indices=" | ".join(["\"{}\"".format(i + 1) for i in range(len(potentialDuplicates))]))

            print(prompt)

            out = Generator.create_deterministic_completion(Formatter.generatePrompt(prompt, "The answer is "), grammar)
            out = out["choices"][0]["text"]

            print(out)

            if out == "0":
                self.addClaim(claim, sourceID, degree)
            else:
                self._strToAssertion[claim] = potentialDuplicates[int(out) - 1][1].getID()

            return self._assertions[self._strToAssertion[claim]]

    def _addConnections(self, assertion: Assertion):
        potentialContradictions = [self._assertions[pair[1]] for pair in self.getSimilarClaims(assertion.getEmbedding())]

        if len(potentialContradictions) == 0:
            return
        
        with open('engine/core/prompts/findContradicting.txt', 'r') as prompt, open('engine/core/prompts/findContradicting.gnbf', 'r') as grammar:
            prompt = prompt.read().format(claim=assertion.getClaim(), closest_matches="\n".join(["{}. \"{}\"".format(i + 1, potentialContradictions[i].getClaim()) for i in range(len(potentialContradictions))]))
            grammar = grammar.read().format(grammar=' "\n" '.join(['("{}. Compatibility with \'{}\': " strength)'.format(i + 1, potentialContradictions[i].getClaim()) for i in range(len(potentialContradictions))]))

            out = Generator.create_deterministic_completion(prompt, grammar)
            out = out["choices"][0]["text"]

            print(prompt)
            print(out)
            
            arr = out.split("\n")

            i = 0

            for item in arr:
                assertionID = potentialContradictions[i].getID()
                i += 1

                value = item.split(": ")[-1]
                value = int(value.replace("%", ""))/100.0

                if assertion.getID() not in self._supportNetwork:
                    self._supportNetwork[assertion.getID()] = {}
                if assertionID not in self._supportNetwork:
                    self._supportNetwork[assertionID] = {}
                
                self._supportNetwork[assertion.getID()][assertionID] = value
                self._supportNetwork[assertionID][assertion.getID()] = value

    def getConnections(self, assertion: Assertion):
        if not assertion.getID() in self._supportNetwork:
            return {}
        
        return self._supportNetwork[assertion.getID()]