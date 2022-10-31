import math
from enum import Enum
import networkx as nx
from virus_on_network import server
import mesa
import csv


class State(Enum):
    SUSCEPTIBLE = 0
    EXPOSED_VIRUS_1_SUSCEPTIBLE_VIRUS_2 = 1
    EXPOSED_VIRUS_2_SUSCEPTIBLE_VIRUS_1 = 2
    EXPOSED_BOTH = 3
    INFECTED_VIRUS_1_SUSCEPTIBLE_VIRUS_2 = 4
    INFECTED_VIRUS_2_SUSCEPTIBLE_VIRUS_1 = 5
    INFECTED_VIRUS_1_EXPOSED_VIRUS_2 = 6
    INFECTED_VIRUS_2_EXPOSED_VIRUS_1 = 7
    SKEPTICAL = 8


def number_state(model, state):
    return sum(1 for a in model.grid.get_all_cell_contents() if a.state is state)


def number_infected_1_susceptible_2(model, write_results=True):
    print("Infected 1 Susceptible 2: ", number_state(model, State.INFECTED_VIRUS_1_SUSCEPTIBLE_VIRUS_2))
    data = [number_state(model, State.INFECTED_VIRUS_1_SUSCEPTIBLE_VIRUS_2)]
    if write_results:
        with open('results_test.csv', 'a') as f:
            writer = csv.writer(f)
            for i in data:
                f.write("\t")
                f.write(str(data))
    return number_state(model, State.INFECTED_VIRUS_1_SUSCEPTIBLE_VIRUS_2)


def number_infected_2_susceptible_1(model, write_results=True):
    print("Infected 2 Susceptible 1: ", number_state(model, State.INFECTED_VIRUS_2_SUSCEPTIBLE_VIRUS_1))
    data = [number_state(model, State.INFECTED_VIRUS_2_SUSCEPTIBLE_VIRUS_1)]
    if write_results:
        with open('results_test.csv', 'a') as f:
            writer = csv.writer(f)
            for i in data:
                f.write("\t")
                f.write(str(data))
    return number_state(model, State.INFECTED_VIRUS_2_SUSCEPTIBLE_VIRUS_1 )


def number_infected_1_exposed_2(model, write_results=True):
    print("Infected 1 Exposed 2: ", number_state(model, State.INFECTED_VIRUS_1_EXPOSED_VIRUS_2))
    data = [number_state(model, State.INFECTED_VIRUS_1_EXPOSED_VIRUS_2)]
    if write_results:
        with open('results_test.csv', 'a') as f:
            writer = csv.writer(f)
            for i in data:
                f.write("\t")
                f.write(str(data))
    return number_state(model, State.INFECTED_VIRUS_1_EXPOSED_VIRUS_2 )


def number_infected_2_exposed_1(model, write_results=True):
    print("Infected 2 Exposed 1: ", number_state(model, State.INFECTED_VIRUS_2_EXPOSED_VIRUS_1))
    data = [number_state(model, State.INFECTED_VIRUS_2_EXPOSED_VIRUS_1)]
    if write_results:
        with open('results_test.csv', 'a') as f:
            writer = csv.writer(f)
            for i in data:
                f.write("\t")
                f.write(str(data))
    return number_state(model, State.INFECTED_VIRUS_2_EXPOSED_VIRUS_1 )


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

   
def number_exposed_1_susceptible_2(model):
    print("Exposed 1 Susceptible 2: ", number_state(model, State.EXPOSED_VIRUS_1_SUSCEPTIBLE_VIRUS_2))
    data = [number_state(model, State.EXPOSED_VIRUS_1_SUSCEPTIBLE_VIRUS_2)]
    with open('results_test.csv', 'a') as f:
        writer = csv.writer(f)
        for i in data:
            f.write("\t\t")
            f.write(str(data))
        f.write("\n")
    return number_state(model, State.EXPOSED_VIRUS_1_SUSCEPTIBLE_VIRUS_2)


def number_exposed_2_susceptible_1(model):
    print("Exposed 2 Susceptible 1: ", number_state(model, State.EXPOSED_VIRUS_2_SUSCEPTIBLE_VIRUS_1))
    data = [number_state(model, State.EXPOSED_VIRUS_2_SUSCEPTIBLE_VIRUS_1)]
    with open('results_test.csv', 'a') as f:
        writer = csv.writer(f)
        for i in data:
            f.write("\t\t")
            f.write(str(data))
        f.write("\n")
    return number_state(model, State.EXPOSED_VIRUS_2_SUSCEPTIBLE_VIRUS_1)


