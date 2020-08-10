import os
import argparse
import numpy as np
import sys
import pickle as pkl
import pathwayParameterAdvising as ppa

"""
Author: Chris Magnano
Created: 07/21/2020

Description: This file contains utilities related to file input and output, and loading
of graphlet output files.

When run as a script this file will create a pickled dictionary of graphlet distributions
from a list of graphlet output files.
"""

"""
Changes distances dictionary to use desired names
"""
def changeNames(distances,nameMap):
    if nameMap == "fileName":
        return distances
    if nameMap == "stripped":
        newDistances = dict()
        for name in distances:
            nameList = os.path.split(name)
            sName = nameList[-1]
            sName = os.path.splitext(sName)[0]
            newDistances[sName] = distances[name]
        return newDistances
    else:
        #Assume file format is fileName sep name
        nameDict = dict()
        for line in open(nameMap):
            lineList = line.strip().split()
            #Not great practice but flexible
            if len(lineList)<2:
                lineList = line.strip().split(",")
            if len(lineList)<2:
                continue
            nameDict[lineList[0]] = lineList[1]
        newDistances = dict()
        for name in distances:
            if name not in nameDict:
                print("Error: %s not in provided name mapping file. Using file name instead")
                newDistances[name]=distances[name]
            newDistances[nameDict[name]] = distances[name]
        return newDistances


"""
Saves ranking output according to command line settings
"""
def saveRankingOutput(distances,outFN,outMax,outScore,verbose):
    if verbose:
        print("Saving scores to "+outFN)
    outF = open(outFN,"w")
    if outScore:
        outF.write("Run\tScore\n")
    else:
        outF.write("Run\n")
    for run in sorted(distances, key = lambda x:(distances[x], x)):
        if outScore:
            score = distances[run]
            outF.write("%s\t%0.4f\n" %(run, score))
        else:
            outF.write(run+"\n")
        if outMax:
            break
    outF.close()
    return

"""
Loads all graphlet freqs and stores as ready to go distributions
"""
def loadGraphlets(allGraphsF,minSize,saveGraphlets,verbose):
    allGDists = dict()

    #Check if allGraphsF is a pickled dictionary
    try:
        allGraphsPickle = open(allGraphsF, "rb")
        allGDists = pkl.load(allGraphsPickle)
        allGraphsPickle.close()
        if verbose:
            print("Successfully loaded graphlet distributions from pickle file %s." %(allGraphsF))
        return allGDists
    except pkl.UnpicklingError:
        allGraphsPickle.close()

    skipCount = 0
    for line in open(allGraphsF):
        graphlets = loadSingleGFD(line.strip(),minSize,verbose)
        if len(graphlets)>0:
            allGDists[line.strip()]=graphlets
        else:
            skipCount += 1

    if verbose and minSize>0:
        print("Skipped %d reference pathways for being too small." %(skipCount))

    if saveGraphlets:
        if verbose:
            print("Saving loaded graphlet distributions as pickled dictionaries.")
        graphPklF = os.path.splitext(allGraphsF)[0]+".pkl"
        graphPkl = open(graphPklF,"wb")
        pkl.dump(allGDists,graphPkl)
        graphPkl.close()

    return allGDists

"""
Loads a graphlet freq dist from output file
"""
def loadSingleGFD(name,minSize,verbose):
    inGFD = False
    allG = 0
    outDict = dict()

    for line in open(name):
        lineList = line.strip().split()
        #Let's also grab size
        if line.startswith("|V|"):
            outDict["size"] = float(lineList[-1])

            if outDict["size"]<minSize:
                if verbose:
                    print("Skipping "+name+" with size",outDict["size"])
                    pass
                return dict()

        if not inGFD:
            if lineList[0].startswith("*"):
                inGFD = True
                continue
        if inGFD:
            # A line of *** means we're done with graphlet counts
            if line.startswith("*"):
                break
            if len(lineList) < 3:
                continue
            mName = lineList[0]
            mFreq = lineList[2]
            freq = float(mFreq)
            if not np.isfinite(freq) or freq==0:
                freq = 1.0
            outDict[mName] = freq
            allG += freq

    #Normalize
    for mName in outDict:
        if mName=="size":
            continue
        outDict[mName] = outDict[mName]/allG
    return outDict


if __name__ == "__main__":
    #Handle command line arguments
    parser = argparse.ArgumentParser(description="The pathway parameter advisor creates a ranking of pathways based on their topological distance to a set of reference pathways. Version %s, released under the MIT license."%(ppa.__version__))
    parser.add_argument("--graphletsFile", help="File where each line is a graphlets file of a reference pathway, or a pickled dictionary of precomputed reference graphlet distributions.",required=True)
    parser.add_argument("--minSize", default=15, help="Minimum size a reference pathway must be to be included. Must be integer.")
    parser.add_argument("--verbose", action="store_true",help="If set, will print intermediate status updates.")

    args = parser.parse_args()
    refPathsF = args.graphletsFile
    minSize = int(args.minSize)
    verbose = args.verbose
    loadGraphlets(refPathsF, minSize, True, verbose)
