pyOSPF
======
A python implementation of the OSPF Routing Protocol.
It's probably very inaccurate but i try to implement it as accurate as i can.
Its supposed to be used as an educational explanation of how OSPF works and not to be used as an emulator or anything like the CISCO emulators.

I am going to simulate 2 parts 
- Establishing router adjacency by the exchange of hello messages.
- Calculating Routing Table from the adjacency information.


#Step 0 : Defining Router Class
##Properties :
* Router class methods map router actions [ex : send hello message]
* Routers run in separate threads to emulate their parallelism in action.
* Routers write outputs in separate files to be monitored separately. [ a good enough solution for threads to write outputs with console interface. i use tail -f command to monitor the outputs.]
* Routers simulate physical connections.

#Step 1 : Establishing Router Adjacency
* Router thread keeps sending hello messages to physical connections [ this is simulated by running the send_hello method in connected routers ].
* Router receiving hello message adds the sender in his neighbours list .
* Router adds his neighbours neighbours to his adjacency list.
* after certain time each router creates a graph from the adjacency list and passes it to the Dijkstra's algorithm module.

#Step 2 : Election of DR , BDR [not implemented]
It needs a little bit of code do be done because it was initialy supported the Router priority is sent so its just the process of seleceting the highst priority .


#Step 3 : Calculating Routing Table

##Inputs : 
Adjacency Information from all adjacent routers in the form of a Graph G.

##Outputs : 
Generate the routing table for this node to all other nodes.

##Process : 
applying the implementation of Dijkstra's algorithm on the graph to generate the shortest path from the node to all other nodes in the AS.






