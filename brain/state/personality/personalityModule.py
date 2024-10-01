from enum import Enum
from engine.enums.degree import Degree

class Trait(Enum):
    HUMOR, PATIENCE, HELPFULNESS, INTELLIGENCE, DISCIPLINE = range(5)

class PersonalityModule:
    def __init__(self, humor: Degree, patience: Degree, helpfulness: Degree, intelligence: Degree, discipline: Degree) -> None:
        self._personalityMeter = {}

        self._personalityMeter[Trait.HUMOR] = humor
        self._personalityMeter[Trait.PATIENCE] = patience
        self._personalityMeter[Trait.HELPFULNESS] = helpfulness
        self._personalityMeter[Trait.INTELLIGENCE] = intelligence
        self._personalityMeter[Trait.DISCIPLINE] = discipline

    def getTraits(self):
        return self._personalityMeter.keys()

    def getTraitStrength(self, trait: Trait) -> Degree:
        return self._personalityMeter[trait]
    
    def setTrait(self, trait: Trait, degree: Degree) -> None:
        self._personalityMeter[trait] = degree

    def increaseTrait(self, trait: Trait) -> None:
        self._personalityMeter[trait] = Degree(min(6, self._personalityMeter[trait].value + 1))

    def decreaseTrait(self, trait: Trait) -> None:
        self._personalityMeter[trait] = Degree(max(0, self._personalityMeter[trait].value - 1))
    
    def __str__(self):
        return '{{\n{}\n}}'.format('\n'.join(['{}: {}'.format(trait.name.lower().replace("_", " "), self._personalityMeter[trait].name.lower().replace("_", " ")) for trait in Trait]))