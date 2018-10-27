#!/bin/sh

./halite --replay-directory replays/ -vvv --width 32 --height 32 "python3 bots/testerBot.py" "python3 bots/MyBot.py"
