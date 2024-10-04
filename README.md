# NeuroNPC

## Setting up the LLM
1. First install a LLM of your choice. One example that is recommended for ~16GB RAM is https://huggingface.co/TheBloke/OpenHermes-2.5-Mistral-7B-GGUF/tree/main 
2. Dowload this version: `openhermes-2.5-mistral-7b.Q6_K.gguf` : Size(5.94GB)
3. Place the gguf file into `NeuroNPC\LLM\modelCurrent`

## Installing dependencies

Install a virtual environment so that your global installs won't interfere with other projects:

1. Setup the environment with `python -m venv .venv`.
2. To enter the virtual environment, run `source .venv/bin/activate`.
3. To install dependencies, run `pip install -r requirements.txt`.
4. Installing llama.cpp for specific GPU:
   a. If you just want to run it on your CPU, install normally like so: `pip install llama_cpp_python==0.3.0`

   b. Otherwise, to find out which backend to run for your GPU and any other necessary cmake variables to run: https://github.com/ggerganov/llama.cpp?tab=readme-ov-file#supported-backends

   c. Then, visit https://github.com/abetlen/llama-cpp-python?tab=readme-ov-file#supported-backends to find instructions on how to install for your specific backend

**If you want to install a new package regardless of if you have a virtual environment, run `pip freeze`, copy all of the contents it prints out, and replace everything in `requirements.txt`**

## Running test.py

1. Enter the virtual environment
2. Change directory to the main folder (`cd `path to project`/NueroNPC`)
3. Edit the `.venv/bin/activate` script and add the following: On Linux/Mac, `export PYTHONPATH=.` On windows, this is `set PYTHONPATH=.`
4. Run `python simulator/test.py`

If you don't have venv, simply run the `export` or `set` command in your project directory in a terminal.
