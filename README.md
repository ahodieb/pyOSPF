pyOSPF
======
A python implementation of the OSPF Routing Protocol.
It's probably very inaccurate but i try to implement it as accurate as i can.
Its supposed to be used as an educational explanation of how OSPF works and not to be used as an emulator or anything like the CISCO emulators.

I have divided the OSPF operations to 5 different operations and theses steps might not get fully implemented as this is a college project and i might run out of time.

I'm going to start with Step 4 , because its the most important one.

#Step 0 : Defining Router Class
##Properties :
* Router class methods map router actions [ex : send hello message]
* Routers run in separate threads to emulate their parallelism in action.
* Routers write outputs in separate files to be monitored separately. [ a good enough solution for threads to write outputs with console interface. i use tail -f command to monitor the outputs.]

#Step 1 : Establishing Router Adjacency
#Step 2 : Election of DR , BDR
#Step 3 : Discovering Routes.



#Step 4 : Calculating Routing Table

##Inputs : 
Adjacency Information from all adjacent routers in the form of a Graph G.

##Outputs : 
Generate the routing table for this node to all other nodes.

##Process : 
applying the implementation of dijktra's algorithm on the graph to generate the shortest path from the node to all other nodes in the AS.


#Step 5 : Maintaining LSDB / Routing Table



