"""
Originally written by Anthony Gitter
Edited by Chris Magnano for batch use

This script attempts to connect sources to targets in a graph
using a minimum-cost flow algorithm. Minimum cost flow is solved using
Google's OR-Tools library: https://developers.google.com/optimization/flow/mincostflow
"""
import argparse
from ortools.graph import pywrapgraph

def parse_nodes(node_file):
    ''' Parse a list of sources or targets and return a set '''
    with open(node_file) as node_f:
        lines = node_f.readlines()
        nodes = set(map(str.strip, lines))
    return nodes


def construct_digraph(edges_file, cap):
    ''' Parse a list of weighted undirected edges.  Construct a weighted
    directed graph in which an undirected edge is represented with a pair of
    directed edges.  Use the specified weight as the edge weight and a default
    capacity of 1.
    '''
    G = pywrapgraph.SimpleMinCostFlow()
    idDict = dict() #Hold names to number ids
    curID = 0
    default_capacity = int(cap)

    with open(edges_file) as edges_f:
        for line in edges_f:
            tokens = line.strip().split()
            node1 = tokens[0]
            if not node1 in idDict:
                idDict[node1] = curID
                curID += 1
            node2 = tokens[1]
            if not node2 in idDict:
                idDict[node2] = curID
                curID += 1
            #Google's solver can only handle int weights, so round to the 100th
            w = int((1-(float(tokens[2])))*100)
            G.AddArcWithCapacityAndUnitCost(idDict[node1],idDict[node2], default_capacity, int(w))
            G.AddArcWithCapacityAndUnitCost(idDict[node2],idDict[node1], default_capacity, int(w))
    idDict["maxID"] = curID
    return G,idDict


def print_graph(graph):
    ''' Print the edges in a graph '''
    print('\n'.join(sorted(map(str, graph.edges(data=True)))))


def add_sources_targets(G, sources, targets, idDict, flow):
    ''' Similar to ResponseNet, add an artificial source node that is connected
    to the real source nodes with directed edges.  Unlike ResponseNet, these
    directed edges should have weight of 0 and Infinite capacity.  Also add an
    artificial target node that has directed edges from the real target nodes
    with the same weights and capacities as the source node edges.  The new
    nodes must be named "source" and "target".
    '''
    default_weight = 0
    default_capacity = flow*10
    curID = idDict["maxID"]
    idDict["source"] = curID
    curID += 1
    idDict["target"] = curID

    for source in sources:
        if source in idDict:
            G.AddArcWithCapacityAndUnitCost(idDict["source"],idDict[source], default_capacity, default_weight)

    for target in targets:
        if target in idDict:
            G.AddArcWithCapacityAndUnitCost(idDict[target],idDict["target"], default_capacity, default_weight)


def write_output_to_sif(G,out_file_name,idDict):
    ''' Convert a flow dictionary from networkx.min_cost_flow into a list
    of directed edges with the flow.  Edges are represented as tuples.
    '''

    out_file = open(out_file_name,"w")
    names = {v: k for k, v in idDict.iteritems()}
    numE = 0
    for i in range(G.NumArcs()):
        node1 = names[G.Head(i)]
        node2 = names[G.Tail(i)]
        flow = G.Flow(i)
        if flow <= 0:
            continue
        if node1 in ["source","target"]:
            continue
        if node2 in ["source","target"]:
            continue
        numE+=1
        out_file.write(node1+"\t"+node2+"\n")
    print("Final network had %d edges" % numE)
    out_file.close()

    return

def min_cost_flow(G, flow, output, idDict):
    ''' Use the min cost flow algorithm to distribute the specified amount
    of flow from sources to targets.  The artificial source should have
    demand = -flow and the traget should have demand = flow.  output is the
    filename of the output file.  The graph should have artificial nodes
    named "source" and "target".
    '''
    G.SetNodeSupply(idDict['source'],int(flow))
    G.SetNodeSupply(idDict['target'],int(-1*flow))

    print("Computing min cost flow")
    if G.Solve() == G.OPTIMAL:
        print("Solved!")
    else:
        print("There was an issue with the solver")
        return

    write_output_to_sif(G,output,idDict)

def main(args):
    ''' Parse a weighted edge list, source list, and target list.  Run
    min cost flow or k-shortest paths on the graph to find source-target
    paths.  Write the solutions to a file.
    '''
    flow = int(args.flow)

    sources = parse_nodes(args.sources_file)

    targets = parse_nodes(args.targets_file)

    G,idDict = construct_digraph(args.edges_file, args.capacity)

    add_sources_targets(G, sources, targets, idDict, flow)

    out_file = args.output+"_flow"+str(flow)+"_c"+str(args.capacity)+".sif"
    min_cost_flow(G, flow, out_file, idDict)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--edges_file',
                        help='Network file. File should be in SIF file format.',
                        type=str,
                        required=True)
    parser.add_argument('--sources_file',
                        help='File which denotes source nodes, with one node per line.',
                        type=str,
                        required=True)
    parser.add_argument('--targets_file',
                        help='File which denotes source nodes, with one node per line.',
                        type=str,
                        required=True)
    parser.add_argument('--flow',
                        help='The amount of flow pushed through the network.',
                        type=float)
    parser.add_argument('--output',
                        help='Prefix for all output files.',
                        type=str,
                        required=True)
    parser.add_argument('--capacity',
                        help='The amount of flow which can pass through a single edge.',
                        type=float,
                        required=False,
                        default=1.0)

    args = parser.parse_args()
main(args)
