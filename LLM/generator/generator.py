from llama_cpp import Llama, LlamaRAMCache, LlamaGrammar
#from LLM.generator.customLlama import CustomLlama
import LLM.constants.constants as constants
import numpy as np

from transformers import pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

from sentence_transformers import SentenceTransformer
encoder = SentenceTransformer("all-MiniLM-L6-v2")

import json
import argparse
parser = argparse.ArgumentParser()

parser.add_argument('-s', '--server', action='store_true')

args = parser.parse_args()

import requests

url = "http://localhost:8080/completion"

import glob

from nltk.tokenize import word_tokenize

llm = None

if not args.server:
    filepath = glob.glob("LLM/modelCurrent/*.gguf")[0]

    llm = Llama(model_path=filepath, chat_format="chatml", embedding=True, verbose=False, n_ctx=2048 + 1024, n_gpu_layers=-1, logits_all=True)

    cache = LlamaRAMCache()

    llm.set_cache(cache)

def tokenCount(string):
    if args.server:
        return len(word_tokenize(string))
    else:
        return len(llm.tokenize(bytes(string, 'utf-8')))

def encode(string):
    return encoder.encode(string)

def encodedSimilarity(embeddingA, embeddingB):
    return np.dot(embeddingA, embeddingB) / (np.linalg.norm(embeddingA) * np.linalg.norm(embeddingB))

def create_deterministic_completion(prompt: str, grammar=None):
    if args.server:
        body = {
            "prompt": prompt,
            "n_predict": 512,
            "stream": False,
            "stop": ["<|im_start|>", "<|im_end|>"],
            "temperature": 0.01,
            "repeat_penalty": 1.25
        }

        if grammar:
            body['grammar'] = grammar
        
        r = requests.post(url=url, data=json.dumps(body))

        data = r.json()

        return {
            "choices": [{
                 "text": data["content"]
            }]
        }
    else:
        return llm.create_completion(prompt, model=constants.MODEL_NAME, max_tokens=512, stop=["<|im_start|>", "<|im_end|>"], echo=False, stream=False, mirostat_mode=0, mirostat_tau=5, top_p=1.0, temperature=0.01, grammar=LlamaGrammar.from_string(grammar, verbose=False) if grammar else None)

def create_completion(prompt: str, grammar=None):
    if args.server:
        body = {
            "prompt": prompt,
            "n_predict": 512,
            "stream": False,
            "stop": ["<|im_start|>", "<|im_end|>"],
            "repeat_penalty": 1.25
        }

        if grammar:
            body['grammar'] = grammar
        
        r = requests.post(url=url, data=json.dumps(body))

        data = r.json()

        return {
            "choices": [{
                 "text": data["content"]
            }]
        }
    else:
        return llm.create_completion(prompt, model=constants.MODEL_NAME, max_tokens=512, stop=["<|im_start|>", "<|im_end|>"], echo=False, stream=False, mirostat_mode=0, mirostat_tau=5, top_p=0.95, repeat_penalty=1.25, grammar=LlamaGrammar.from_string(grammar, verbose=False) if grammar else None)

def classify(sentence: str, labels: list[str]) -> str:
    return classifier(sentence, labels)["labels"][0]