import os
import secrets

MAX_TURNS = 50
map_settings = {32: 400,
                40: 425,
                48: 450,
                56: 475,
                64: 500}

while True:
    map_size = secrets.choice(list(map_settings.keys()))
    commands = [f'./halite --replay-directory replays/ --turn-limit {MAX_TURNS} -vvv --no-logs --width {map_size} --height {map_size} "python3 bharddwaj_experiment_ML.py" "python3 bharddwaj_experiment_ML.py"',
                f'./halite --replay-directory replays/ --turn-limit {MAX_TURNS} -vvv --no-logs --width {map_size} --height {map_size} "python3 bharddwaj_experiment_ML.py" "python3 bharddwaj_experiment_ML.py" "python3 bharddwaj_experiment_ML.py" "python3 bharddwaj_experiment_ML.py"']

    command = secrets.choice(commands)
    os.system(command)
