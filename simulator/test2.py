"""import LLM.generator.generator as Generator

from fastcoref import spacy_component
import spacy

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("fastcoref")

while True:
    print(nlp(input(">>> "), component_cfg={"fastcoref": {'resolve_text': True}})._.resolved_text)"""