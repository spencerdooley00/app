from flask import Flask, render_template, request, jsonify
import json
from passing_networks import fetch_data, create_network, generate_d3_data

app = Flask(__name__)

with open("network_data/all_stats_test.json", "r") as f:
    all_stats = json.load(f)

with open("network_data/teams.json", "r") as f:
    team_info = json.load(f)

@app.route("/")
def index():
    seasons = sorted(all_stats.keys(), reverse=True)
    selected_season = request.args.get("season", seasons[0])
    teams = list(all_stats[selected_season].keys())
    selected_team = request.args.get("team", teams[0])
    players = list(all_stats[selected_season][selected_team].keys())

    return render_template(
        "index.html",
        seasons=seasons,
        selected_season=selected_season,
        teams=teams,
        selected_team=selected_team,
        players=players,
        selected_players=players  # preselect all
    )

@app.route("/update_network", methods=["POST"])
def update_network():
    data = request.get_json()
    season = data.get("season")
    team = data.get("team")
    selected_players = data.get("players", [])

    if season and team:
        _, team_data, team_info_season = fetch_data(season, team)
        color = team_info_season["primary_color"]
        _, G = create_network(team_data, team, color, "Pass Per Game", selected_players)
        d3_data = generate_d3_data(G)
        return jsonify(d3_data)

    return jsonify({"nodes": [], "links": []})

if __name__ == "__main__":
    app.run(debug=True)

# from flask import Flask, render_template, request
# import json
# import os
# from passing_networks import fetch_data, create_network, get_default_starters, generate_d3_data

# app = Flask(__name__)

# # Load JSON metadata
# with open("network_data/all_stats.json", "r") as f:
#     all_stats = json.load(f)

# with open("network_data/teams.json", "r") as f:
#     team_info = json.load(f)

# @app.route("/", methods=["GET", "POST"])
# def index():
#     seasons = sorted(all_stats.keys(), reverse=True)
#     selected_season = seasons[0]
#     # selected_team = None
#     teams = list(all_stats[selected_season].keys())
#     selected_team = request.args.get("team")
#     if not selected_team or selected_team not in teams:
#         selected_team = teams[0]    
        
#     selected_players = []

#     if request.method == "POST":
#         selected_season = request.form.get("season")
#         selected_team = request.form.get("team")
#         selected_players = request.form.getlist("players")
#         edge_info = request.form.get("edge_info", "Pass Per Game")

#         if selected_season and selected_team:
#             _, team_data, team_info_season = fetch_data(selected_season, selected_team)

#             color = team_info_season["primary_color"]
#             net, G = create_network(team_data, selected_team, color, edge_info, selected_players)

#             # ✅ Save network JSON for D3.js
#             d3_data = generate_d3_data(G)
#             with open("static/network.json", "w") as f:
#                 json.dump(d3_data, f)

#     # Always update teams + player list based on selection
#     teams = list(all_stats[selected_season].keys())
#     current_team = selected_team or teams[0]
#     players = list(all_stats[selected_season][current_team].keys())

#     # If no players selected, default to all players
#     if not selected_players:
#         selected_players = players

#     return render_template(
#         "index.html",
#         seasons=seasons,
#         selected_season=selected_season,
#         teams=teams,
#         selected_team=current_team,
#         players=players,
#         selected_players=selected_players,
#     )

# if __name__ == "__main__":
#     app.run(debug=True)


# from flask import Flask, render_template, request
# import json
# from passing_networks import fetch_data, create_network, get_default_starters, generate_d3_data
# import os

# app = Flask(__name__)

# # Load JSON metadata
# with open("network_data/all_stats.json", "r") as f:
#     all_stats = json.load(f)

# with open("network_data/teams.json", "r") as f:
#     team_info = json.load(f)

# @app.route("/", methods=["GET", "POST"])
# def index():
#     seasons = sorted(all_stats.keys(), reverse=True)
#     selected_season = seasons[0]
#     selected_team = None
#     selected_players = []
#     network_file = None

#     if request.method == "POST":
#         selected_season = request.form.get("season")
#         selected_team = request.form.get("team")
#         selected_players = request.form.getlist("players")  # List of selected players

#         if selected_season and selected_team:
#             _, team_data, team_info_season = fetch_data(selected_season, selected_team)

#             color = team_info_season["primary_color"]
#             edge_info = request.form.get("edge_info", "Pass Per Game")
#             net, G = create_network(team_data, selected_team, color, edge_info, selected_players)

#             # network_file = f"{selected_team}_network.html"

#     # On GET or POST, repopulate teams and players
#     teams = list(all_stats[selected_season].keys())
#     default_team = selected_team or teams[0]
#     # players = get_default_starters(selected_season, default_team)
#     # Get list of all players
#     players = list(all_stats[selected_season][default_team].keys())

#     # # Check if any players were selected (from form submission)
#     # if selected_players:
#     #     # If any players are selected, use that list
#     #     selected_players = selected_players
#     # else:
#     #     # If no players selected, default to the starters for the team
#     #     selected_players = get_default_starters(selected_season, default_team)
#     if not selected_players:
#         selected_players = list(all_stats[selected_season][default_team].keys())
#     return render_template(
#         "index.html",
#         seasons=seasons,
#         selected_season=selected_season,
#         teams=teams,
#         selected_team=selected_team,
#         players=players,
#         selected_players=selected_players or players,
#         network_file=network_file
#     )

# if __name__ == "__main__":
#     app.run(debug=True)
