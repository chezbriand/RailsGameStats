import matplotlib.pyplot as plt
import re

def parse_amount(action):
    match = re.search(r'\$(\d+)', action)
    return int(match.group(1)) if match else 0

def process_file(filename, starting_money):
    with open(filename, 'r') as file:
        lines = file.readlines()[::-1]

    players = {}
    rounds = []
    current_round = None
    for line in lines:
        round, player, action = line.strip().split("\t")
        if player not in players:
            players[player] = [starting_money]
        else:
            if current_round != round:
                players[player].append(players[player][-1])
                current_round = round
            if action.startswith("Built") or action.startswith("Upgraded"):
                players[player].append(players[player][-1] - parse_amount(action))
            elif action.startswith("Delivered"):
                players[player].append(players[player][-1] + parse_amount(action))
            else:
                players[player].append(players[player][-1])
        if round not in rounds:
            rounds.append(round)

    for player, money in players.items():
        plt.plot(range(len(money)), money, label=player)
    plt.xticks(range(len(rounds)), rounds)
    plt.xlabel('Round')
    plt.ylabel('Money')
    plt.legend()
    plt.show()

process_file("Original Order.txt", 50)