import os
import subprocess
import argparse
import random
import json

mapDimensions = [32, 40, 48, 56, 64]

parser = argparse.ArgumentParser(description="Automate game running for Halite III bots in Python.")
parser.add_argument("-b", "--binary", help="location of halite binary file", required=True, dest="binary")
parser.add_argument("-rd", "--replay-directory", help="directory to store replay files", dest="replayDirectory")
parser.add_argument("-d", "--dimension", help="dimension of map", default=0, dest="dimension", type=int)
parser.add_argument("--log", help="log errors", action="store_true")
parser.add_argument("--compress", help="compress output files", action="store_true")
parser.add_argument("-v", "--verbosity", action="count", default=0, help="increase the logging verbosity level", dest="verbosity")
parser.add_argument("-s", "--seed", help="seed of map to generate", dest="seed")
parser.add_argument("-i", "--iterations", help="# of games to run", type=int, default=10, dest="iterations")
parser.add_argument("bots", help="bots to play", nargs="+")


args = parser.parse_args()

def playGame(binary, dimension, flags, bots):
    
    commands = [binary, "--results-as-json"]

    if dimension == 0:
        dimension = random.choice(mapDimensions)
    dimension = str(dimension)
    commands.extend(['--height', dimension])
    commands.extend(['--width', dimension])

    commands.extend(flags)

    for bot in bots:
        commands.append("python3 " + bot)

    return subprocess.check_output(commands).decode("utf-8")

def determineWinner(results):
    """
    From the game result string, extract the winner's id.
    :param game_result: The result of running a game on the Halite binary
    :return:
    """
    for player_id, stats in results["stats"].items():
        if stats["rank"] == 1:
            return player_id
def getGameSeed(results):
    return results["map_seed"]
def getScore(results, player):
    return results["stats"][str(player)]["score"]
def getScores(results):
    scores = []
    for stats in results["stats"].values():
        scores.append(stats["score"])
    return scores
def getDimension(results):
    return results["map_height"]


def formatLog(winStatus, dimension, spawnTurnDivider, totalHalite, gameSeed, playerScores):
    log = f"{winStatus},{dimension},{spawnTurnDivider},{totalHalite},{gameSeed}"
    for score in playerScores:
        log = f"{log},{score}"
    log = f"{log}\n"
    return log

def logInfo(results, loggingFile):
    targetWinner = 0
    winner = determineWinner(results)
    print(winner);
    logFile = f"bot-{targetWinner}.log"
    bot0Log = open(logFile)
    logLine = bot0Log.readline()
    spawnTurnDivider = logLine[logLine.index("-(")+2:logLine.index(")-")]
    logLine = bot0Log.readline()
    totalHalite = logLine[logLine.index("-(")+2:logLine.index(")-")]
    gameSeed = getGameSeed(results)
    dimension = getDimension(results)
    winStatus = "LOSE"
    if int(winner) == targetWinner:
        winStatus = "WIN"
    scores = getScores(results)
    logLine = formatLog(winStatus, dimension, spawnTurnDivider, totalHalite, gameSeed, scores)
    print(logLine)
    loggingFile.write(logLine)


def playGames(binary, replayDirectory, dimension, verbosity, bots, iterations=10, seed=None, compress=False, log=False):
    commands = []
    binary = os.path.abspath(binary)

    if replayDirectory is not None:
        replayDirectory = os.path.abspath(replayDirectory)
        if not os.path.lexists(replayDirectory):
            try:
                os.mkdir(replayDirectory)
            except FileExistsError:
                pass
        commands.extend(['--replay-directory', replayDirectory])
    else:
        commands.append("--no-replay")
    
    if compress:
        commands.append("--no-compression")
    if not log:
        commands.append("--no-logs")
    if seed:
        commands.extend(['--seed', str(seed)])
    
    if verbosity != 0:
        commands.append("-" + ("v" * verbosity))

    if not(len(bots) == 4 or len(bots) == 2):
        raise IndexError("The number of bots specified must be either 2 or 4.")


    print(commands)
    loggingFile = f"{len(bots)}-{dimension}.csv"
    loggingFile = open(loggingFile, "a+")
    print("Starting games!")
    
    
    for i in range(iterations):
        print(f"GAME {i+1}:")
        matchOutput = playGame(binary, dimension, commands, bots)
        print(matchOutput)
        results = json.loads(matchOutput)
        logInfo(results, loggingFile)
        print("========================================")
    loggingFile.close()




playGames(args.binary, args.replayDirectory, args.dimension, args.verbosity, args.bots, args.iterations, args.seed, args.compress, args.log)