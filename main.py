import datetime
import random
from pathlib import Path

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def is_move_legal(board, origin, target):
    if origin == target:
        return False
    if not board[origin]:
        return False
    if not board[target]:
        return True
    origin_top = board[origin[-1]]
    target_top = board[target[-1]]
    return target_top > origin_top


if __name__ == '__main__':
    num_disks = 4
    attempts = 50

    # Create new CSV file for each run instance and write header record. CSV will later be used to create Pandas
    # module Dataframe object.

    path = Path("output")
    path.mkdir(parents=True, exist_ok=True)
    filename = "TowersOfHanoi_" + str(datetime.datetime.now()) + ".csv"
    filename = filename.replace(":", ".")
    filepath = path / filename
    f = open(filepath, "a")
    f.write("Header " + "Start Time: " + str(datetime.datetime.now()) + "\n")

    num_optimal_moves = (2 ** num_disks) - 1
    print("The fastest you can solve this game is in", num_optimal_moves)


    def play_game():
        startTime = datetime.datetime.now()
        moves = 0
        board = {
            "a": [*range(num_disks, 0, -1)],
            "b": [],
            "c": []
        }
        options = list(board.keys())
        while len(board["c"]) != num_disks:
            moves += 1
            origin = options[random.randrange(len(options))]
            target = options[random.randrange(len(options))]
            if not is_move_legal(board, origin, target):
                continue
            ring = board[origin].pop()
            board[target].append(ring)
        endTime = datetime.datetime.now()
        deltaTime = str(int((endTime - startTime).total_seconds() * 1000))  # convert time delta to milliseconds
        print("Game over, it took # moves:", moves, "in", deltaTime)
        f.write(str(moves) + ',' + deltaTime + "\n")
        return moves


    # Enter how many times to play game
    num_user_moves_cumulative_sum = 0
    for i in range(attempts):
        num_user_moves_cumulative_sum += play_game()
    f.write("Trailer " + str(num_user_moves_cumulative_sum) + " total move over " + str(
        i + 1) + " runs. " + "End time: " + str(datetime.datetime.now()))
    f.close()

    # Import csv file using Pandas library and create Dataframe object (ignoring header and trailer records)
    df = pd.read_csv(filepath, names=['# of moves', 'Time elapsed (ms)'], skiprows=1, skipfooter=1, engine='python')

    # Define linear regression using numpy library and insert into dataframe object
    d = np.polyfit(df['# of moves'], df['Time elapsed (ms)'], 1)
    fpoly1d = np.poly1d(d)
    df.insert(0, 'Linear regression', fpoly1d(df['# of moves']))

    # Print entire Dataframe object
    print(df.to_string())

    # Create scatterplot as subplot (ax), and plot linear regression
    ax = df.plot(kind='scatter', x='# of moves', y='Time elapsed (ms)')
    df.plot(x='# of moves', y='Linear regression', color='Red', ax=ax)

    # Display diagram
    plt.show()
