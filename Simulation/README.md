# CoffeeBot Simulation


## Setup
To setup, start a venv. 

Mac:
```bash
python -m venv venv
source venv/bin/activate
```

Windows:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
If this doesn't work, you may have to run this in an Admin shell first:
```powershell
set-executionpolicy remotesigned
```


Next, install all the python requirements
```bash
pip install -r requirements.txt
```

## Running
To run the simulation, make sure you are in this `Simulation` directory and run:

```bash
python3 main.py
```

You should see a window pop up with the simulation.


