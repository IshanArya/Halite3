import os
import argparse

mapDimensions = [32, 40, 48, 56, 64]

parser = argparse.ArgumentParser(description="Automate game running for Halite III bots in Python.")
parser.add_argument("--replay-directory", "-rd", help="directory to store replay files")
args = parser.parse_args()

print(args.echo)