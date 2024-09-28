# NeuroNPC

## Installing dependencies

Install a virtual environment so that your global installs won't interfere with other projects:

1. Setup the environment with `python -m venv .venv`.
2. To enter the virtual environment, run `source .venv/bin/activate`.
3. To install dependencies, run `pip install -r requirements.txt`.

**If you want to install a new package regardless of if you have a virtual environment, run `pip freeze`, copy all of the contents it prints out, and replace everything in `requirements.txt`**

## Running test.py

1. Enter the virtual environment
2. Change directory to the main folder (`cd ..` until you reach NeuroNPC)
3. Make sure to set `PYTHONPATH` environment variable to `.` On Linux/Mac, this is `export PYTHONPATH=.` On windows, this is `set PYTHONPATH=.`
4. Run `python test.py`
