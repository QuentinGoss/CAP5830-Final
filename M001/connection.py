# Connection.py

import env
import pantherine as purr
import networkx as nx
import math
import atomicModel as am
import nxops

class Connection(am.AtomicModel):
    # @param int isrc = index of src poi
    # @param int idst = index of dst poi
    def __init__(self,name,isrc,idst):
        super().__init__(name)
        self.isrc = isrc            # Index of src
        self.idst = idst            # Index of dst
        self.src = env.names[isrc]  # Source POI node ID
        self.dst = env.names[idst]  # Destination POI node ID
        self.cost = -1              # Estimated Cost of trip (seconds)
        self.nids = []              # SUMO node IDS (for NX routing) 
        self.eids = []              # SUMO EIDS for SUMO routing
        self.rid = None             # SUMO Route ID
        self.visits = 0             # Number of visits on this connection
        self.trails = []            # Log of time for every visit
        self.trails_avg = 0.5       # Avg trails value
        # Normalized trails value
        self.trails_normal = 1 / math.pow(len(env.poi_ids),2)
        
        self.IN_PORT = "in"
        self.OUT_PORT = "out"
        self.in_port = self.add_in_port(self.IN_PORT)
        self.out_port = self.add_out_port(self.OUT_PORT)
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
        
    def delta_int(self):
        self.passivate()
        return
    
    def delta_ext(self):
        while len(self.in_ports[0].bag) > 0:
            veh = self.in_ports[0].bag.pop()
            # ~ print("\nReceived Vehicle %s at Connection %s!" % (veh.vid,self.name))
            self.trails.append(veh.dt)
            self.visits += 1
            self.trails_avg = sum(self.trails) / self.visits
            self.update_trails_norm
            veh.hop()
            env.ants.append(veh)
        # ~ purr.pause()
        return
        
    def delta_con(self):
        return
        
    def _lambda(self):
        return
    
    def update_trails_norm(self):
        total = 0
        for row in env.connections:
            for conn in row:
                if not conn.cost == math.inf:
                    total += conn.trails_avg
        self.trails_normal = self.trails_avg / total
        return
    pass
    
def initialize():
    env.connections = []
    env.names = env.poi_ids
    env.names.append(env.start)
    n = 0; total = len(env.names) * len(env.names)
    for isrc, src in enumerate(env.names):
        row = []
        for idst, dst in enumerate(env.names):
            conn = Connection("%s+%s" % (src,dst),isrc,idst)
            if isrc == idst:
                conn.cost = math.inf
            else:
                conn.nids = nx.dijkstra_path(env.nx,src,dst)
                conn.cost, conn.eids = nxops.path_info(env.nx,conn.nids)
                conn.rid = new_route(conn.eids)
            row.append(conn)
            n += 1; purr.update(n,total,"Creating Connection Matrix ")
            continue
        env.connections.append(row)
        continue
    print("\nComplete!")
    return

# Create a new Route with traci given Edge IDS
# @param [str] = List of Edge IDS
# @return str = routeid
def new_route(eids):
    rid = "route%d" % (env.route_id_counter)
    env.route_id_counter += 1
    env.traci.route.add(rid,eids)
    return rid
