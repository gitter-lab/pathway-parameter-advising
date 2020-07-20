import os
import argparse
import numpy as np
import sys
import pickle as pkl
__version__ = "0.1.0"

"""
Author: Chris Magnano
10/29/19

Description: This file takes in a set of generated pathway graphlet decompositions, and a set of reference pathway graphlet decompositions.
It then ranks the generated pathways by their similarity to the reference pathways.
"""


def main():
    #Handle command line arguments
    parser = argparse.ArgumentParser(description="The pathway parameter advisor creates a ranking of pathways based on their topological distance to a set of reference pathways. Version %s, released under the MIT license."%(__version__))
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
    percTopCompute = 0.2

    #Secondary argument checking due to some explicity empty strings passed in by scripts
    if len(outF)==0:
        outF="parameterRanking.txt"

    print("Running pathway parameter advising with generated pathways at %s and reference pathways at %s" %(genPathsF,refPathsF))
    if verbose:
        print("Other parameters: \n output file \t\t %s \n min ref pathway size \t %s \n output max only \t %s \n output scores \t\t %s \n name mapping \t\t %s" %(outF,str(minSize),str(outMax),str(outScore),nameMap))

    #Load Graphlets
    if verbose:
        print("Command line arguments parsed, loading graphlets...")
    refPathsG = loadGraphlets(refPathsF,minSize,verbose)
    genPathsG = loadGraphlets(genPathsF,0,verbose)
    if saveGraphlets:
        if verbose:
            print("Saving loaded graphlet distributions as pickled dictionaries.")
        refPathsPklF = os.path.splitext(refPathsF)[0]+".pkl"
        refPathsPkl = open(refPathsPklF,"wb")
        pkl.dump(refPathsG,refPathsPkl)
        refPathsPkl.close()
        if verbose:
            print("Sucessfully saved %s." %(refPathsPklF))
        genPathsPklF = os.path.splitext(genPathsF)[0]+".pkl"
        genPathsPkl = open(genPathsPklF,"wb")
        pkl.dump(genPathsG,genPathsPkl)
        genPathsPkl.close()
        if verbose:
            print("Sucessfully saved %s." %(genPathsPklF))


    if len(refPathsG)==0:
        print("Error: Must include at least 1 reference pathway.")
        sys.exit()

    if len(genPathsG)==0:
        print("Error: Must include at least 1 generated pathway.")
        sys.exit()

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
    saveOutput(distances,outF,outMax,outScore,verbose)
    return

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
def saveOutput(distances,outFN,outMax,outScore,verbose):
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
Calculates graphlet distance
"""
def calcGraphletDistance(testG, refGraphlets):
    dists=[]
    for refP in refGraphlets:
        dist = calcPairwiseGraphletDistance(testG,refP)
        dists.append(dist)
    dists = sorted(dists)
    return dists


"""
Loads all graphlet freqs and stores as ready to go distributions
"""
def loadGraphlets(allGraphsF,minSize,verbose):
    allGDists = dict()

    #Check if allGraphsF is a pickled dictionary
    try:
        allGraphsPickle = open(allGraphsF, "rb")
        allGDists = pkl.load(allGraphsPickle)
        allGraphsPickle.close()
        if verbose:
            print("Successfully loaded %d graphlet distributions from pickle file %s." %(len(allGDists), allGraphsF))
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
    main()
