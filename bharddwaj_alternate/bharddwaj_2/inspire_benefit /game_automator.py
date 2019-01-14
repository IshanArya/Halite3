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
parser.add_argument("--no-compress", help="compress output files", action="store_true", dest="noCompress")
parser.add_argument("-v", "--verbosity", action="count", default=0, help="increase the logging verbosity level", dest="verbosity")
parser.add_argument("-s", "--seed", help="seed of map to generate", dest="seed")
parser.add_argument("-i", "--iterations", help="# of games to run", type=int, default=1, dest="iterations")
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

def logInfo(results, loggingFile=None):
    winner = determineWinner(results)
    print(f"Winner: {winner}")
    scores = getScores(results)
    i = 0
    for score in scores:
        print(f"\tPlayer {i} - {score}")
        i += 1
    if int(winner) == 0:
        return True
    return False


def playGames(binary, replayDirectory, dimension, verbosity, bots, iterations=10, seed=None, noCompress=False, log=False):
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
    
    if noCompress:
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
    print("Starting games!")
    
    numberOfWins = 0
    numberOfLosses = 0
    for i in range(iterations):
        print(f"GAME {i+1}:")
        matchOutput = playGame(binary, dimension, commands, bots)
        # print(matchOutput)
        results = json.loads(matchOutput)
        didWin = logInfo(results)
        if didWin:
            numberOfWins += 1
        else:
            numberOfLosses += 1
        print("========================================")
    print(f"Wins:{numberOfWins} v. Losses:{numberOfLosses}")




playGames(args.binary, args.replayDirectory, args.dimension, args.verbosity, args.bots, args.iterations, args.seed, args.noCompress, args.log)