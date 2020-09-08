games_won = dict(sara=0, bob=1, tim=5, julian=3, jim=1)

for player, score in games_won:
    print(player, score)
    # games = 'game' if score == 1 else 'games'
    # print(f'{player} has won {score} {games}')