def number_exposed_both(model):
    print("Exposed Both: ", number_state(model, State.EXPOSED_BOTH))
    data = [number_state(model, State.EXPOSED_BOTH)]
    with open('results_test.csv', 'a') as f:
        writer = csv.writer(f)
        for i in data:
            f.write("\t\t")
            f.write(str(data))
        f.write("\n")
    return number_state(model, State.EXPOSED_BOTH)


class VirusOnNetwork(mesa.Model):
    """A virus model with some number of agents"""

    def __init__(
        self,
        num_nodes=10,
        avg_node_degree=3,
        initial_outbreak_size_virus_1=1,
        initial_outbreak_size_virus_2=1,
        virus_1_spread_chance=0.4,
        virus_2_spread_chance=0.4,
        virus_check_frequency=0.4,
        exposed_chance_virus_1=0.3,
        exposed_chance_virus_2=0.3,
        #recovery_chance=0.3,
        gain_skeptical_chance=0.5,
        skeptical_level_virus_1=0.2,
        skeptical_level_virus_2=0.2,
    ):
        header = ['number infected', ' number susceptible', ' number skeptical', ' number exposed']
        with open('results_test.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow({'Batch: test'})
            writer.writerow({'Total Agents: ', num_nodes})
            writer.writerow({'Spread Chance Virus 1: ', virus_1_spread_chance})
            writer.writerow({'Spread Chance Virus 2: ', virus_2_spread_chance})
            writer.writerow({'Exposed Chance Virus 1: ', exposed_chance_virus_1})
            writer.writerow({'Exposed Chance Virus 2: ', exposed_chance_virus_2})
            writer.writerow({'Node Degree: ', avg_node_degree})
            writer.writerow({'Initial Outbreak Size Virus 1: ', initial_outbreak_size_virus_1})
            writer.writerow({'Initial Outbreak Size Virus 2: ', initial_outbreak_size_virus_2})
            #print("Number of Agents: ", num_nodes)
            #print("Skeptical_level: ", skeptical_level)
            #print("virus spread chance: ", virus_spread_chance)
            #print("exposed chance: ", exposed_chance)
            writer.writerow(header)

        self.step_number = 0

        self.num_nodes = num_nodes
        prob = avg_node_degree / self.num_nodes
        self.G = nx.erdos_renyi_graph(n=self.num_nodes, p=prob)
        self.grid = mesa.space.NetworkGrid(self.G)
        self.schedule = mesa.time.RandomActivation(self)
        self.initial_outbreak_size_virus_1 = (
            initial_outbreak_size_virus_1 if initial_outbreak_size_virus_1 <= num_nodes else num_nodes
        )
        self.initial_outbreak_size_virus_2 = (
            initial_outbreak_size_virus_2 if initial_outbreak_size_virus_2 <= num_nodes else num_nodes
        )
        self.virus_1_spread_chance = virus_1_spread_chance
        self.virus_2_spread_chance = virus_2_spread_chance
        self.virus_check_frequency = virus_check_frequency
        self.exposed_chance_virus_1 = exposed_chance_virus_1
        self.exposed_chance_virus_2 = exposed_chance_virus_2
        self.gain_skeptical_chance = gain_skeptical_chance
        self.skeptical_level_virus_1 = skeptical_level_virus_1
        self.skeptical_level_virus_2 = skeptical_level_virus_2
        self.datacollector = mesa.DataCollector(
            {
                #"Infected": number_infected,
                #"Susceptible": number_susceptible,
                #"Skeptical": number_skeptical,
                #"Exposed": number_exposed,

                'Susceptible': number_susceptible,
                'Exposed 1 and Susceptible 2': number_exposed_1_susceptible_2,
                'Exposed 2 and Susceptible 1': number_exposed_2_susceptible_1,
                'Exposed Both': number_exposed_both,
                'Infected 1 Susceptible 2': number_infected_1_susceptible_2,
                'Infected 2 Susceptible 1': number_infected_2_susceptible_1,
                'Infected 1 Exposed 2': number_infected_1_exposed_2,
                'Infected 2 Exposed 1': number_infected_2_exposed_1,
                'Skeptical': number_skeptical,
            }
        )

        # Create agents
        for i, node in enumerate(self.G.nodes()):
            a = VirusAgent(
                i,
                self,
                State.SUSCEPTIBLE,
                self.virus_1_spread_chance,
                self.virus_2_spread_chance,
                self.virus_check_frequency,
                self.exposed_chance_virus_1,
                self.exposed_chance_virus_2,
                self.gain_skeptical_chance,
                self.skeptical_level_virus_1,
                self.skeptical_level_virus_2,
            )
            self.schedule.add(a)
            # Add the agent to the node
            self.grid.place_agent(a, node)
        self.running = True
        self.datacollector.collect(self)

        # Previously used function to set a number of nodes to the skeptical state
        '''skeptical_nodes = self.random.sample(list(self.G), (int(num_nodes*self.gain_skeptical_chance)))
        for a in self.grid.get_cell_list_contents(skeptical_nodes):
            a.state = State.SKEPTICAL
            '''
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
        infected_nodes_1 = self.random.sample(list(self.G), self.initial_outbreak_size_virus_1)
        for a in self.grid.get_cell_list_contents(infected_nodes_1):
            a.state = State.INFECTED_VIRUS_1_SUSCEPTIBLE_VIRUS_2
            a.skeptical_level_virus_2 = .90
        infected_nodes_2 = self.random.sample(list(self.G), self.initial_outbreak_size_virus_2)
        for a in self.grid.get_cell_list_contents(infected_nodes_2):
            a.state = State.INFECTED_VIRUS_2_SUSCEPTIBLE_VIRUS_1
            a.skeptical_level_virus_1 = .90
        # Gives every node in the graph a level of skepticism
        skeptics1 = self.random.sample(list(self.G), self.num_nodes)
        f = 0
        for a in self.grid.get_cell_list_contents(skeptics1):
            if f <= (int(len(skeptics1)*.25)):
                a.skeptical_level_virus_1 = .20
                f += 1
            elif (int(len(skeptics1) * .25)) < f <= (int(len(skeptics1) * .50)):
                a.skeptical_level_virus_1 = .40
                f += 1
            elif (int(len(skeptics1) * .50)) < f <= (int(len(skeptics1) * .75)):
                a.skeptical_level_virus_1 = .60
                f += 1
            elif (int(len(skeptics1) * .75)) < f <= (int(len(skeptics1))):
                a.skeptical_level_virus_1 = .80
                f += 1

        skeptics2 = self.random.sample(list(self.G), self.num_nodes)
        f = 0
        for a in self.grid.get_cell_list_contents(skeptics2):
            if f <= (int(len(skeptics2) * .25)):
                a.skeptical_level_virus_2 = .20
                f += 1
            elif (int(len(skeptics2) * .25)) < f <= (int(len(skeptics2) * .50)):
                a.skeptical_level_virus_2 = .40
                f += 1
            elif (int(len(skeptics2) * .50)) < f <= (int(len(skeptics2) * .75)):
                a.skeptical_level_virus_2 = .60
                f += 1
            elif (int(len(skeptics2) * .75)) < f <= (int(len(skeptics2))):
                a.skeptical_level_virus_2 = .80
                f += 1

    '''def skeptical_susceptible_ratio(self):
        try:
            return number_state(self, State.SKEPTICAL) / number_state(
                self, State.SUSCEPTIBLE
            )
        except ZeroDivisionError:
            return math.inf'''

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

    '''def try_gain_skeptical(self):
        if self.random.random() < self.gain_skeptical_chance:
            self.state = State.SKEPTICAL'''


class VirusAgent(mesa.Agent):
    def __init__(
        self,
        unique_id,
        model,
        initial_state,
        virus_1_spread_chance,
        virus_2_spread_chance,
        virus_check_frequency,
        exposed_chance_virus_1,
        exposed_chance_virus_2,
        gain_skeptical_chance,
        skeptical_level_virus_1,
        skeptical_level_virus_2,
    ):
        super().__init__(unique_id, model)

        self.state = initial_state
        self.virus_1_spread_chance = virus_1_spread_chance
        self.virus_2_spread_chance = virus_2_spread_chance
        self.virus_check_frequency = virus_check_frequency
        self.exposed_chance_virus_1 = exposed_chance_virus_1
        self.exposed_chance_virus_2 = exposed_chance_virus_2
        self.gain_skeptical_chance = gain_skeptical_chance
        self.skeptical_level_virus_1 = skeptical_level_virus_1
        self.skeptical_level_virus_2 = skeptical_level_virus_2

    def try_exposing_to_virus_1(self):
        # Try to expose
        neighbors_nodes = self.model.grid.get_neighbors(self.pos, include_center=True)
        susceptible_neighbors = [
            agent
            for agent in self.model.grid.get_cell_list_contents(neighbors_nodes)
            if agent.state is State.SUSCEPTIBLE or State.INFECTED_VIRUS_2_SUSCEPTIBLE_VIRUS_1 or State.EXPOSED_VIRUS_2_SUSCEPTIBLE_VIRUS_1
        ]
        for a in susceptible_neighbors:
            if self.random.random() < self.exposed_chance_virus_1:
                if a.state is State.SUSCEPTIBLE:
                    a.state = State.EXPOSED_VIRUS_1_SUSCEPTIBLE_VIRUS_2
                if a.state is State.EXPOSED_VIRUS_2_SUSCEPTIBLE_VIRUS_1:
                    a.state = State.EXPOSED_BOTH
                if a.state is State.INFECTED_VIRUS_2_SUSCEPTIBLE_VIRUS_1:
                    a.state = State.INFECTED_VIRUS_2_EXPOSED_VIRUS_1

    def try_exposing_to_virus_2(self):
        # Try to expose
        neighbors_nodes = self.model.grid.get_neighbors(self.pos, include_center=True)
        susceptible_neighbors = [
            agent
            for agent in self.model.grid.get_cell_list_contents(neighbors_nodes)
            if agent.state is State.SUSCEPTIBLE or State.INFECTED_VIRUS_1_SUSCEPTIBLE_VIRUS_2 or State.EXPOSED_VIRUS_1_SUSCEPTIBLE_VIRUS_2
        ]
        for a in susceptible_neighbors:
            if self.random.random() < self.exposed_chance_virus_2:
                if a.state is State.SUSCEPTIBLE:
                    a.state = State.EXPOSED_VIRUS_2_SUSCEPTIBLE_VIRUS_1
                if a.state is State.EXPOSED_VIRUS_1_SUSCEPTIBLE_VIRUS_2:
                    a.state = State.EXPOSED_BOTH
                if a.state is State.INFECTED_VIRUS_1_SUSCEPTIBLE_VIRUS_2:
                    a.state = State.INFECTED_VIRUS_1_EXPOSED_VIRUS_2

    def try_to_infect_neighbors_with_virus_1(self):
        neighbors_nodes = self.model.grid.get_neighbors(self.pos, include_center=True)
        exposed_neighbors = [
            agent
            for agent in self.model.grid.get_cell_list_contents(neighbors_nodes)
            if agent.state is State.EXPOSED_BOTH or State.EXPOSED_VIRUS_1_SUSCEPTIBLE_VIRUS_2 or State.INFECTED_VIRUS_2_EXPOSED_VIRUS_1
        ]
        for a in exposed_neighbors:
            if self.random.random() < self.virus_1_spread_chance:
                if self.random.random() > self.skeptical_level_virus_1:
                    if a.state is State.EXPOSED_BOTH:
                        a.state = State.INFECTED_VIRUS_1_EXPOSED_VIRUS_2
                        if a.skeptical_level_virus_2 < .90:
                            a.skeptical_level_virus_2 = .90
                    if a.state is State.EXPOSED_VIRUS_1_SUSCEPTIBLE_VIRUS_2:
                        a.state = State.INFECTED_VIRUS_1_SUSCEPTIBLE_VIRUS_2
                        if a.skeptical_level_virus_2 < .90:
                            a.skeptical_level_virus_2 = .90
                    if a.state is State.INFECTED_VIRUS_2_EXPOSED_VIRUS_1:
                        a.state = State.INFECTED_VIRUS_1_EXPOSED_VIRUS_2
                        if a.skeptical_level_virus_2 < .90:
                            a.skeptical_level_virus_2 = .90

    def try_to_infect_neighbors_with_virus_2(self):
        neighbors_nodes = self.model.grid.get_neighbors(self.pos, include_center=True)
        exposed_neighbors = [
            agent
            for agent in self.model.grid.get_cell_list_contents(neighbors_nodes)
            if agent.state is State.EXPOSED_BOTH or State.EXPOSED_VIRUS_2_SUSCEPTIBLE_VIRUS_1 or State.INFECTED_VIRUS_1_EXPOSED_VIRUS_2
        ]
        for a in exposed_neighbors:
            if self.random.random() < self.virus_2_spread_chance:
                if self.random.random() > self.skeptical_level_virus_2:
                    if a.state is State.EXPOSED_BOTH:
                        a.state = State.INFECTED_VIRUS_2_EXPOSED_VIRUS_1
                        if a.skeptical_level_virus_1 < .90:
                            a.skeptical_level_virus_1 = .90
                    if a.state is State.EXPOSED_VIRUS_2_SUSCEPTIBLE_VIRUS_1:
                        a.state = State.INFECTED_VIRUS_2_SUSCEPTIBLE_VIRUS_1
                        if a.skeptical_level_virus_1 < .90:
                            a.skeptical_level_virus_1 = .90
                    if a.state is State.INFECTED_VIRUS_1_EXPOSED_VIRUS_2:
                        a.state = State.INFECTED_VIRUS_2_EXPOSED_VIRUS_1
                        if a.skeptical_level_virus_1 < .90:
                            a.skeptical_level_virus_1 = .90

    def try_gain_skeptical_virus_1(self):
        if self.random.random() < self.gain_skeptical_chance:
            if self.skeptical_level_virus_1 < 1:
                self.skeptical_level_virus_1 = self.skeptical_level_virus_1 + .10
            elif self.skeptical_level_virus_1 >= 1 and self.skeptical_level_virus_2 >= 1:
                self.state = State.SKEPTICAL

    def try_gain_skeptical_virus_2(self):
        if self.random.random() < self.gain_skeptical_chance:
            if self.skeptical_level_virus_2 < 1:
                self.skeptical_level_virus_2 = self.skeptical_level_virus_2 + .10
            elif self.skeptical_level_virus_1 == 1 and self.skeptical_level_virus_2 == 1:
                self.state = State.SKEPTICAL

    def try_check_situation(self):
        if self.random.random() < self.virus_check_frequency:
            # Checking...
            if self.state is State.EXPOSED_VIRUS_1_SUSCEPTIBLE_VIRUS_2:
                self.try_to_infect_neighbors_with_virus_1()
            elif self.state is State.EXPOSED_VIRUS_2_SUSCEPTIBLE_VIRUS_1:
                self.try_to_infect_neighbors_with_virus_2()
            # The following if statement needs to be reworked because as of now it gives priority to virus 1 to try to infect first
            elif self.state is State.EXPOSED_BOTH:
                self.try_to_infect_neighbors_with_virus_1()
                self.try_to_infect_neighbors_with_virus_2()
            elif self.state is State.INFECTED_VIRUS_1_EXPOSED_VIRUS_2:
                self.try_to_infect_neighbors_with_virus_2()
            elif self.state is State.INFECTED_VIRUS_2_EXPOSED_VIRUS_1:
                self.try_to_infect_neighbors_with_virus_1()
        elif self.state is State.EXPOSED_VIRUS_1_SUSCEPTIBLE_VIRUS_2:
            self.try_gain_skeptical_virus_1()
        elif self.state is State.EXPOSED_VIRUS_2_SUSCEPTIBLE_VIRUS_1:
            self.try_gain_skeptical_virus_2()
        elif self.state is State.EXPOSED_BOTH:
            self.try_gain_skeptical_virus_1()
            self.try_gain_skeptical_virus_2()
        elif self.state is State.INFECTED_VIRUS_1_EXPOSED_VIRUS_2:
            self.try_gain_skeptical_virus_2()
        elif self.state is State.INFECTED_VIRUS_2_EXPOSED_VIRUS_1:
            self.try_gain_skeptical_virus_1()

    def step(self):
        if self.state is State.INFECTED_VIRUS_1_EXPOSED_VIRUS_2:
            self.try_exposing_to_virus_1()
        elif self.state is State.INFECTED_VIRUS_2_EXPOSED_VIRUS_1:
            self.try_exposing_to_virus_2()
        elif self.state is State.INFECTED_VIRUS_1_SUSCEPTIBLE_VIRUS_2:
            self.try_exposing_to_virus_1()
        elif self.state is State.INFECTED_VIRUS_2_SUSCEPTIBLE_VIRUS_1:
            self.try_exposing_to_virus_2()

        self.try_check_situation()
