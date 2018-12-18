import os
import secrets

MAX_TURNS = 200
map_settings = {32: 400,
                40: 425,
                48: 450,
                56: 475,
                64: 500}

for i in range(100):
    map_size = secrets.choice(list(map_settings.keys()))
    commands = [f'./halite --replay-directory replays/ --turn-limit {MAX_TURNS} -vvv --no-logs --width {map_size} --height {map_size} "python3 ../kingsmenmlBot.py" "python3 ../kingsmenmlBot.py"',
                f'./halite --replay-directory replays/ --turn-limit {MAX_TURNS} -vvv --no-logs --width {map_size} --height {map_size} "python3 ../kingsmenmlBot.py" "python3 ../kingsmenmlBot.py" "python3 ../kingsmenmlBot.py" "python3 ../kingsmenmlBot.py"']

    command = secrets.choice(commands)
    os.system(command)
