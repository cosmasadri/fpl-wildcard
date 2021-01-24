import json

import numpy as np
import pandas as pd
import requests
from ortools.linear_solver import pywraplp

### INPUT ###
available_money = 99

# weights required for the optimization
w_total_points = 0.5
w_form = 0.4
w_selected_by_percent = 0.1
#############

url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
r = requests.get(url)
fpl_json = r.json()

# defining teams dict
teams = dict([
    [
        team['id'],
        dict(
            name=team['name'],
            short_name=team['short_name']
        )
    ]
    for team in fpl_json['teams']
])

# defining positions dict
positions = dict([
    [
        position['id'],
        dict(
            name=position['singular_name'],
            short_name=position['singular_name_short'],
            max_players=position['squad_select']
        )
    ]
    for position in fpl_json['element_types']
])

# defining players dict list
df_players = pd.DataFrame(fpl_json['elements'])
df_players['form'] = df_players['form'].astype(float)
df_players['selected_by_percent'] = df_players['selected_by_percent'].astype(float)

players = dict([
    [
        player['id'],
        dict(
            first_name=player['first_name'],
            last_name=player['second_name'],
            team_id=player['team'],
            position_id=player['element_type'],
            cost=player['now_cost'],
            total_points=player['total_points'],
            form=int(player['form'] * 10),
            selected_by_percent=int(player['selected_by_percent'] * 10)
        )
    ]
    for _, player in df_players.iterrows()
])

# check maximum value of total points, forma and selected by percent
# for weighting the optimization
max_total_points = df_players['total_points'].max()
max_form = int(df_players['form'].max() * 10)
max_selected_by_percent = int(df_players['selected_by_percent'].max() * 10)

available_money_10 = available_money * 10  # available money multiplied by ten

# OR tools
solver = pywraplp.Solver.CreateSolver("SCIP")

# defining decision variable x for players
x = {}
for player_id in players:
    x[player_id] = solver.IntVar(0, 1, "x[%i]" % player_id)

# constraint: total costs of players cannot be greater than available money
solver.Add(
    sum(
        x[player_id] * player_info["cost"] for player_id, player_info in players.items()
    )
    <= available_money_10
)

# constraint: each team cannot have more than 3 persons
for team_id in teams.keys():
    solver.Add(
        sum(
            x[player_id]
            for player_id, player_info in players.items()
            if player_info["team_id"] == team_id
        )
        <= 3
    )

# constraint: each position must be filled by the specified number of persons of this particular position
for pos_id, pos_info in positions.items():
    solver.Add(
        sum(
            x[player_id]
            for player_id, player_info in players.items()
            if player_info["position_id"] == pos_id
        )
        == pos_info["max_players"]
    )

solver.Maximize(
    solver.Sum(
        x[player_id]
        * (
            (player_info["total_points"] * w_total_points / max_total_points)
            + (player_info["form"] * w_form / max_form)
            + (
                player_info["selected_by_percent"]
                * w_selected_by_percent
                / max_selected_by_percent
            )
        )
        for player_id, player_info in players.items()
    )
)

status = solver.Solve()

selected_players = {}
if status == pywraplp.Solver.OPTIMAL:
    for player_id, player_info in players.items():
        if x[player_id].solution_value() == 1:
            selected_players[player_id] = player_info

selected_players = []
if status == pywraplp.Solver.OPTIMAL:
    for player_id, player_info in players.items():
        if x[player_id].solution_value() == 1:
            selected_players.append(
                {
                    'player_id': player_id,
                    **player_info
                }
            )
    
    print(json.dumps(selected_players))
