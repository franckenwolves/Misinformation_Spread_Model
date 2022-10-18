import math
from enum import Enum
import networkx as nx
from virus_on_network import server
import mesa
import csv


class State(Enum):
    SUSCEPTIBLE = 0
    INFECTED = 1
    SKEPTICAL = 2
    EXPOSED = 3

def number_state(model, state):
    return sum(1 for a in model.grid.get_all_cell_contents() if a.state is state)


def number_infected(model, write_results = True):
    print("Infected: ", number_state(model, State.INFECTED))
    data = [number_state(model, State.INFECTED)]
    if write_results:
        with open('results_test.csv', 'a') as f:
            writer = csv.writer(f)
            for i in data:
                f.write("\t")
                f.write(str(data))
    return number_state(model, State.INFECTED)


def number_susceptible(model):
    print("Susceptible: ", number_state(model, State.SUSCEPTIBLE))
    data = [number_state(model, State.SUSCEPTIBLE)]
    with open('results_test.csv', 'a') as f:
        writer = csv.writer(f)
        for i in data:
            f.write("\t\t")
            f.write(str(data))
    return number_state(model, State.SUSCEPTIBLE)


def number_skeptical(model):
    print("Skeptical: ", number_state(model, State.SKEPTICAL))
    data = [number_state(model, State.SKEPTICAL)]
    with open('results_test.csv', 'a') as f:
        writer = csv.writer(f)
        for i in data:
            f.write("\t\t")
            f.write(str(data))
        
    return number_state(model, State.SKEPTICAL)

   
def number_exposed(model):
    print("Exposed: ", number_state(model, State.EXPOSED))
    data = [number_state(model, State.EXPOSED)]
    with open('results_test.csv', 'a') as f:
        writer = csv.writer(f)
        for i in data:
            f.write("\t\t")
            f.write(str(data))
        f.write("\n")
    return number_state(model, State.EXPOSED)


class VirusOnNetwork(mesa.Model):
    """A virus model with some number of agents"""

    def __init__(
        self,
        num_nodes=10,
        avg_node_degree=3,
        initial_outbreak_size=1,
        virus_spread_chance=0.4,
        virus_check_frequency=0.4,
        exposed_chance=0.3,
        #recovery_chance=0.3,
        gain_skeptical_chance=0.5,
    ):
        header = ['number infected', ' number susceptible', ' number skeptical', ' number exposed']
        with open('results_test.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow({'Batch: test'})
            writer.writerow({'Total Agents: ', num_nodes})
            writer.writerow({'Spread Chance: ', virus_spread_chance})
            writer.writerow({'Exposed Chance: ', exposed_chance})
            writer.writerow({'Node Degree: ', avg_node_degree})
            writer.writerow({'Initial Outbreak Size: ', initial_outbreak_size})
            writer.writerow(header)

        self.step_number = 0

        self.num_nodes = num_nodes
        prob = avg_node_degree / self.num_nodes
        self.G = nx.erdos_renyi_graph(n=self.num_nodes, p=prob)
        self.grid = mesa.space.NetworkGrid(self.G)
        self.schedule = mesa.time.RandomActivation(self)
        self.initial_outbreak_size = (
            initial_outbreak_size if initial_outbreak_size <= num_nodes else num_nodes
        )
        self.virus_spread_chance = virus_spread_chance
        self.virus_check_frequency = virus_check_frequency
        self.exposed_chance = exposed_chance
        self.gain_skeptical_chance = gain_skeptical_chance

        self.datacollector = mesa.DataCollector(
            {
                "Infected": number_infected,
                "Susceptible": number_susceptible,
                "Skeptical": number_skeptical,
                "Exposed": number_exposed,
            }
        )

        # Create agents
        for i, node in enumerate(self.G.nodes()):
            a = VirusAgent(
                i,
                self,
                State.SUSCEPTIBLE,
                self.virus_spread_chance,
                self.virus_check_frequency,
                self.exposed_chance,
                self.gain_skeptical_chance,
            )
            self.schedule.add(a)
            # Add the agent to the node
            self.grid.place_agent(a, node)


        skeptical_nodes = self.random.sample(list(self.G),(int(num_nodes*self.gain_skeptical_chance)))
        for a in self.grid.get_cell_list_contents(skeptical_nodes):
            a.state = State.SKEPTICAL
        """
        #Expose some nodes
        print(self.exposed_chance)
        print(list(self.G))
        print(self.initial_outbreak_size)
        exposed_nodes = self.random.sample(list(self.G), (int(num_nodes*self.exposed_chance)))
        for a in self.grid.get_cell_list_contents(exposed_nodes):
            a.state = State.EXPOSED
        """
        # Infect some nodes
        infected_nodes = self.random.sample(list(self.G), self.initial_outbreak_size)
        for a in self.grid.get_cell_list_contents(infected_nodes):
            a.state = State.INFECTED

        self.running = True
        self.datacollector.collect(self)

    def skeptical_susceptible_ratio(self):
        try:
            return number_state(self, State.SKEPTICAL) / number_state(
                self, State.SUSCEPTIBLE
            )
        except ZeroDivisionError:
            return math.inf

    def step(self):
        with open('results_test.csv', 'a') as f:
            f.write(str(self.step_number +1))
            f.write(",")
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        self.step_number = self.step_number +1

    def run_model(self, n):
        for i in range(n):
            self.step()

    def try_gain_skeptical(self):
        if self.random.random() < self.gain_skeptical_chance:
            self.state = State.SKEPTICAL


class VirusAgent(mesa.Agent):
    def __init__(
        self,
        unique_id,
        model,
        initial_state,
        virus_spread_chance,
        virus_check_frequency,
        exposed_chance,
        gain_skeptical_chance,
        trust_network=[],
    ):
        super().__init__(unique_id, model)

        self.state = initial_state

        self.virus_spread_chance = virus_spread_chance
        self.virus_check_frequency = virus_check_frequency
        self.exposed_chance = exposed_chance
        self.gain_skeptical_chance = gain_skeptical_chance

    
    def try_exposing(self):
        ## Try to expose
        neighbors_nodes = self.model.grid.get_neighbors(self.pos, include_center=True)
        susceptible_neighbors = [
            agent
            for agent in self.model.grid.get_cell_list_contents(neighbors_nodes)
            if agent.state is State.SUSCEPTIBLE
        ]
        for a in susceptible_neighbors:
            if self.random.random() < self.exposed_chance:
                a.state = State.EXPOSED

    def try_to_infect_neighbors(self):
        neighbors_nodes = self.model.grid.get_neighbors(self.pos, include_center=True)
        exposed_neighbors = [
            agent
            for agent in self.model.grid.get_cell_list_contents(neighbors_nodes)
            if agent.state is State.EXPOSED
        ]
        for a in exposed_neighbors:
            if self.random.random() < self.virus_spread_chance:
                a.state = State.INFECTED

    def try_gain_skeptical(self):
        if self.random.random() < self.gain_skeptical_chance:
            self.state = State.SKEPTICAL

    

    def try_check_situation(self):
        if self.random.random() < self.virus_check_frequency:
            # Checking...
            if self.state is State.SUSCEPTIBLE:
                self.try_to_infect_neighbors()
        elif self.state is State.EXPOSED:
            self.try_gain_skeptical()

    def step(self):
        if self.state is State.INFECTED:
            self.try_exposing()
        
        self.try_check_situation()

     
