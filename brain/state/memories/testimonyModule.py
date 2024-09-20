from llama_cpp import LlamaGrammar
import LLM.generator.generator as Generator
import LLM.formatter.formatter as Formatter
from engine.classes.assertion import Assertion
from engine.enums.degree import Degree

from enum import Enum

class BeliefClassification(Enum):
    TRUE, FALSE, UNKNOWN = range(3)

class BeliefRanking(Enum):
    SUPPORTS, IRRELEVANT, CONTRADICTS = range(3)

class TestimonyModule:
    def __init__(self):
        self._testimonyArr = set()
    
    def addClaim(self, knowledgeBase, claim: str, sourceID=-1, degree=1):
        self._testimonyArr.add(knowledgeBase.getClaim(claim, sourceID, degree).getID())
    
    def getClaims(self):
        return self._testimonyArr

    def believes(self, claim: str) -> BeliefClassification:
        claimEmbedding = Generator.encode(Formatter.removeStopWords(claim))
        topEvidence = sorted(self._testimonyArr, key=lambda elem: Generator.encodedSimilarity(elem.getEmbedding(), claimEmbedding))[-5:]

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
    
    def searchMemory(self, knowledgeBase, query):
        embedding = Generator.encode(query)
        matches = [pair for pair in knowledgeBase.getSimilarClaims(embedding) if pair[1] in self._testimonyArr]

        if len(matches) == 0:
            return None

        with open('brain/state/memories/prompts/findMatch.txt', 'r') as prompt, open('brain/state/memories/prompts/findMatch.gnbf', 'r') as grammar:
            prompt = prompt.read().format(query=query, closest_matches="\n".join(["{}: \"{}\"".format(i + 1, matches[i][1].content) for i in range(len(matches))]))
            grammar = LlamaGrammar.from_string(grammar.read().format(facts=" | ".join(["\"{}\"".format(i + 1) for i in range(len(matches))])), verbose=False)

            out = Generator.create_deterministic_completion(prompt, grammar)

            if out == "0":
                return None
            else:
                return matches[int(out) - 1][1]
    
    def believabilityScore(self, perceptionModule, assertion):
        if assertion.getDegree() == 1:
            return 1

        perception = perceptionModule.getPerception(assertion.getSourceID())

        trustworthiness = perception.getTrustworthiness() if perception else 1

        return (int(trustworthiness) + 1.0) / (len(Degree)) / assertion.getDegree()

    def believability(self, knowledgeBase, perceptionModule, assertion):
        score = self.believabilityScore(perceptionModule, assertion)

        support = {}

        connected = [pair for pair in knowledgeBase.getConnections(assertion).items() if pair[0] in self._testimonyArr]

        for pair in connected.items():
            id = pair[0]
            strength = pair[1]

            assertion = knowledgeBase.getClaim(id)

            if assertion.getSourceID() not in support:
                support[assertion.getSourceID()] = 0
            
            support[assertion.getSourceID()] += strength * self.believabilityScore(perceptionModule, assertion)
            support[assertion.getSourceID()] = max(-1, min(1, support[assertion.getSourceID()]))
        
        totalDisagreement = score + sum([pair[1] for pair in support])
        
        if totalDisagreement <= -1:
            return "not true"
        elif totalDisagreement <= 0:
            return "possibly false"
        elif totalDisagreement < 1:
            return "not conflicting with existing information"
        else:
            return "probably true"

