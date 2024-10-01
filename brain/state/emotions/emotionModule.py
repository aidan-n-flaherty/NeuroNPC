from engine.enums.degree import Degree
from engine.enums.emotion import Emotion

class EmotionModule:
    def __init__(self) -> None:
        self._emotionMeter = {}

        for emotion in Emotion:
            self._emotionMeter[emotion] = Degree.NEUTRAL
    
    def getEmotions(self):
        return self._emotionMeter.keys()

    def getEmotion(self, emotion: Emotion) -> Degree:
        return self._emotionMeter[emotion]
    
    def setEmotion(self, emotion: Emotion, degree: Degree) -> None:
        self._emotionMeter[emotion] = Degree

    def increaseEmotion(self, emotion: Emotion) -> None:
        self._emotionMeter[emotion] = Degree(min(6, self._emotionMeter[emotion].value + 1))

    def decreaseEmotion(self, emotion: Emotion) -> None:
        self._emotionMeter[emotion] = Degree(max(0, self._emotionMeter[emotion].value - 1))

    def __str__(self):
        return '{{\n{}\n}}'.format('\n'.join(['{}: {}'.format(emotion.name.lower().replace("_", " "), self._emotionMeter[emotion].name.lower().replace("_", " ")) for emotion in Emotion]))