from enum import Enum
from engine.enums.degree import Degree

class PersonalityModule:
    def __init__(self, traits: dict[str, Degree], phrases: list[str], preferredWords: list[str]) -> None:
        self._personalityTraits = traits
        self._phrases = phrases
        self._preferredWords = preferredWords

    def getTraits(self):
        return self._personalityMeter.keys()
    
    def addTrait(self, trait: str, strength: Degree):
        self._personalityTraits[trait] = strength

    def removeTrait(self, trait: str):
        self._personalityTraits.pop(trait, None)

    def getTraitStrength(self, trait: str) -> Degree:
        return self._personalityTraits[trait]

    def increaseTrait(self, trait: str) -> None:
        self._personalityTraits[trait] = Degree(min(len(Degree) - 1, self._personalityTraits[trait].value + 1))

    def decreaseTrait(self, trait: str) -> None:
        self._personalityTraits[trait] = Degree(max(0, self._personalityTraits[trait].value - 1))
    
    def __str__(self):
        return 'Traits: [{traits}]\nPhrases: [{phrases}]\nPreferred words: [{words}]'\
            .format(
                traits=', '.join(['{} ({})'.format(trait.lower(), value.name.lower().replace("_", " ")) for trait, value in self._personalityTraits.items()]),
                phrases=', '.join(['"{}"'.format(phrase) for phrase in self._phrases]),
                words=', '.join(['"{}"'.format(word) for word in self._preferredWords])
            )