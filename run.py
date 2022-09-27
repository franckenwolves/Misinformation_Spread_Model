from virus_on_network.server import server
import sys
import socketserver

for i in range(8521, 8524):
    try:
        server.launch(i)
        port = i
    except:
        print(i, " is occupied")