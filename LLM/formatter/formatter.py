from LLM.constants.constants import MODEL_NAME, NARRATOR_NAME
from brain.state.memories.observedMemory import ObservedMemory
import time
import re
import nltk
nltk.download('stopwords')
nltk.download('maxent_ne_chunker')
nltk.download('words')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree

stop_words = set(stopwords.words('english'))

def getModelName():
    return MODEL_NAME

def getNarratorName():
    return NARRATOR_NAME

def removeStopWords(text: str):
    word_tokens = word_tokenize(text)
    text = " ".join([w for w in word_tokens if not w.lower() in stop_words and not w in ['.', '?', '!', '\'', '"', ',', ';', ':', '-', '(', ')']])
    
    return text

def resolveNames(text: str, world):
    for match in re.findall(r"<@[0-9]+>", text):
        id = re.sub("[^0-9]", "", match)
        name = world.getAgent(id).getName()

        text = text.replace(match, name)
    
    return text

def formatTags(text: str, world):
    results = ne_chunk(pos_tag(word_tokenize(text)))
    
    for result in results:
        if type(result) == Tree:
            name = ' '.join([leaf[0] for leaf in result.leaves()])
            if result.label() == 'PERSON':
                agent = world.getAgentByName(name)
                if agent:
                    text = text.replace(name, "<@{}>".format(agent.getID()))
    
    return text

def formatHistory(agentID: int, summarizedMemory, observedMemoryModule):
    history = ""

    lastAuthor = None

    if summarizedMemory:
        history += "<|im_start|>{author}\nHere's the last thing you remember: {memory}<|im_end|>\n".format(author=NARRATOR_NAME, memory=summarizedMemory.getDescription())

    referencedAgents = set()

    for memory in observedMemoryModule.getShortTermMemories():
        author = MODEL_NAME if memory.referencesAgent(agentID) else NARRATOR_NAME

        if lastAuthor is None:
            history += "<|im_start|>{}".format(author)
        elif lastAuthor != author:
            history += "<|im_end|>\n<|im_start|>{}".format(author)
        
        if memory.getAgentID() >= 0 and memory.getAgentID() != agentID and memory.getAgentID() not in referencedAgents:
            history += "\n" + observedMemoryModule.getPerceptionStr(memory.getAgentID())

            referencedAgents.add(memory.getAgentID())

        history += "\n{memory}".format(memory=(memory.getFunctionCall() if memory.referencesAgent(agentID) else memory.getObservedDescription()))

        if memory.getNote():
            history += " " + memory.getNote()

        lastAuthor = author
    
    history += "<|im_end|>\n"

    return history

def generatePrompt(prompt: str, initialCompletion=""):
    return "<|im_start|>{narrator}\n{prompt}<|im_end|>\n<|im_start|>{model}\n{initialCompletion}".format(narrator=NARRATOR_NAME, prompt=prompt, model=MODEL_NAME, initialCompletion=initialCompletion)

def timeToString(t: int):
    timeDiff = t - time.time()

    timeStr = "{}"

    if timeDiff < 0:
        timeStr = timeStr + " ago"
    else:
        timeStr = "in " + timeStr
    timeDiff = abs(timeDiff)

    timeVal, timeUnit = (None, None)

    if timeDiff < 60:
        timeVal = int(timeDiff)
        timeUnit = "second"
    elif timeDiff < 60 * 60:
        timeVal = int(timeDiff/60)
        timeUnit = "minute"
    elif timeDiff < 24 * 60 * 60:
        timeVal = int(timeDiff/(60 * 60))
        timeUnit = "hour"
    elif timeDiff < 7 * 24 * 60 * 60:
        timeVal = int(timeDiff/(24 * 60 * 60))
        timeUnit = "day"
    elif timeDiff < 28 * 24 * 60 * 60:
        timeVal = int(timeDiff/(7 * 24 * 60 * 60))
        timeUnit = "week"
    elif timeDiff < 365 * 24 * 60 * 60:
        timeVal = int(timeDiff/(28 * 24 * 60 * 60))
        timeUnit = "month"
    else:
        timeVal = int(timeDiff/(365 * 24 * 60 * 60))
        timeUnit = "year"

    return timeStr.format("{} {}{}".format(timeVal, timeUnit, ("s" if timeVal != 1 else "")))
    