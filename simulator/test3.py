# Use a pipeline as a high-level helper
from transformers import pipeline
import LLM.generator.generator as Generator
import LLM.formatter.formatter as Formatter

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
candidate_labels = ['claim', 'speculation', 'question', 'conditional', 'threat', 'suggestion', 'small talk', 'other']
candidate_labels_2 = ['very important', 'important', 'moderately important', 'slightly important', 'not important']

while True:
    sentence = input(">>> ")
    print(classifier(sentence, candidate_labels))
    print(classifier(sentence, candidate_labels_2))
    print(Generator.create_completion(Formatter.generatePrompt(f"Classify {sentence} as one of the following: {candidate_labels}. Do not explain, just output the label and nothing else.\n\nOutput:"))["choices"][0]["text"])