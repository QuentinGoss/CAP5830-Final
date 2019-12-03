# vehicle.py

import env
import pantherine as purr

class Vehicle(object):
    # @param vid = ID (Not the sumo ID)
    def __init__(self,vid):
        self.vid = vid       # ID (Not the SUMO ID)
        self.sumo_vid = None # SUMO ID
        self.pois_visited = [env.start] # POIs visited
        return
    
    
    pass

# Run 1 set of N vehicles through the map.
def itertation():
    return
