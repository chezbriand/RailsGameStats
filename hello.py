import numpy as np 
import re
import sys
import matplotlib.pyplot as plt 

def extract_dollar_amount(text):
    # The regular expression pattern for a dollar amount
    pattern = r'\$(\d+)(?=[\.\s]|$)'
    
    # Find all matches in the text
    matches = re.findall(pattern, text)
    
    # Remove the dollar sign and convert to integers
    amounts = [int(match) for match in matches]
    
    return amounts

# Initialize empty lists for rounds, players, and actions
rounds = []
players = []
actions = []


msg="Here we go!"
print(msg)

with open('Original Order.txt', 'r') as file:
    lines = file.readlines()

lines.reverse()

for line in lines:
    parts = line.strip().split('\t')
    rounds.append(parts[0])
    players.append(parts[1])
    actions.append(parts[2])
    print(line.strip())
    dollars = extract_dollar_amount(line)
    print('In Round ', parts[0],' I found ', dollars, ' dollars!\n')

# Initialize an empty set for unique players
unique_players = set()

# Go through each round, player, and action
for round, player, action in zip(rounds, players, actions):
    # Check if the round is 1
    if round == '1':
        # Add the player to the set of unique players
        unique_players.add(player)

# The number of unique players is the size of the set
num_unique_players = len(unique_players)

print('Found ',num_unique_players,' unique players!\n')

# Initialize an empty dictionary for player totals
player_totals = {player: 50 for player in unique_players}

# Go through each round, player, and action
for round, player, action in zip(rounds, players, actions):
    # Extract the dollar amount from the action
    match = re.search(r'\$(\d+)(?=[\.\s]|$)', action)
    if match:
        amount = int(match.group(1))
        
        # Update the player's total based on the action
        if action.startswith('Built') or action.startswith('Upgraded'):
            player_totals[player] -= amount
        elif action.startswith('Delivered'):
            player_totals[player] += amount


    
# Initialize a dictionary to store each player's totals over time
player_totals_over_time = {player: [] for player in unique_players}

# Go through each round, player, and action
for round, player, action in zip(rounds, players, actions):
    # Extract the dollar amount from the action
    match = re.search(r'\$(\d+)(?=[\.\s]|$)', action)
    if match:
        amount = int(match.group(1))
        
        # Update the player's total based on the action
        if action.startswith('Built') or action.startswith('Upgraded'):
            player_totals[player] -= amount
        elif action.startswith('Delivered'):
            player_totals[player] += amount
        
        # Add the player's current total to their list of totals over time
        player_totals_over_time[player].append(player_totals[player])

# Create a new figure
plt.figure()

# Plot each player's totals over time
for player, totals in player_totals_over_time.items():
    plt.plot(totals, label=player)

# Add a legend
plt.legend()

# Show the plot
plt.show()
