# options.py
# Author: Quentin Goss
# The options parser options are here
import optparse
import env
import sys
import os

def get_options():
    opt_parser = optparse.OptionParser()
    # GUI
    opt_parser.add_option("--nogui",action="store_true",default=False, help="run the commandline version of sumo")
    #
    opt_parser.add_option('--seed',type='int',dest='seed',default=8635839050,help='Random Seed')
    opt_parser.add_option('--map-dir',type='string',dest='map_dir',default=None,help='Directory of SUMO map files')
    #
    opt_parser.add_option('--veh.total',type='int',dest='veh_total',default=1000,help='Total amount of vehicles.')
    opt_parser.add_option('--veh.exists.max',type='int',dest='veh_exists_max',default=50,help='The amount of vehicles that exist in the simulation at any time.')
    #
    opt_parser.add_option('-o','--out.dir',type='string',dest='out_dir',default='out',help='Output directory.')
    # Start
    opt_parser.add_option('--start',type='string',dest='start',default=None,help='Starting node.')
    # poi
    opt_parser.add_option('--poi-file',type='string',dest='poi_file',default=None,help='POI File')
    #
    options, args = opt_parser.parse_args()

    # Validate Options
    if options.map_dir == None:
        print('Please specify a map directory with --map-dir')
        sys.exit(1)
    elif options.start == None:
        print("Please specify a starting node with --start")
        sys.exit(1)
    elif options.poi_file == None:
        print("Please specify a poi file with --poi-file.")
        sys.exit(1)
        
    # Set variables
    env.veh_total = options.veh_total
    env.veh_exists_max = options.veh_exists_max
    env.seed = options.seed
    env.start = options.start
    env.poi_file = options.poi_file
    env.out_dir = options.out_dir
    
    return options
