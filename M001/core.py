import env
import os
import pantherine as purr
import preprocess
import poi
import connection
import vehicle

###############################
# Initilize anything that needs to happen at step 0 here.
###############################
def initialize(traci):
    os.system("cls")
    print("Initializing...")
    
    env.traci = traci
    env.n_step = 0
    preprocess.initialize_nx()
    preprocess.initialize_edges_and_nodes()
    poi.initialize()
    connection.initialize()
    env.iteration_ready = True
    # ~ purr.pause()

    print("Initialization complete!")
    return
# end def intialize


###############################
# Anything that happens within the TraCI control loop goes here.
# One pass of the loop == 1 timestep.
# Return False to finalize the simulation
###############################
def timestep(traci,n_step):
    env.n_step = n_step
    
    # Vehicle 
    if env.iteration_ready:
        vehicle.iteration()
        
    vehicle.arrival_check()
    if len(env.finished) >= env.veh_total:
        return False
                
    # Connection
    for irow,row in enumerate(env.connections):
        for icol,conn in enumerate(row):
            if env.connections[irow][icol].check_for_event() or env.connections[irow][icol].check_for_ext():
                env.connections[irow][icol].event()
            continue
        continue
    
    return True
# end timestep

###############################
# Finalize the Simulation
###############################
def finalize():
    if os.path.exists(env.out_dir):
        purr.deldir(env.out_dir)
    os.mkdir(env.out_dir)
    vehicle.csv()
    return
# End finalize
