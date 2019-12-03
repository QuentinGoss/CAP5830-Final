# Connection.py

import env
import pantherine as purr
import networkx as nx
import nxops
import math

class Connection(object):
    # @param int isrc = index of src poi
    # @param int idst = index of dst poi
    def __init__(self,isrc,idst):
        self.isrc = isrc            # Index of src
        self.idst = idst            # Index of dst
        self.src = env.names[isrc]  # Source POI node ID
        self.dst = env.names[idst]  # Destination POI node ID
        self.cost = -1              # Estimated Cost of trip (seconds)
        self.visits = 0             # Number of visits on this connection
        self.trails = []            # Log of time for every visit
        self.nids = []              # SUMO node IDS (for NX routing) 
        self.eids = []              # SUMO EIDS for SUMO routing
        return
    
    def as_dict(self):
        d = {
            "isrc":self.isrc,
            "idst":self.idst,
            "src":self.src,
            "dst":self.dst,
            "cost":self.cost,
            "visits":self.visits,
            "trails":self.trails,
            "nids":self.nids,
            "eids":self.eids
        }
        return d
    pass
    
def initialize():
    env.names = env.poi_ids
    env.names.append(env.start)
    n = 0; total = len(env.names) * len(env.names)
    for isrc, src in enumerate(env.names):
        row = []
        for idst, dst in enumerate(env.names):
            conn = Connection(isrc,idst)
            if isrc == idst:
                conn.cost = math.inf
            else:
                conn.nids = nx.dijkstra_path(env.nx,src,dst)
                conn.cost, conn.eids = nxops.path_info(env.nx,conn.nids)
            n += 1; purr.update(n,total,"Creating Connection Matrix ")
            continue
            env.connections.append(row)
        continue
    print("\nComplete!")
    return
