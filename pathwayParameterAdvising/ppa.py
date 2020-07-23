import os
import argparse
import numpy as np
import sys
import pickle as pkl
from pathwayParameterAdvising.graphletUtils import *
import pathwayParameterAdvising as ppa

"""
Author: Chris Magnano
Created: 10/29/19
Last Updated: 07/20/2020

Description: This file takes in a set of generated pathway graphlet decompositions, and a set of reference pathway graphlet decompositions.
It then ranks the generated pathways by their similarity to the reference pathways.
"""


"""
Main method which uses pathway parameter advising to rank parameters.

See argument definitions in README or by running "python pathwayParameterAdvising.py --help".
"""
def rankParameters(genPathsF,refPathsF,outF,minSize,outMax,outScore,verbose,nameMap,saveGraphlets,percTopCompute=0.2):
    #Load Graphlets
    if verbose:
        print("Command line arguments parsed, loading graphlets...")
    refPathsG = loadGraphlets(refPathsF,minSize,saveGraphlets,verbose)
    genPathsG = loadGraphlets(genPathsF,0,saveGraphlets,verbose)

    #Check loaded graphlets
    if len(refPathsG)==0:
        print("Must include at least 1 reference pathway to perform ranking.")
        return

    if len(genPathsG)==0:
        print("Must include at least 1 generated pathway to perform ranking.")
        return

    if verbose:
        print("Loaded %d generated pathways." %(len(genPathsG)))
        print("Loaded %d reference pathways." %(len(refPathsG)))

    #Calculate Distances
    distances = dict()
    if verbose:
        print("Calculating graphlet distances",end='',flush=True)
    for run in genPathsG:
        distances[run] = calcGraphletDistance(genPathsG[run], refPathsG.values())
        distances[run] = np.mean(distances[run][:int(len(distances[run])*percTopCompute)])
        if verbose:
            print(".",end='',flush=True)
    if verbose:
        print()

    #Save Output
    distances = changeNames(distances,nameMap)
    saveRankingOutput(distances,outF,outMax,outScore,verbose)
    return

"""
Calculates pairwise graphlet distance
"""
def calcPairwiseGraphletDistance(testG, refP):
    dist = 0
    allG = dict()
    for g in refP:
        if g=="size":
            continue
        allG[g] = True
        if g not in testG:
            dist += np.abs(refP[g])
        else:
            dist += np.abs((refP[g]) - (testG[g]))
    for g in testG:
        if g=="size":
            continue
        if g not in allG:
            dist += np.abs(testG[g])
    return dist


"""
Calculates graphlet distance between a single network's graphlet distribution
and a set of reference graphlet distritbutions
"""
def calcGraphletDistance(testG, refGraphlets):
    dists=[]
    for refP in refGraphlets:
        dist = calcPairwiseGraphletDistance(testG,refP)
        dists.append(dist)
    dists = sorted(dists)
    return dists



if __name__ == "__main__":
    #Handle command line arguments
    parser = argparse.ArgumentParser(description="The pathway parameter advisor creates a ranking of pathways based on their topological distance to a set of reference pathways. Version %s, released under the MIT license."%(ppa.__version__))
    parser.add_argument("--genPathwayGraphlets", help="File where each line is a graphlets file of a generated pathway, or a pickled dictionary of precomputed reference graphlet distributions",required=True)
    parser.add_argument("--refPathwayGraphlets", help="File where each line is a graphlets file of a reference pathway, or a pickled dictionary of precomputed reference graphlet distributions.",required=True)
    parser.add_argument("--outFile", default="parameterRanking.txt", help="File to store output in.")
    parser.add_argument("--minSize", default=15, help="Minimum size a reference pathway must be to be included. Must be integer.")
    parser.add_argument("--outputMax", action="store_true",help="If set, will return only the top pathway instead of a full ranking.")
    parser.add_argument("--outputScore", action="store_true",help="If set, will return scores in addition to pathway rankings.")
    parser.add_argument("--nameMap", default="stripped",help="Either a file mapping generated pathway fileNames to parameter values, \"stripped\" to exclude the directory and extension from the filename, or \"fileName\" to use raw file names.")
    parser.add_argument("--saveGraphlets", action="store_true",help="If set, will save graphlet distributions as pickled dictionaries.")
    parser.add_argument("--verbose", action="store_true",help="If set, will print intermediate status updates.")

    args = parser.parse_args()
    genPathsF = args.genPathwayGraphlets
    refPathsF = args.refPathwayGraphlets
    outF = args.outFile
    minSize = int(args.minSize)
    outMax = args.outputMax
    outScore = args.outputScore
    verbose = args.verbose
    nameMap = args.nameMap
    saveGraphlets = args.saveGraphlets

    #Secondary argument checking due to some explicity empty strings passed in by scripts
    if len(outF)==0:
        outF="parameterRanking.txt"

    print("Running pathway parameter advising with generated pathways at %s and reference pathways at %s" %(genPathsF,refPathsF))
    if verbose:
        print("Other parameters: \n output file \t\t %s \n min ref pathway size \t %s \n output max only \t %s \n output scores \t\t %s \n name mapping \t\t %s" %(outF,str(minSize),str(outMax),str(outScore),nameMap))

    rankParameters(genPathsF,refPathsF,outF,minSize,outMax,outScore,verbose,nameMap,saveGraphlets)
