import math
from enum import Enum
import networkx as nx
from virus_on_network import server
import mesa
import csv
import copy
import time
from datetime import date
import pandas as pd

t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)

today = date.today()


def batch_csv():
    filename = str(today)
    new_batch_csv = (str(filename + '.csv'))
    with open(new_batch_csv, 'w') as f:
        f.write(",")


class VirusOnNetwork(mesa.Model):
    """A virus model with some number of agents"""

    # create_csv()

    def __init__(
            self,
            j=0,
            virus=0,
            num_nodes=10,
            avg_node_degree=3,
            initial_outbreak_size_virus_0=1,
            initial_outbreak_size_virus_1=1,
            initial_outbreak_size_virus_2=1,
            virus_0_spread_chance=1,
            virus_1_spread_chance=1,
            virus_2_spread_chance=1,
            virus_0_check_frequency=0.4,
            virus_1_check_frequency=0.4,
            virus_2_check_frequency=0.4,
            exposed_chance_virus_0=1,
            exposed_chance_virus_1=1,
            exposed_chance_virus_2=1,
            gain_skeptical_chance_virus_0=0.5,
            gain_skeptical_chance_virus_1=0.5,
            gain_skeptical_chance_virus_2=0.5,
            skeptical_level_virus_0=0,
            skeptical_level_virus_1=0,
            skeptical_level_virus_2=0,
    ):
        self.misinformation = {0: {'infected': 'no', 'exposed': 'no', 'initial_outbreak_size': 1, 'spread_chance': 1, 'exposed_chance': 1, 'skeptical_level': 0, 'virus_check_frequency': 0, 'gain_skeptical_chance': 1, 'opposite_virus': 1,
                                   'infected_list': [], 'num_virus': 1},
                               1: {'infected': 'no', 'exposed': 'no', 'initial_outbreak_size': 1, 'spread_chance': 1, 'exposed_chance': 1, 'skeptical_level': 0, 'virus_check_frequency': 0, 'gain_skeptical_chance': 1, 'opposite_virus': 0,
                                   },
                               2: {'infected': 'no', 'exposed': 'no', 'initial_outbreak_size': 1, 'spread_chance': 1, 'exposed_chance': 1, 'skeptical_level': 0, 'virus_check_frequency': 0, 'gain_skeptical_chance': 1, 'opposite_virus': None,
                                   }}

        # print("debug: ", self.misinformation)
        # header = ['number infected', ' number susceptible', ' number skeptical', ' number exposed']
        # with open('results_test.csv', 'w', newline='') as f:
        # writer = csv.writer(f)
        # writer.writerow({'Batch: test'})
        # writer.writerow({'Total Agents: ', num_nodes})
        # writer.writerow({'Spread Chance Virus 1: ', virus_1_spread_chance})
        # writer.writerow({'Spread Chance Virus 2: ', virus_2_spread_chance})
        # writer.writerow({'Exposed Chance Virus 1: ', exposed_chance_virus_1})
        # writer.writerow({'Exposed Chance Virus 2: ', exposed_chance_virus_2})
        # writer.writerow({'Node Degree: ', avg_node_degree})
        # writer.writerow({'Initial Outbreak Size Virus 1: ', initial_outbreak_size_virus_1})
        # writer.writerow({'Initial Outbreak Size Virus 2: ', initial_outbreak_size_virus_2})
        # print("Number of Agents: ", num_nodes)
        # print("Skeptical_level: ", skeptical_level)
        # print("virus spread chance: ", virus_spread_chance)
        # print("exposed chance: ", exposed_chance)
        # writer.writerow(header)

        self.step_number = 0
        self.num_nodes = num_nodes
        prob = avg_node_degree / self.num_nodes
        self.G = nx.erdos_renyi_graph(n=self.num_nodes, p=prob, directed=True)
        self.grid = mesa.space.NetworkGrid(self.G)
        self.schedule = mesa.time.RandomActivation(self)
        self.j = j
        self.virus = virus
        self.initial_outbreak_size_virus_0 = initial_outbreak_size_virus_0
        self.misinformation[0]['initial_outbreak_size'] = (
            initial_outbreak_size_virus_0 if initial_outbreak_size_virus_0 <= num_nodes else num_nodes
        )
        self.initial_outbreak_size_virus_1 = initial_outbreak_size_virus_1
        self.misinformation[1]['initial_outbreak_size'] = (
            initial_outbreak_size_virus_1 if initial_outbreak_size_virus_1 <= num_nodes else num_nodes
        )
        self.initial_outbreak_size_virus_2 = initial_outbreak_size_virus_2
        self.misinformation[2]['initial_outbreak_size'] = (
            initial_outbreak_size_virus_2 if initial_outbreak_size_virus_2 <= num_nodes else num_nodes
        )
        self.misinformation[0]['num_virus'] = j
        self.virus_0_spread_chance = virus_0_spread_chance
        self.misinformation[0]['spread_chance'] = virus_0_spread_chance
        self.virus_1_spread_chance = virus_1_spread_chance
        self.misinformation[1]['spread_chance'] = virus_1_spread_chance
        self.virus_2_spread_chance = virus_2_spread_chance
        self.misinformation[2]['spread_chance'] = virus_2_spread_chance
        self.virus_0_check_frequency = virus_0_check_frequency
        self.misinformation[0]['virus_check_frequency'] = virus_0_check_frequency
        self.virus_1_check_frequency = virus_1_check_frequency
        self.misinformation[1]['virus_check_frequency'] = virus_1_check_frequency
        self.virus_2_check_frequency = virus_2_check_frequency
        self.misinformation[2]['virus_check_frequency'] = virus_2_check_frequency
        self.exposed_chance_virus_0 = exposed_chance_virus_0
        self.misinformation[0]['exposed_chance'] = exposed_chance_virus_0
        self.exposed_chance_virus_1 = exposed_chance_virus_1
        self.misinformation[1]['exposed_chance'] = exposed_chance_virus_1
        self.exposed_chance_virus_2 = exposed_chance_virus_2
        self.misinformation[2]['exposed_chance'] = exposed_chance_virus_2
        self.gain_skeptical_chance_virus_0 = gain_skeptical_chance_virus_0
        self.misinformation[0]['gain_skeptical_chance'] = gain_skeptical_chance_virus_0
        self.gain_skeptical_chance_virus_1 = gain_skeptical_chance_virus_1
        self.misinformation[1]['gain_skeptical_chance'] = gain_skeptical_chance_virus_1
        self.gain_skeptical_chance_virus_2 = gain_skeptical_chance_virus_2
        self.misinformation[2]['gain_skeptical_chance'] = gain_skeptical_chance_virus_2
        self.skeptical_level_virus_0 = skeptical_level_virus_0
        self.misinformation[0]['skeptical_level'] = skeptical_level_virus_0
        self.skeptical_level_virus_1 = skeptical_level_virus_1
        self.misinformation[1]['skeptical_level'] = skeptical_level_virus_1
        self.skeptical_level_virus_2 = skeptical_level_virus_2
        self.misinformation[2]['skeptical_level'] = skeptical_level_virus_2
        self.datacollector = mesa.DataCollector(
            {
                # "Infected": number_infected,
                # "Susceptible": number_susceptible,
                # "Skeptical": number_skeptical,
                # "Exposed": number_exposed,

                # 'Susceptible': (self.misinformation[0]['exposed']=='no' and self.misinformation[1]['exposed']=='no'),
                # 'Exposed 0 and Susceptible 1': (self.misinformation[0]['exposed']=='yes' and self.misinformation[1]['exposed'])=='no',
                # 'Exposed 1 and Susceptible 0': (self.misinformation[0]['exposed']=='no' and self.misinformation[1]['exposed'])=='yes',
                # 'Exposed Both': (self.misinformation[0]['exposed']=='yes' and self.misinformation[1]['exposed'])=='yes',
                # 'Infected 0 Susceptible 1': (self.misinformation[0]['infected']=='yes' and self.misinformation[1]['exposed'])=='no',
                # 'Infected 1 Susceptible 0': (self.misinformation[0]['exposed']=='no' and self.misinformation[1]['infected'])=='yes',
                # 'Infected 0 Exposed 1': (self.misinformation[0]['infected']=='yes' and self.misinformation[1]['exposed'])=='yes',
                # 'Infected 1 Exposed 0': (self.misinformation[0]['exposed']=='yes' and self.misinformation[1]['infected'])=='yes',
                # Skeptical': number_skeptical,
            }
        )

        # Create agents
        for i, node in enumerate(self.G.nodes()):
            a = VirusAgent(
                i,
                self,
                self.j,
                self.virus,
                self.initial_outbreak_size_virus_0,
                self.initial_outbreak_size_virus_1,
                self.initial_outbreak_size_virus_2,
                self.virus_0_spread_chance,
                self.virus_1_spread_chance,
                self.virus_2_spread_chance,
                self.virus_0_check_frequency,
                self.virus_1_check_frequency,
                self.virus_2_check_frequency,
                self.exposed_chance_virus_0,
                self.exposed_chance_virus_1,
                self.exposed_chance_virus_2,
                self.gain_skeptical_chance_virus_0,
                self.gain_skeptical_chance_virus_1,
                self.gain_skeptical_chance_virus_2,
                self.skeptical_level_virus_0,
                self.skeptical_level_virus_1,
                self.skeptical_level_virus_2,
            )
            self.schedule.add(a)
            # Add the agent to the node
            self.grid.place_agent(a, node)
        self.running = True
        self.datacollector.collect(self)

        #print(self.G.nodes)
        print(self.G.number_of_edges(), '\n')

        with open('edgelist.csv', 'w') as f:
            for i in self.G.edges:
                #print(i)
                f.write('|')
                g=0
                for u in i:
                    g=g+1
                    #print(u)
                    f.write(str(u))
                    if (g%2) != 0:
                        f.write(',')

        def create_bidirectional_edges_with_weights(G):
            for edge in G.edges:
                x=str(edge)
                x=x[1:]
                x=x[:-1]
                a=x.split(',')[0]
                b=x.split(',')[-1]
                G[int(a)][int(b)]['weight'] = 0
                if G.has_edge(int(b), int(a)) is False:
                    G.add_edge(int(b), int(a))
                    G[int(b)][int(a)]['weight'] = 0

        create_bidirectional_edges_with_weights(self.G)

        # Infect some nodes
        for i in self.misinformation:
            if i < self.misinformation[0]['num_virus']:
                infected_nodes = self.random.sample(list(self.G), self.misinformation[i]['initial_outbreak_size'])
                # print(infected_nodes)
                for a in self.grid.get_cell_list_contents(infected_nodes):
                    # print(a.unique_id)
                    # print(a.misinformation)
                    a.misinformation[i]['infected'] = 'yes'
                    a.misinformation[i]['exposed'] = 'yes'
                    a.misinformation[0]['infected_list'].append(i)
                    # print(a.misinformation)
                    if a.misinformation[i]['opposite_virus'] is not None:
                        a.misinformation[a.misinformation[i]['opposite_virus']]['skeptical_level'] = .90
                        a.misinformation[a.misinformation[i]['opposite_virus']]['infected'] = 'no'

        # Gives every node in the graph a level of skepticism
        for i in self.misinformation:
            if i < self.misinformation[0]['num_virus']:
                skeptics = self.random.sample(list(self.G), self.num_nodes)
                f = 0
                for a in self.grid.get_cell_list_contents(skeptics):
                    if f <= (int(len(skeptics) * .25)):
                        a.misinformation[i]['skeptical_level'] = .20
                        f += 1
                    elif (int(len(skeptics) * .25)) < f <= (int(len(skeptics) * .50)):
                        a.misinformation[i]['skeptical_level'] = .40
                        f += 1
                    elif (int(len(skeptics) * .50)) < f <= (int(len(skeptics) * .75)):
                        a.misinformation[i]['skeptical_level'] = .60
                        f += 1
                    elif (int(len(skeptics) * .75)) < f <= (int(len(skeptics))):
                        a.misinformation[i]['skeptical_level'] = .80
                        f += 1

    def infected_nodes(self, i):
        infected_nodes = {0: [], 1: [], 2: []}
        for a in self.grid.get_cell_list_contents(self.G.nodes):
            if a.misinformation[i]['infected'] == 'yes':
                infected_nodes[i].append(a.unique_id)
        return infected_nodes[i]

    def exposed_nodes(self, i):
        exposed_nodes = {0: [], 1: [], 2: []}
        for a in self.grid.get_cell_list_contents(self.G.nodes):
            if a.misinformation[i]['exposed'] == 'yes':
                exposed_nodes[i].append(a.unique_id)
        return exposed_nodes[i]

    with open('infected.csv', 'w') as f:
        with open('exposed.csv', 'w') as e:
            with open('dictionary.csv', 'w') as d:

                def step(self):
                    self.schedule.step()
                    # collect data
                    self.datacollector.collect(self)
                    self.step_number = self.step_number + 1
                    #print(self.G.nodes)
                    #print(self.misinformation)
                    # print(self.G.edges)
                    # print(today, current_time)
                    with open('dictionary.csv', 'a') as d:
                        #d.write(str(self.step_number))
                        d.write('\n')
                    for i in self.grid.get_cell_list_contents(self.G.nodes):
                        print(i.unique_id)
                        print(i.misinformation)
                        with open('dictionary.csv', 'a') as d:
                            #d.write(str(i.unique_id))
                            d.write(str(i.misinformation))
                            d.write('\n')

                        #with open('dictionary.csv', 'w') as d:
                            #d.write()

                    for i in self.misinformation:
                        if i < self.misinformation[0]['num_virus']:
                            #print("List of infected nodes for virus", i, ": ", self.infected_nodes(i))

                            with open('infected.csv', 'a') as f:
                                f.write(str(self.step_number))
                                f.write(',')
                                f.write(str(i))
                                f.write(':')
                                f.write(str(self.infected_nodes(i)))
                                f.write('\n')

                    for i in self.misinformation:
                        if i < self.misinformation[0]['num_virus']:
                            #print("List of exposed nodes for virus", i, ": ", self.exposed_nodes(i))

                            with open('exposed.csv', 'a') as e:
                                e.write(str(self.step_number))
                                e.write(',')
                                e.write(str(i))
                                e.write(':')
                                e.write(str(self.exposed_nodes(i)))
                                e.write('\n')

    def run_model(self, n):
        for i in range(n):
            self.step()


