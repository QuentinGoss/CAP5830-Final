# env.py
options = None

# Random Seed
seed = None

# Routes
route_id_counter = 0

# Vehicles
veh_total = None      # Number of vehicles to simulate
veh_exists_max = None # Number of vehicles that may exist at any point in time.
veh_id_counter = 0

# Ant Vehicles
ant_id_counter = 0
ants = []           # List of all tracked ants
finished = []       # Container for finished ants

# Edge/Node dictionaries
edges = None # Edge dictionaries for every edge in the map
nodes = None # Node dictionaries for every node in the map

# Networkx graph
nx = None

# traci
traci = None

# POI
start = None    # Starting node ID
poi_file = None # File which has node IDS of POIs
poi_ids = None  # Node IDS of POIs
poi_nodes = None# Node dicts of each POI

# Connections
names = None     # Connection Matrix PID names
connections = [] # Connections Matrix

# States
iteration_ready = False
hop_ready = False
arrived = 0

# Output
out_dir = None
