import networkx as nx
import sys
import argparse
import os
import pathwayParameterAdvising as ppa

"""
Author: Chris Magnano
11/06/19

Description: This short script converts networks into a numbered edgelist for use with PGD.
"""
def makePGDNet(networkFile,delim,outF):
    if outF == "":
        nameParts = os.path.split(networkFile)
        netName = nameParts[1]
        outDir = os.path.join(os.path.split(nameParts[0])[0],"graphlets")
        if not os.path.isdir(outDir):
            os.mkdir(outDir)
        outF = os.path.join(outDir,netName)

    #Load Network
    if delim == "":
        pathway = nx.read_edgelist(networkFile.strip())
    else:
        pathway = nx.read_edgelist(networkFile.strip(), delimiter=delim)
    pathway = pathway.to_undirected()
    if len(pathway) < 4:
        print(networkFile, "too short at ",len(pathway),". Network must contain at least 4 nodes.")
        return

    #Write Output
    nx.write_edgelist(nx.convert_node_labels_to_integers(pathway, first_label=1), outF, delimiter="\t", data=False)
    print("Converted "+networkFile+" to "+outF)
    return

if __name__ == "__main__":
    #Parse Arguments
    parser = argparse.ArgumentParser(description="This script converts a sif or edgelist network file into a format interpretable by the pgd library. The network will be converted to be undirected and have sequential integer node names. Version %s, released under the MIT license" %(ppa.__version__))
    parser.add_argument("networkFile", help="Network sif or edgelist network file to be converted to a format interpretable by pgd. Must be in format readable by networkx.read_edgelist and have at least 4 nodes.")
    parser.add_argument("--delim", help="Node delimiter in network file to be passed to the \"delimiter\" argument in networkx.read_edgelist. Default is none, which will use the default whitespace delimeter in networkx.read_edgelist.", default="")
    parser.add_argument("--outFile", help="File to store formatted network in. Default is to store the network as NETWORKFILE in a new directory named graphlets.", default="")
    args = parser.parse_args()
    networkFile = args.networkFile
    delim = args.delim
    outF = args.outFile
    makePGDNet(networkFile,delim,outF)


