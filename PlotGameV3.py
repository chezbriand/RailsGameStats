import matplotlib.pyplot as plt
# import pandas as pd
import re

def parse_amount(action):
    match = re.search(r'\$(\d+)', action)
    return int(match.group(1)) if match else 0

def parse_segments(action):
    match = re.search(r'Built (\d+) segments', action)
    return int(match.group(1)) if match else 0

def parse_movement(action):
    match = re.search(r'Moved (\d+) spaces', action)
    return int(match.group(1)) if match else 0

def process_file(filename, starting_money):
    with open(filename, 'r') as file:
        lines = file.readlines()[::-1]

    players = {}
    current_rounds = {}
    rounds = []
    segments_built = {}  # New dictionary to track segments built
    segments_cost = {} # Dictionary to track cost of segments built
    loads_delivered = {}
    loads_revenue = {}
    mileposts_moved = {}

    for line in lines:
        round, player, action = line.strip().split("\t")
        if player not in players:
            players[player] = [starting_money]
            current_rounds[player] = None
            segments_built[player] = 0  # Initialize segments built for this player
            segments_cost[player] = 0  # Initialize cost of segments built for this player
            loads_delivered[player] = 0
            loads_revenue[player] = 0
            mileposts_moved[player] = 0
        if current_rounds[player] != round:
            players[player].append(players[player][-1])
            current_rounds[player] = round
        if action.startswith("Built"):
            cost = parse_amount(action)
            players[player][-1] -= cost
            segments_built[player] += parse_segments(action)  # Increment segments built
            segments_cost[player] += cost  # Increment cost of segments built
        elif action.startswith("Upgraded") or action.startswith("Player was taxed"):
            players[player][-1] -= parse_amount(action)
        elif action.startswith("Delivered"):
            revenue = parse_amount(action)
            players[player][-1] += revenue
            loads_delivered[player] += 1 # increment number of loads delivered
            loads_revenue[player] += revenue # add revenue earned
        elif "for rent to" in action:
            rent = parse_amount(action)
            players[player][-1] -= rent
            recipient = action.split("for rent to")[-1].strip()
            if recipient and recipient in players:
                if current_rounds[recipient] != round:
                    players[recipient].append(players[recipient][-1] + rent)
                    current_rounds[recipient] = round
                else:
                    players[recipient][-1] += rent
        elif action.startswith("Moved"):
            movement = parse_movement(action)
            mileposts_moved[player] += movement
        if round not in rounds:
            rounds.append(round)

    # Print totals for each player for each round
            
    print(f"There were a total of {len(rounds)} rounds.")

    for player in players.keys():
        print(f"{player} {players[player]}")
        print(f"{player} built {segments_built[player]} segments for ${segments_cost[player]}")  # Print segments built and cost for each player
        print(f"{player} delivered {loads_delivered[player]} loads for ${loads_revenue[player]}")
        print(f"{player} moved a total of {mileposts_moved[player]} spaces.")

    for player, money in players.items():
        plt.plot(range(len(money)), money, label=player)
    plt.axhline(0, color='black', linewidth=0.5)  # Line at y=0
    plt.axhline(250, color='black', linewidth=0.5)  # Line at y=250plt.xticks(range(len(rounds)), rounds)
    plt.xlabel('Round')
    plt.ylabel('Money')
    plt.legend()

     # Add a line of text under the graph with the total segments built
    stats_text = f"In Game: {filename[:-4]} "
    stats_text += f"there were {len(rounds)} rounds. \n"
    stats_text += "\n".join([f"{player} built {segments_built[player]} segments for \\${segments_cost[player]} delivering {loads_delivered[player]} loads for \\${loads_revenue[player]} with {mileposts_moved[player]} movements." for player in players.keys()])
    plt.figtext(0.25, 0.90, stats_text, ha="left", fontsize=12, bbox={"facecolor":"orange", "alpha":0.5, "pad":5})

    plt.show()

process_file("TMBS0008.txt", 60)