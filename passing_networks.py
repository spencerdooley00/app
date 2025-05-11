import json
import networkx as nx
from pyvis.network import Network
from nltk import ngrams

# Load JSON data from local files
with open("network_data/all_stats.json", "r") as f:
    all_stats = json.load(f)

with open("network_data/teams.json", "r") as f:
    team_info_all = json.load(f)

# Helper function: Jaccard similarity for name matching


def jaccard_similarity(s1, s2):
    set1 = set(ngrams(s1, 3))
    set2 = set(ngrams(s2, 3))
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union)


def check_name_in_list(given_name, player_names, threshold=0.6):
    for name in player_names:
        similarity = jaccard_similarity(given_name.lower(), name.lower())
        if similarity >= threshold:
            return True
    return False

# Fetch data from loaded JSON


def fetch_data(season, team):
    season_data = all_stats[season]
    team_data = season_data[team]
    team_info = team_info_all[f"Season={season}"][team]
    return season_data, team_data, team_info

# Create the network graph


def create_network(team_data, team_name, color, edge_info, selected_players):
    net = Network('600px', '800px', bgcolor='#FFFFFF',
                  font_color='black', directed=True)
    G = nx.DiGraph()

    selected_players = [
        player for player in selected_players if player in team_data.keys()]
    for player in selected_players:
        player_dict = team_data[player]
        net.add_node(player, shape="image",
                     image=player_dict["img"], size=50, label=' ')
        G.add_node(player)

    for player in selected_players:
        if "passes" in team_data[player]:
            player_passing = team_data[player]["passes"]
            for player_passed_to, player_dict in player_passing.items():
                if player_passed_to in selected_players:
                    w = player_dict["passes"] if edge_info == "Pass Per Game" else player_dict.get(
                        "ast", 0)
                    net.add_edge(player, player_passed_to,
                                 value=w, title=str(w), color=color)
                    G.add_edge(player, player_passed_to, weight=w)
    net.set_options("""
    const options = {
      "nodes": {
        "borderWidth": 0,
        "borderWidthSelected": 7,
        "opacity": 1,
        "font": {
          "size": 36
        },
        "scaling": {
          "max": 46
        },
        "size": 19
      },
      "edges": {
        "color": {
          "inherit": true,
          "opacity": 0.5
        },
        "selfReferenceSize": 1,
        "selfReference": {
          "angle": 0.7853981633974483
        },
        "smooth": {
          "forceDirection": "none"
        }
      },
      "physics": {
        "forceAtlas2Based": {
          "gravitationalConstant": -326,
          "springLength": 70,
          "damping": 1
        },
        "minVelocity": 0.75,
        "solver": "forceAtlas2Based",
        "timestep": 0.25
      }
    }
    """)
    # Save network as an HTML file
    net.save_graph(f"static/{team_name}_network.html")
    return net, G

# Generate default starter list


def get_default_starters(season, team):
    return team_info_all[f"Season={season}"][team]["starter_info"]["starters"]


# Example usage
if __name__ == "__main__":
    season = "2023-24"
    team = "NYK"
    edge_info = "Pass Per Game"

    _, team_data, team_info = fetch_data(season, team)
    starters = get_default_starters(season, team)

    net, G = create_network(
        team_data, team, team_info["primary_color"], edge_info, starters)
    # print(G)
    # net.show("net.html")
