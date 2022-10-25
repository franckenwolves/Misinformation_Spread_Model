import math
import sys
import mesa
import socket
import errno

from .model import VirusOnNetwork, State, number_infected


def network_portrayal(G):
    # The model ensures there is always 1 agent per node

    def node_color(agent):
        return {State.INFECTED: "#FF0000", State.SUSCEPTIBLE: "#008000", State.EXPOSED: "#FFFC33"}.get(
            agent.state, "#808080"
        )

    def edge_color(agent1, agent2):
        if State.SKEPTICAL in (agent1.state, agent2.state):
            return "#000000"
        return "#e8e8e8"

    def edge_width(agent1, agent2):
        if State.SKEPTICAL in (agent1.state, agent2.state):
            return 3
        return 2

    def get_agents(source, target):
        return G.nodes[source]["agent"][0], G.nodes[target]["agent"][0]

    portrayal = dict()
    portrayal["nodes"] = [
        {
            "size": 6,
            "color": node_color(agents[0]),
            "tooltip": f"id: {agents[0].unique_id}<br>state: {agents[0].state.name}"
                       f"<br> skeptical level: {agents[0].skeptical_level}",
        }
        for (_, agents) in G.nodes.data("agent")
    ]

    portrayal["edges"] = [
        {
            "source": source,
            "target": target,
            "color": edge_color(*get_agents(source, target)),
            "width": edge_width(*get_agents(source, target)),
        }
        for (source, target) in G.edges
    ]

    return portrayal


network = mesa.visualization.NetworkModule(network_portrayal, 750, 750)
chart = mesa.visualization.ChartModule(
    [
        {"Label": "Infected", "Color": "#FF0000"},
        {"Label": "Susceptible", "Color": "#008000"},
        {"Label": "Exposed", "Color": "#FFFC33"},
        #{"Label": "Skeptical", "Color": "#808080"},
    ]
)


def get_skeptical_susceptible_ratio(model):
    ratio = model.skeptical_susceptible_ratio()
    ratio_text = "&infin;" if ratio is math.inf else f"{ratio:.2f}"
    infected_text = str(number_infected(model))

    return "Skeptical/Susceptible Ratio: {}<br>Infected Remaining: {}".format(
        ratio_text, infected_text
    )


model_params = {
    "num_nodes": mesa.visualization.Slider(
        "Number of agents",
        10,   #starting value
        10,   #beginning value of scale
        100,   #ending value of scale
        1,   #interval by which scale is increased
        description="Choose how many agents to include in the model",
    ),
    "avg_node_degree": mesa.visualization.Slider(
        "Avg Node Degree", 3, 3, 8, 1, description="Avg Node Degree"
    ),
    "initial_outbreak_size": mesa.visualization.Slider(
        "Initial Outbreak Size",
        1,
        1,
        10,
        1,
        description="Initial Outbreak Size",
    ),
    "virus_spread_chance": mesa.visualization.Slider(
        "Virus Spread Chance",
        0.4,
        0.0,
        1.0,
        0.1,
        description="Probability that susceptible neighbor will be infected",
    ),
    "virus_check_frequency": mesa.visualization.Slider(
        "Virus Check Frequency",
        0.4,
        0.0,
        1.0,
        0.1,
        description="Frequency the nodes check whether they are infected by " "a virus",
    ),
    "exposed_chance": mesa.visualization.Slider(
        "Exposed Chance",
        0.3,
        0.0,
        1.0,
        0.1,
        description="Probability that the individual will be exposed to the misinformation",
    ),

    "gain_skeptical_chance": mesa.visualization.Slider(
        "Gain Skeptical Chance",
        0.5,
        0.0,
        1.0,
        0.1,
        description="Probability that a recovered agent will become "
        "skeptical to this virus in the future",
    ),
}

server = mesa.visualization.ModularServer(
    VirusOnNetwork,
    [network, chart], #need to add ", get_skeptical_susceptible_ratio" to this line in between network and charty to get the original
    "Virus Model",
    model_params,
)





