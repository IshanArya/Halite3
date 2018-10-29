#!/bin/sh

./halite --replay-directory replays/ -vvv --width 32 --height 32 "python3 bots/testerBot.py" "python3 bots/MyBot.py"

./halite --replay-directory replays/ -vvv --width 32 --height 32 "python3 bots/inspiredDetectionBot.py" "python3 bots/inspiredDetectionBot.py"

./halite --replay-directory replays/ -vvv --width 16 --height 16 "python3 bots/inspiredDetectionBot.py" "python3 bots/inspiredDetectionBot.py"
