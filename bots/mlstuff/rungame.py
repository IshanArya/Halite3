import os
import secrets

MAX_TURNS = 50
map_settings = {32: 400,
                40: 425,
                48: 450,
                56: 475,
                64: 500}

for i in range(2):
    map_size = secrets.choice(list(map_settings.keys()))
    commands = [f'./halite --replay-directory replays/ --turn-limit {MAX_TURNS} -vvv --no-logs --width {map_size} --height {map_size} "Macintosh HD⁩/⁨Users⁩/⁨bharddwajvemulapalli⁩/⁨Documents⁩/⁨Halite_project⁩/⁨Halite3_Python3_MacOS⁩/⁨Halite3⁩/⁨bots/⁩python3 bharddwaj_experiment_ML.py" "Macintosh HD⁩/⁨Users⁩/⁨bharddwajvemulapalli⁩/⁨Documents⁩/⁨Halite_project⁩/⁨Halite3_Python3_MacOS⁩/⁨Halite3⁩/⁨bots/⁩python3 bharddwaj_experiment_ML.py"',
                f'./halite --replay-directory replays/ --turn-limit {MAX_TURNS} -vvv --no-logs --width {map_size} --height {map_size} "Macintosh HD⁩/⁨Users⁩/⁨bharddwajvemulapalli⁩/⁨Documents⁩/⁨Halite_project⁩/⁨Halite3_Python3_MacOS⁩/⁨Halite3⁩/⁨bots/⁩python3 bharddwaj_experiment_ML.py" "Macintosh HD⁩/⁨Users⁩/⁨bharddwajvemulapalli⁩/⁨Documents⁩/⁨Halite_project⁩/⁨Halite3_Python3_MacOS⁩/⁨Halite3⁩/⁨bots/⁩python3 bharddwaj_experiment_ML.py" "Macintosh HD⁩/⁨Users⁩/⁨bharddwajvemulapalli⁩/⁨Documents⁩/⁨Halite_project⁩/⁨Halite3_Python3_MacOS⁩/⁨Halite3⁩/⁨bots/⁩python3 bharddwaj_experiment_ML.py" "Macintosh HD⁩/⁨Users⁩/⁨bharddwajvemulapalli⁩/⁨Documents⁩/⁨Halite_project⁩/⁨Halite3_Python3_MacOS⁩/⁨Halite3⁩/⁨bots/⁩python3 bharddwaj_experiment_ML.py"']

    command = secrets.choice(commands)
    os.system(command)
