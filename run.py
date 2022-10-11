from virus_on_network.server import server
import sys
import socketserver

for i in range(8521, 8524):
    try:
        server.launch(i)
        port = i
    except:
        print(i, " is occupied")




### START OF CODE FOR BATCH RUNNER

from virus_on_network.model import *
from virus_on_network.server import *
from numpy import arange
#import matplotlib.pyplot as plt
from mesa.batchrunner import BatchRunner

#fixed_params = {
    #"virus_spread_chance": 0.4,
    #"virus_check_frequency": 0.4,
    #"avg_node_degree": 3,
    #"initial_outbreak_size": 1,
#}

#variable_params = {
    #"number of agents": range(100, 100, 10),

#}

#num_iterations = 1
#num_steps = 30

#batch_run = BatchRunner(server,
                        #fixed_parameters=fixed_params,
                        #variable_parameters=variable_params,
                        #iterations=num_iterations,
                        #max_steps=num_steps,
                        #model_reporters=
                        #{
                            ###some form of csv file writer perhaps?...
                        #}
#)

#batch_run.run_all()