import matplotlib.pyplot as plt
import re

def process_file(filename, starting_money):
    with open(filename, 'r') as file:
        lines = file.readlines()[::-1]  # Reverse the lines

    players = {}  # Dictionary to hold player data

    for line in lines:
        try:
            round, player, action = line.split('\t')
            action_type = action.split(' ')[0]
            amount = int(re.findall(r'\d+', action)[-1])  # Extract the last number in the action

            if player not in players:
                players[player] = [starting_money]

            if action_type == 'Built' or action_type == 'Upgraded':
                players[player].append(players[player][-1] - amount)
            elif action_type == 'Delivered':
                players[player].append(players[player][-1] + amount)
        except IndexError:
            print(f"Skipping line due to unexpected format: {line}")

    return players

def plot_graph(players):
    for player, money in players.items():
        plt.plot(money, label=player)

    plt.xlabel('Action Number')
    plt.ylabel('Total Money')
    plt.legend()
    plt.show()

filename = 'Original Order.txt'  # Replace with your filename
starting_money = 50  # Replace with your starting money
players = process_file(filename, starting_money)
plot_graph(players)