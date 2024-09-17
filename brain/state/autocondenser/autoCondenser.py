from enum import Enum
import LLM.formatter.formatter as Formatter
import LLM.generator.generator as Generator
import brain.constants.constants as Constants

class AutoCondenser:
    def __init__(self, timestamp: int, note: str, promptFile: str) -> None:
        self._timestamp = timestamp
        self._notes = [note] if note else []
        self._promptFile = promptFile

    def update(self, timestamp: int, note: str) -> None:
        self._timestamp = timestamp

        if note:
            self._notes.append(note)

            if sum([len(n) for n in self._notes]) > Constants.NOTE_LIMIT:
                with open(self._promptFile, 'r') as prompt:
                    prompt = prompt.read().format(notes="\n".join(['"{}"'.format(note) for note in self._notes]))
                    result = Generator.create_deterministic_completion(Formatter.generatePrompt(prompt))

                    self._notes = [result["choices"][0]["text"]]

    def getNotes(self):
        return self._notes

    def getIdentifier(self) -> str:
        return "<undefined>"