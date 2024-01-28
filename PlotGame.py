# I have a file that represents the history of each action taken during a game of VestalRails. I need to write Python code to open the file, read in each line, and reverse the order since the top of the file is the last action taken in the game and I want to start with the first action in the game. Each line of text in the file contains a "Game Round", a "Player Name" and an "Action" . You can assume they are delimited by a Tab character. For each unique player in the game, I need to keep a running total after each action. The action line contains text that describes how money is spent. If the Action line starts with "Built", the dollar amount in that line is a debit from the running total. If the Action line starts with "Delivered" then the dollar amount listed in that text is a Credit. And if the line starts with "Upgraded" then the dollar amount in that line is a debit. Each player starts with a variable amount of money. For instance, each player might start with 50, 60, or 70 dollars. You should use a variable to control the starting money. Then for each action taken (which is each line), the action will show how each player's total is impacted. Note that the player name in the line of text means only that players total is affected by the action text. If the text doesn't start with "Delivered", "Built", or "Upgraded" then there is no impact on their total.  I want to output a graph that shows how the players total changes over the course of each action taken.

import matplotlib.pyplot as plt
import re

def process_file(filename, starting_money):
    with open(filename, 'r') as file:
        lines = file.readlines()[::-1]  # Reverse the lines

    players = {}  # Dictionary to hold player data

    for line in lines:
        round, player, action = line.split('\t')
        action_type = action.split(' ')[0]
        amount = int(re.findall(r'\d+', action)[-1])  # Extract the last number in the action

        if player not in players:
            players[player] = [starting_money]

        if action_type == 'Built' or action_type == 'Upgraded':
            players[player].append(players[player][-1] - amount)
        elif action_type == 'Delivered':
            players[player].append(players[player][-1] + amount)

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