class VirusAgent(mesa.Agent):

    def __init__(
            self,
            unique_id,
            model,
            j,
            virus,
            initial_outbreak_size_virus_0,
            initial_outbreak_size_virus_1,
            initial_outbreak_size_virus_2,
            virus_0_spread_chance,
            virus_1_spread_chance,
            virus_2_spread_chance,
            virus_0_check_frequency,
            virus_1_check_frequency,
            virus_2_check_frequency,
            exposed_chance_virus_0,
            exposed_chance_virus_1,
            exposed_chance_virus_2,
            gain_skeptical_chance_virus_0,
            gain_skeptical_chance_virus_1,
            gain_skeptical_chance_virus_2,
            skeptical_level_virus_0,
            skeptical_level_virus_1,
            skeptical_level_virus_2,
    ):

        super().__init__(unique_id, model)
        self.misinformation = {0: {'infected': 'no', 'exposed': 'no', 'initial_outbreak_size': 1, 'spread_chance': 1, 'exposed_chance': 1, 'skeptical_level': 0, 'virus_check_frequency': 0, 'gain_skeptical_chance': 1, 'opposite_virus': 1,
                                   'infected_list': [], 'num_virus': 1},
                               1: {'infected': 'no', 'exposed': 'no', 'initial_outbreak_size': 1, 'spread_chance': 1, 'exposed_chance': 1, 'skeptical_level': 0, 'virus_check_frequency': 0, 'gain_skeptical_chance': 1, 'opposite_virus': 0,
                                   },
                               2: {'infected': 'no', 'exposed': 'no', 'initial_outbreak_size': 1, 'spread_chance': 1, 'exposed_chance': 1, 'skeptical_level': 0, 'virus_check_frequency': 0, 'gain_skeptical_chance': 1, 'opposite_virus': None,
                                   }}

        self.virus = virus
        self.misinformation[0]['num_virus'] = j
        self.misinformation[0]['initial_outbreak_size'] = initial_outbreak_size_virus_0
        self.misinformation[1]['initial_outbreak_size'] = initial_outbreak_size_virus_1
        self.misinformation[2]['initial_outbreak_size'] = initial_outbreak_size_virus_2
        self.misinformation[0]['virus_check_frequency'] = virus_0_check_frequency
        self.misinformation[1]['virus_check_frequency'] = virus_1_check_frequency
        self.misinformation[2]['virus_check_frequency'] = virus_2_check_frequency
        self.misinformation[0]['spread_chance'] = virus_0_spread_chance
        self.misinformation[1]['spread_chance'] = virus_1_spread_chance
        self.misinformation[2]['spread_chance'] = virus_2_spread_chance
        self.misinformation[0]['exposed_chance'] = exposed_chance_virus_0
        self.misinformation[1]['exposed_chance'] = exposed_chance_virus_1
        self.misinformation[2]['exposed_chance'] = exposed_chance_virus_2
        self.misinformation[0]['gain_skeptical_chance'] = gain_skeptical_chance_virus_0
        self.misinformation[1]['gain_skeptical_chance'] = gain_skeptical_chance_virus_1
        self.misinformation[2]['gain_skeptical_chance'] = gain_skeptical_chance_virus_2
        self.misinformation[0]['skeptical_level'] = skeptical_level_virus_0
        self.misinformation[1]['skeptical_level'] = skeptical_level_virus_1
        self.misinformation[2]['skeptical_level'] = skeptical_level_virus_2

    def try_exposing(self, i):
        # Try to expose
        neighbors_nodes = self.model.grid.get_neighbors(self.pos, include_center=True)
        susceptible_neighbors = [
            agent
            for agent in self.model.grid.get_cell_list_contents(neighbors_nodes)
            if agent.misinformation[i]['exposed'] == 'no' and agent.misinformation[i]['infected'] == 'no'
        ]
        for a in susceptible_neighbors:
            if self.random.random() < self.misinformation[i]['skeptical_level']:
                a.misinformation[i]['exposed'] = 'yes'

    def try_to_infect_neighbors(self, i):
        neighbors_nodes = self.model.grid.get_neighbors(self.pos, include_center=True)
        exposed_neighbors = [
            agent
            for agent in self.model.grid.get_cell_list_contents(neighbors_nodes)
            if agent.misinformation[i]['exposed'] == 'yes' and agent.misinformation[i]['infected'] == 'no'
        ]
        for a in exposed_neighbors:
            if self.random.random() < self.misinformation[i]['spread_chance']:
                if self.random.random() > self.misinformation[i]['skeptical_level']:
                    a.misinformation[i]['infected'] = 'yes'
                    a.misinformation[0]['infected_list'].append(i)
                    a.misinformation[i]['exposed'] = 'no'
                    if a.misinformation[i]['opposite_virus'] is not None:
                        a.misinformation[a.misinformation[i]['opposite_virus']]['skeptical_level'] = .90
                        if a.misinformation[a.misinformation[i]['opposite_virus']]['infected'] == 'yes':
                            a.misinformation[a.misinformation[i]['opposite_virus']]['infected'] = 'no'

    def try_gain_skeptical(self, i):
        if self.random.random() < self.misinformation[i]['gain_skeptical_chance']:
            if self.misinformation[i]['skeptical_level'] < .91:
                self.misinformation[i]['skeptical_level'] = self.misinformation[i]['skeptical_level'] + .10
            else:
                self.misinformation[i]['skeptical_level'] = 1

    def try_check_situation(self, i):
        if self.random.random() < self.misinformation[i]['virus_check_frequency']:
            # Checking...
            if self.misinformation[i]['infected'] == 'yes':
                self.try_to_infect_neighbors(i)
        elif self.misinformation[i]['exposed'] == 'yes':
            self.try_gain_skeptical(i)

    def step(self):

        for i in self.misinformation:
            if i < self.misinformation[0]['num_virus']:
                if self.misinformation[i]['infected'] == 'yes':
                    self.try_exposing(i)
        for i in self.misinformation:
            if i < self.misinformation[0]['num_virus']:
                self.try_check_situation(i)

    def step2(self):

        for i in self.misinformation:
            if i < self.misinformation[0]['num_virus']:
                if self.misinformation[i]['infected'] == 'yes':
                    self.try_exposing(i)
        for i in self.misinformation:
            if i < self.misinformation[0]['num_virus']:
                self.try_check_situation(i)
