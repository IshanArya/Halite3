#!/bin/sh

./halite --replay-directory replays/ -vvv --width 16 --height 16 "python3 bots/testBot1.py" "python3 bots/directionEvalBot.py"

./halite --replay-directory replays/ -vvv --width 32 --height 32 "python3 bots/inspiredDetectionBot.py" "python3 bots/inspiredDetectionBot.py"

./halite --replay-directory replays/ -vvv --width 16 --height 16 "python3 bots/inspiredDetectionBot.py" "python3 bots/inspiredDetectionBot.py"

./halite --replay-directory replays/ -vvv --width 32 --height 32 "python3 bots/testMyBot.py" "python3 bots/testMyBot.py"

./halite --replay-directory replays/ -vvv --width 32 --height 32 "python3 bots/testMyBot.py" "python3 bots/svmAttemptBot.py"


#Ishan's Tests#
./halite --replay-directory replays/ -vvv --no-logs --width 64 --height 64 "python3 bots/oldTestMyBot.py" "python3 bots/kingsmenv3Bot.py" "python3 bots/testMyBot.py" "python3 bots/experimentOneBot.py"

hlt play -r "python experimentOneBot.py" -r "python kingsmenv3Bot.py" -r "python kingsmenv3Bot.py" -r "python experimentOneBot.py" -b ../halite --output-dir ../replays -i 10
hlt play -r "python experimentOneBot.py" -r "python kingsmenv3Bot.py" -r "python kingsmenv3Bot.py" -r "python experimentOneBot.py" -b ../halite-linux --output-dir ../replays -i 10

./halite --replay-directory replays/ -vvv --no-logs --width 40 --height 40 "python3 bots/kingsmenv3Bot.py" "python3 bots/experimentOneBot.py"
./halite --replay-directory replays/ -vvv --no-logs --width 32 --height 32 "python3 bots/bharddwaj_experiment_bot.py" "python3 bots/bharddwaj_experiment_bot.py"
../halite -vvv --no-logs --width 8 --height 8 "python3 ./kingsmenv3Bot.py" "python3 ./experimentOneBot.py"

#Bharddwaj's commands
 python3 -m hlt_client play -b "/Users/bharddwajvemulapalli/Documents/Halite_project/Halite3_Python3_MacOS/Halite3/hlt" -r "python3 /Users/bharddwajvemulapalli/Documents/Halite_project/Halite3_Python3_MacOS/Halite3/bots/testMyBot.py" -r "python3 /Users/bharddwajvemulapalli/Documents/Halite_project/Halite3_Python3_MacOS/Halite3/bots/testMyBot.py" -i 10
#getting permission denied from that for some reason
