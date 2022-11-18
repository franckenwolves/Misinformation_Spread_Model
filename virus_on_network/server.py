import math
import sys
import mesa
import socket
import errno

from .model import VirusOnNetwork, State#, number_infected


def network_portrayal(G):
    # The model ensures there is always 1 agent per node

    def node_color(agent):
        return {State.SUSCEPTIBLE: "#008000", State.EXPOSED_VIRUS_1_SUSCEPTIBLE_VIRUS_2: "#FFFC33", State.EXPOSED_VIRUS_2_SUSCEPTIBLE_VIRUS_1: "#DF5FED", State.EXPOSED_BOTH: "#4A2804",
                State.INFECTED_VIRUS_1_SUSCEPTIBLE_VIRUS_2: "#FF0000", State.INFECTED_VIRUS_2_SUSCEPTIBLE_VIRUS_1: "#0D1FDE",
                State.INFECTED_VIRUS_2_EXPOSED_VIRUS_1: "#720F7D", State.INFECTED_VIRUS_1_EXPOSED_VIRUS_2: "#E66C20"
                }.get(
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
                       f"<br> skeptical level virus 1: {agents[0].skeptical_level_virus_1}"
                       f"<br> skeptical level virus 2: {agents[0].skeptical_level_virus_2}",
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
        {"Label": "Susceptible", "Color": "#008000"},
        {"Label": "Exposed 1 and Susceptible 2", "Color": "#FFFC33"},
        {"Label": "Exposed 2 and Susceptible 1", "Color": "#DF5FED"},
        {"Label": "Exposed Both", "Color": "#4A2804"},
        {"Label": "Infected 1 Susceptible 2", "Color": "#FF0000" },
        {"Label": "Infected 2 Susceptible 1", "Color": "#0D1FDE"},
        {"Label": "Infected 1 Exposed 2", "Color": "#E66C20"},
        {"Label": "Infected 2 Exposed 1", "Color": "#720F7D"},
        {"Label": "Skeptical", "Color": "#808080"},
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
        50,   #starting value
        10,   #beginning value of scale
        100,   #ending value of scale
        1,   #interval by which scale is increased
        description="Choose how many agents to include in the model",
    ),
    "avg_node_degree": mesa.visualization.Slider(
        "Avg Node Degree", 3, 3, 8, 1, description="Avg Node Degree"
    ),
    "initial_outbreak_size_virus_0": mesa.visualization.Slider(
        "Initial Outbreak Size Virus 0",
        1,
        1,
        10,
        1,
        description="Initial Outbreak Size of virus 0",
    ),
    "initial_outbreak_size_virus_1": mesa.visualization.Slider(
        "Initial Outbreak Size Virus 1",
        1,
        1,
        10,
        1,
        description="Initial Outbreak Size of virus 1",
    ),
    "virus_0_spread_chance": mesa.visualization.Slider(
        "Virus 0 Spread Chance",
        0.4,
        0.0,
        1.0,
        0.1,
        description="Probability that susceptible neighbor will be infected with virus 0",
    ),
    "virus_1_spread_chance": mesa.visualization.Slider(
        "Virus 1 Spread Chance",
        0.4,
        0.0,
        1.0,
        0.1,
        description="Probability that susceptible neighbor will be infected with virus 1",
    ),
    "virus_check_frequency": mesa.visualization.Slider(
        "Virus Check Frequency",
        0.4,
        0.0,
        1.0,
        0.1,
        description="Frequency the nodes check whether they are infected by " "a virus",
    ),
    "exposed_chance_virus_0": mesa.visualization.Slider(
        "Exposed Chance Virus 0",
        0.3,
        0.0,
        1.0,
        0.1,
        description="Probability that the individual will be exposed to this virus",
    ),
    "exposed_chance_virus_1": mesa.visualization.Slider(
        "Exposed Chance Virus 1",
        0.3,
        0.0,
        1.0,
        0.1,
        description="Probability that the individual will be exposed to this virus",
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





