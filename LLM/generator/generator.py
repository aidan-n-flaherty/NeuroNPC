from llama_cpp import Llama, LlamaRAMCache, LlamaGrammar
from LLM.generator.customLlama import CustomLlama
import LLM.constants.constants as constants
import numpy as np

from sentence_transformers import SentenceTransformer
encoder = SentenceTransformer("all-MiniLM-L6-v2")

import glob
filepath = glob.glob("LLM/modelCurrent/*.gguf")[0]

llm = CustomLlama(model_path=filepath, chat_format="chatml", embedding=True, verbose=False, n_ctx=2048 + 1024, n_gpu_layers=-1)

cache = LlamaRAMCache()

llm.set_cache(cache)

def tokenCount(string):
    return len(llm.tokenize(bytes(string, 'utf-8')))

def encode(string):
    return encoder.encode(string)

def encodedSimilarity(embeddingA, embeddingB):
    return np.dot(embeddingA, embeddingB) / (np.linalg.norm(embeddingA) * np.linalg.norm(embeddingB))

def create_deterministic_completion(prompt, grammar=None):
    return llm.create_completion(prompt, model=constants.MODEL_NAME, max_tokens=512, stop=["<|im_start|>", "<|im_end|>"], echo=False, stream=False, mirostat_mode=0, mirostat_tau=5, top_p=1.0, temperature=0.01, grammar=grammar)

def create_completion(prompt, grammar=None):
    return llm.create_completion(prompt, model=constants.MODEL_NAME, max_tokens=512, stop=["<|im_start|>", "<|im_end|>"], echo=False, stream=False, mirostat_mode=0, mirostat_tau=5, top_p=0.95, repeat_penalty=1.25, grammar=grammar)