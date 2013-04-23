pyOSPF
======
A python implementation of the OSPF Routing Protocol.
It's proboably very inacurate but i try to implement it as accurate as i can.
Its supposed to be used as an educational explaniation of how OSPF works and not to be used as an emulator or anything like the CISCO emulators.

I have divided the OSPF operations to 5 diffrent operations and theses steps might not get fully implemented as this is a college project and i might run out of time.

I'm going to start with Step 4 , because its the most important one.

#Step 1 : Establishing Router Adjecency
#Step 2 : Election of DR , BDR
#Step 3 : Discovering Routes.



#Step 4 : Calculting Routing Table

##Inputs : 
Adjacency Information from all adjecent routers in the form of a Graph G.

##Outputs : 
Generate the routing table for this node to all other nodes.

##Proceess : 
applaying the implimentation of dijktra's algorithm on the graph to generate the shortest path from the node to all other nodes in the AS.


#Step 5 : Maintaing LSDB / Routing Table
