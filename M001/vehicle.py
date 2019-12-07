# vehicle.py

import env
import pantherine as purr
import random

class Vehicle(object):
    # @param vid = ID (Not the sumo ID)
    def __init__(self,vid):
        self.vid = vid         # ID (Not the SUMO ID)
        self.sumo_vid = None   # SUMO ID
        # index of POIs left to visit
        self.pois2visit = list(range(1,len(env.names)))
        self.pois_visited = [(0,0)]# Pois that have been visited (id,dt)
        self.loc = 0           # Current Location 
        self.dst = None        # Next Destination
        self.C = None          # C
        self.P = None          # P
        self.time_leave = None # Time when the vehicle leaves a node
        self.time_arrive = None# Time when the vehicle arrives at a node
        self.dt = None         # Length of Time veh spent traveling
        self.is_veh_departed = False # Has the vehicle been spawned yet?
        return
    
    def as_dict(self):
        d = {
            "vid":self.vid,
            "sumo_vid":self.sumo_vid,
            "pois2visit":self.pois2visit,
            "pois_visited":self.pois_visited,
            "loc":self.loc,
            "dst":self.dst,
            "C":self.C,
            "P":self.P
        }
        return d
    
    # 1 hop (a single decison of which node to go to)
    def hop(self):
        env.hop_ready = False
        self.update_C()
        self.update_P()
        self.dst = self.lottery()
        self.add()
        self.time_leave = env.n_step
        return
    
    def arrive(self):
        self.is_veh_departed = False
        self.time_arrive = env.n_step
        self.dt = self.time_arrive - self.time_leave
        self.pois_visited.append((self.dst,self.dt))
        # No place left to visit
        if len(self.pois2visit) == 0:
            env.finished.append(self)
            # ~ print("\n\nVehicle %s Complete!" % (self.vid))
            # ~ print("Route ",self.pois_visited)
            # ~ print("\n\n")
            # ~ purr.pause()
        # Hop into the bag of the connection
        else:
            env.connections[self.loc][self.dst].in_ports[0].bag.append(self)
        return
    
    def check_if_arrived(self):
        try:
            env.traci.vehicle.getSpeed(self.sumo_vid)
        except env.traci.exceptions.TraCIException:
            self.arrive()
            return True
        return False
        
    def check_if_departed(self):
        if self.is_veh_departed:
            return True
        elif not self.is_veh_departed and self.sumo_vid in env.traci.vehicle.getIDList():
            self.is_veh_departed = True
            return True
        return False
    
    def add(self):
        index = env.veh_id_counter
        env.veh_id_counter += 1
        self.sumo_vid = "veh%d" % (index)
        env.traci.vehicle.add(self.sumo_vid,env.connections[self.loc][self.dst].rid)
        return
    
    def update_C(self):
        self.C = []
        for i,ipoi in enumerate(self.pois2visit):
            conn = env.connections[self.loc][ipoi]
            self.C.append(conn.cost * conn.trails_normal)
        return
    
    def update_P(self):
        sumC = sum(self.C)
        self.P = [Ci/sumC for Ci in self.C]
        return
    
    # Determine where to go with a random lottery
    def lottery(self):
        big_num = 1000
        tickets = [int(big_num * Pi) for Pi in self.P]
        tickets_interval = []
        total = 0
        for n in tickets:
            total += n
            tickets_interval.append(total)
        val = random.randint(0,max(tickets_interval))
        for i,n in enumerate(tickets_interval):
            val -= n
            if val <= 0:
                return self.pois2visit.pop(i)
            continue
        raise ValueError
    pass

# Run 1 set of N vehicles through the map.
def iteration():
    env.iteration_ready = False
    for n in range(env.veh_exists_max):
        index = env.ant_id_counter
        env.ant_id_counter += 1
        vid = "ant%d" % (index)
        env.ants.append(Vehicle(vid))
        continue
    [env.ants[i].hop() for i,veh in enumerate(env.ants)]
    return

# Checks for arrival every timestep
def arrival_check():
    new_ants = []
    for i,ant in enumerate(env.ants):
        if env.ants[i].check_if_departed() and env.ants[i].check_if_arrived():
            env.arrived += 1
        else:
            new_ants.append(env.ants[i])
    env.ants = new_ants
    return

# Write data to csv
def csv():
    print("Writing vehicles.csv...",end='')
    veh_csv = "%s/vehicles.csv" % (env.out_dir)
    with open(veh_csv,'w') as f:
        f.write("ROUTE,POI0,POI1,POI2,POI3,POI4,POI5,POI6,POI7,POI8,POI9,POI10,COST\n")
        for veh in env.finished:
            route = "0"
            total_cost = 0
            for record in veh.pois_visited:
                index, cost = record
                if index == 10:
                    route += "A"
                else:
                    route += "%d" % (index)
                total_cost += cost
                continue
            f.write("%s" % (route))
            for record in veh.pois_visited:
                index, cost = record
                f.write(",%d" % (index))
            f.write(",%d\n" % (total_cost))
            continue
        pass
        print("COMPLETE!")
    return
