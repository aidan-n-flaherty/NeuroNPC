from enum import Enum
from engine.enums.degree import Degree

class Trait(Enum):
    OPENNESS, CONSCIENTIOUSNESS, EXTRAVERSION, AGREEABLENESS, NEUROTICISM = range(5)

class PersonalityModule:
    def __init__(self, openness: Degree, conscientiousness: Degree, extraversion: Degree, agreeableness: Degree, neuroticism: Degree) -> None:
        self._personalityMeter = {}

        self._personalityMeter[Trait.OPENNESS] = openness
        self._personalityMeter[Trait.CONSCIENTIOUSNESS] = conscientiousness
        self._personalityMeter[Trait.EXTRAVERSION] = extraversion
        self._personalityMeter[Trait.AGREEABLENESS] = agreeableness
        self._personalityMeter[Trait.NEUROTICISM] = neuroticism

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
        return '{{\n{}\n}}'.format('\n'.join(['{}: {}'.format(trait.name, self._personalityMeter[trait].name) for trait in Trait]))