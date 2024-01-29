import matplotlib.pyplot as plt
import pandas as pd
import re

def parse_amount(action):
    match = re.search(r'\$(\d+)', action)
    return int(match.group(1)) if match else 0

def process_file(filename, starting_money):
    with open(filename, 'r') as file:
        lines = file.readlines()[::-1]

    players = {}
    current_rounds = {}
    rounds = []
    for line in lines:
        round, player, action = line.strip().split("\t")
        if player not in players:
            players[player] = [starting_money]
            current_rounds[player] = None
        if current_rounds[player] != round:
            players[player].append(players[player][-1])
            current_rounds[player] = round
        if action.startswith("Built") or action.startswith("Upgraded") or action.startswith("Player was taxed"):
            players[player][-1] -= parse_amount(action)
        elif action.startswith("Delivered"):
            players[player][-1] += parse_amount(action)
        elif "for rent to" in action:
            rent = parse_amount(action)
            players[player][-1] -= rent
            recipient = action.split("for rent to")[-1].strip()
            if recipient not in players:
                players[recipient] = [starting_money + rent]
            else:
                if current_rounds[recipient] != round:
                    players[recipient].append(players[recipient][-1] + rent)
                    current_rounds[recipient] = round
                else:
                    players[recipient][-1] += rent        
        if round not in rounds:
            rounds.append(round)

    # Create DataFrame and print
    # df = pd.DataFrame(players, index=rounds)
    # print(df)

    for player, money in players.items():
        plt.plot(range(len(money)), money, label=player)
    plt.axhline(0, color='black', linewidth=0.5)  # Line at y=0
    plt.axhline(250, color='black', linewidth=0.5)  # Line at y=250plt.xticks(range(len(rounds)), rounds)
    plt.xlabel('Round')
    plt.ylabel('Money')
    plt.legend()
    plt.show()

process_file("BSRVone.txt", 70)