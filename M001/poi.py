# poi.py

import env
import pantherine as purr

def initialize():
    env.poi_ids = []
    with open(env.poi_file,'r') as f:
        for line in f:
            env.poi_ids.append(line.strip())
    
    env.poi_nodes = purr.flattenlist(purr.batchfilterdicts(env.nodes,'id',env.poi_ids))
    return
    
