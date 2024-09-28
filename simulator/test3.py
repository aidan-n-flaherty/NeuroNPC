# Use a pipeline as a high-level helper
from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
candidate_labels = ['claim', 'speculation', 'question', 'conditional', 'threat', 'suggestion', 'small talk', 'other']
candidate_labels_2 = ['very important', 'important', 'moderately important', 'slightly important', 'not important']

while True:
    sentence = input(">>> ")
    print(classifier(sentence, candidate_labels))
    print(classifier(sentence, candidate_labels_2))