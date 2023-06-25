import pickle
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch


def translate_col(strat):
    # KB Blocking
    if strat[0] and strat[1]:
        return 'b'

    # KB Greedy
    elif strat[0] and not strat[1]:
        return 'g'

    # Greedy
    elif not strat[0] and not strat[1]:
        return 'r'

    else:
        raise ValueError


def translate_strat(strat):
    # KB Blocking
    if strat[0] and strat[1]:
        return 'KB Blocking'

    # KB Greedy
    elif strat[0] and not strat[1]:
        return 'KB Greedy'

    # Greedy
    elif not strat[0] and not strat[1]:
        return 'Greedy'

    else:
        raise ValueError

ALL_CONFIGS = [[[False, False], [False, False], [False, False], "Greedy"],
               [[True, False], [True, False], [True, False], "KB Greedy"],
               [[True, True], [True, True], [True, True], "KB Blocking"],
               # [[True, False], [False, False], [False, False], "1 KB Greedy vs 2 Greedy"],
               # [[True, True], [False, False], [False, False], "1 KB Blocking vs 2 Greedy"],
               # [[True, True], [True, False], [True, False], "1 KB Blocking vs 2 KB Greedy"]
              ]


width = 0.25  # the width of the bars
multiplier = 0

fig, ax = plt.subplots(layout='constrained')
x = np.arange(len(ALL_CONFIGS))

for idx, config in enumerate(ALL_CONFIGS):
    with open(f'./data/{config[3].replace(" ", "_")}.pickl', "rb") as file:
        data = pickle.load(file)

    colors = [translate_col(config[0]), translate_col(config[1]), translate_col(config[2])]
    strats = [translate_strat(config[0]), translate_strat(config[1]), translate_strat(config[2])]
    num_games = 7_000

    mean_scores = [sum(data["p1"]) / num_games,
                   sum(data["p2"]) / num_games,
                   sum(data["p3"]) / num_games]

    for col, data, name in zip(colors, mean_scores, strats):
        offset = width * multiplier
        rects = ax.bar(x[idx] + offset, data, width, label=name, color=col)
        ax.bar_label(rects, padding=3)
        multiplier += 1

legend_elements = [Patch(facecolor='b', edgecolor='b', label='KB Blocking'),
                   Patch(facecolor='g', edgecolor='g', label='KB Greedy'),
                   Patch(facecolor='r', edgecolor='r', label='Greedy')
                  ]


# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Mean Score')
ax.set_title('Scores over Strategies')
ax.set_xticks(np.arange(len(ALL_CONFIGS)) + width, list(map(lambda x: x[3], ALL_CONFIGS)))
ax.legend(loc='upper left', handles=legend_elements, ncols=3)
ax.set_ylim(0, 5)

plt.savefig("test.png")
