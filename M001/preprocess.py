# preprocess.py
# Author: Quentin Goss
# Preprocessing steps are kept in this file
import env
import pantherine as purr
import networkx as nx
import os
import sys

# Intitialize the edge and node structures
def initialize_edges_and_nodes():
    edg_xml = purr.mrf(env.options.map_dir,r'*.edg.xml')
    env.edges = purr.readXMLtag(edg_xml,'edge')
    nod_xml = purr.mrf(env.options.map_dir,r'*.nod.xml')
    env.nodes = purr.readXMLtag(nod_xml,'node')
    return

# Loads the networkx graph
def initialize_nx():
    print("Loading networkx graph...",end='')
    map_nx = purr.mrf(env.options.map_dir,r'*.nx')
    env.nx = nx.read_edgelist(map_nx,data=(("weight",float),("id",str),),nodetype=str,comments='%',create_using=nx.MultiDiGraph())
    print("Complete!")
    return

