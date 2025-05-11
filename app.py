

from flask import Flask, render_template, request
import json
from passing_networks import fetch_data, create_network, get_default_starters
import os

app = Flask(__name__)

# Load JSON metadata
with open("network_data/all_stats.json", "r") as f:
    all_stats = json.load(f)

with open("network_data/teams.json", "r") as f:
    team_info = json.load(f)

@app.route("/", methods=["GET", "POST"])
def index():
    seasons = sorted(all_stats.keys(), reverse=True)
    selected_season = seasons[0]
    selected_team = None
    selected_players = []
    network_file = None

    if request.method == "POST":
        selected_season = request.form.get("season")
        selected_team = request.form.get("team")
        selected_players = request.form.getlist("players")  # List of selected players

        if selected_season and selected_team:
            _, team_data, team_info_season = fetch_data(selected_season, selected_team)

            color = team_info_season["primary_color"]
            edge_info = request.form.get("edge_info", "Pass Per Game")
            create_network(team_data, selected_team, color, edge_info, selected_players)

            network_file = f"{selected_team}_network.html"

    # On GET or POST, repopulate teams and players
    teams = list(all_stats[selected_season].keys())
    default_team = selected_team or teams[0]
    # players = get_default_starters(selected_season, default_team)
    # Get list of all players
    players = list(all_stats[selected_season][default_team].keys())

    # # Check if any players were selected (from form submission)
    # if selected_players:
    #     # If any players are selected, use that list
    #     selected_players = selected_players
    # else:
    #     # If no players selected, default to the starters for the team
    #     selected_players = get_default_starters(selected_season, default_team)
    if not selected_players:
        selected_players = list(all_stats[selected_season][default_team].keys())
    return render_template(
        "index.html",
        seasons=seasons,
        selected_season=selected_season,
        teams=teams,
        selected_team=selected_team,
        players=players,
        selected_players=selected_players or players,
        network_file=network_file
    )

if __name__ == "__main__":
    app.run(debug=True)
