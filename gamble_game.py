import random
import enum
import keyboard
import matplotlib.pyplot as plt

class Strategy(enum.Enum):
    Constant = 1
    Percentage = 2
    PercentageNoElimination = 3

n_players = 10
initial_money = 10
n_games = 10000
round_per_display = 25
strategy = Strategy.Constant
percent = 0.1

player_ids = []
remain_player_ids = []
assets = []

def select_two_players():
    assert(len(remain_player_ids) > 1)

    i = random.randint(0, len(remain_player_ids) - 1)
    while True:
        j = random.randint(0, len(remain_player_ids) - 1)
        if i != j:
            return remain_player_ids[i], remain_player_ids[j]

def player_stay(id):
    if strategy == Strategy.PercentageNoElimination:
        return True
    elif strategy == Strategy.Percentage:
        if assets[id] >= 1.0:
            return True
    elif strategy == Strategy.Constant:
        if assets[id] > 0:
            return True
    return False

def play_once(i, j):
    if strategy == Strategy.Constant:
        amount = 1
    elif strategy == Strategy.Percentage or strategy == Strategy.PercentageNoElimination:
        amount = min(assets[i], assets[j]) * percent
    else:
        raise Exception("the strategy is undefined")

    # change money
    flag = (random.randint(0, 9) % 2 == 0)
    assets[i] += flag * amount
    assets[j] -= flag * amount
    
    # eliminate player
    if player_stay(i) == False:
        remain_player_ids.remove(i)
    if player_stay(j) == False:
        remain_player_ids.remove(j)

# init
for i in range(n_players):
    assets.append(initial_money)
    player_ids.append(i)
    remain_player_ids.append(i)

# simulation
plt.ion()
game = 1
while True:
    # end loop condition
    if keyboard.is_pressed('Esc'):
        break
    if n_games > 0 and game > n_games:
        break
    if len(remain_player_ids) == 1:
        break

    # gamble for one round
    i, j = select_two_players()
    play_once(i, j)
    
    if game % round_per_display == 0:
        plt.clf()
        plt.title("Game {0}, {1} players left".format(game, len(remain_player_ids)))
        plt.xlabel('player id')
        plt.ylabel('assets')
        plt.bar(player_ids, assets, tick_label=player_ids)
        plt.pause(1 / 60.0)
        plt.ioff()

    game += 1

# statistics
winner_id, max_amount = 0, 0
for id in remain_player_ids:
    if assets[id] > max_amount:
        max_amount = assets[id]
        winner_id = id

print("Total games: {0}, Winner: {1}".format(game, winner_id))