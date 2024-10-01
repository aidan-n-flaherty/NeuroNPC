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

**If you want to install a new package regardless of if you have a virtual environment, run `pip freeze`, copy all of the contents it prints out, and replace everything in `requirements.txt`**

## Running test.py

1. Enter the virtual environment
2. Change directory to the main folder (`cd `path to project`/NueroNPC`)
3. Make sure to set `PYTHONPATH` environment variable to `.` On Linux/Mac, this is `export PYTHONPATH=.` On windows, this is `set PYTHONPATH=.`
4. Run `python simulator/test.py`
