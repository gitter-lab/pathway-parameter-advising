"""
Author: Chris Magnano
06/18/20

This is a script for getting and parsing all of the reactome pathways sifs into a format
ready for graphlet creation.

Usage: python getReactomePaths.py outputDirectory

Will make 2 subdirectories in outputDirectory: pathways and graphlets

Pathways will hold the raw reactome pathways with protein names and edge types.
Graphlets will hold the reactome pathways with integer edge names for graphlet decomposition.
"""
import sys
import requests
import time
import json
import os
import argparse
import networkx as nx
import pathwayParameterAdvising as ppa

"""
Method to call which downloads all pathways from source database (default is reactome)
in Pathway Commons and saves them in outDir.
"""
def updateReactome(outDir,source="reactome"):
    names = getAllPathwayNames(source)
    print("Found %d pathways from %s in Pathway Commons." %(len(names),source))
    allPaths, delList = getPathwayFiles(names,source)
    saveReactomeOutput(allPaths, outDir, delList)

"""
Saves pathways in allPaths in 2 formats, raw and as simple integer name
edge lists for use with PGD. Also attempts to create the directories
outDir, outDir/pathways, and outDir/graphlets
"""
def saveReactomeOutput(allPaths, outDir, delList):
    #Make subdirectories
    try:
        os.mkdir(outDir,0o755)
    except FileExistsError:
        pass
    try:
        os.mkdir(os.path.join(outDir, "pathways"),0o755)
    except FileExistsError:
        pass
    try:
        os.mkdir(os.path.join(outDir, "graphlets"),0o755)
    except FileExistsError:
        pass

    for path in allPaths:
        if path in delList:
            continue

        #Save pathways in format ready for graphlet analysis
        pathLines = allPaths[path].split("\n")
        if len(pathLines)<2:
            print("Skipping %s as it is 1 edge or less." %(path))
            continue

        eList = []
        for line in pathLines:
            lineList=line.strip().split()
            eList.append(" ".join([lineList[0],lineList[2]]))
        pathID = path.split("/")[-1]
        net = nx.parse_edgelist(eList)
        net = nx.convert_node_labels_to_integers(net, first_label=1)
        nx.write_edgelist(net, os.path.join(outDir,"graphlets",pathID+".sif"), delimiter="\t", data=False)

        #Save pathways with node names for use in any other analyses
        pathF = open(os.path.join(outDir,"pathways",pathID+".sif"),"w")
        pathF.write(allPaths[path])
        pathF.close()
    return

"""
Gets the identifiers for all pathways from Pathway Commons (default is reactome).
"""
def getAllPathwayNames(source="reactome"):
    #Get all reactome (or other source) pathways from pathwaycommons via web API
    allPathNames = []

    reqTxt = "http://www.pathwaycommons.org/pc2/search.json"
    pagesLeft = True
    currentPage = 0
    reqParams= {"type":"pathway","datasource":source,"q":"*"}

    while pagesLeft:
        reqParams["page"]=str(currentPage)
        try:
            #Pathway commons recommends using post, download can be slow so wait up to 10 minutes
            r = requests.post(reqTxt,params=reqParams,timeout=600.00)
        except requests.exceptions.RequestException as e:
            print("Got exception ",e)
            print("\n Skipping page "+str(currentPage)+" and continuing")
            time.sleep(0.4)
            continue
        currentPage += 1
        jsonOutput = json.loads(r.text)
        numHits = int(jsonOutput["numHits"])
        maxHitsPerPage = int(jsonOutput["maxHitsPerPage"])

        if (currentPage*maxHitsPerPage) > numHits:
            pagesLeft=False
        results = jsonOutput["searchHit"]
        if len(results)==0:
            pagesLeft=False
        for r in results:
            name = r["uri"]
            allPathNames.append(name)
    return allPathNames

def getPathwayFiles(reactomeNames,source="reactome"):
    allPaths=dict()

    #Initialize dictionary
    for name in reactomeNames:
        allPaths[name] = ""

    #Get pathways from pathwaycommons via web API
    reqTxt = "http://www.pathwaycommons.org/pc2/get"
    reqParams= {"uri":"","format":"SIF"}
    delList = [] #List of errors to skip

    i=0
    print("Getting files", end="", flush=True)
    for path in allPaths:
        i+=1
        if i%50==0:
            print(str(i), end="", flush=True)
        else:
            print(".", end="", flush=True)
        reqParams["uri"] = path

        #Pathway commons recommends using post, download can be slow so wait up to 10 minutes
        try:
            r = requests.post(reqTxt,params=reqParams,timeout=600.00)
        except requests.exceptions.RequestException as e:
            print("Got exception ",e)
            print("\n Removing pathway "+path+" from analysis and continuing")
            delList.append(path)
            time.sleep(0.2)
            continue

        allPaths[path] = r.text
        #Pathway commons warns not to do multiple per second.
        #Annoying, but needed to prevent a IP address ban.
        time.sleep(0.2)
    return allPaths, delList

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="As a script, this file downloads the latest version of all human Reactome pathways from Pathway Commons and prepares them for graphlet decomposition using the PGD library. Version %s, released under the MIT license."%(ppa.__version__))
    parser.add_argument("--outputDirectory", default="referencePathways", help="Directory where reactome pathways will be stored. Two subdirectories will be created, to hold raw pathways and pathways ready for graphlet decomposition.")
    parser.add_argument("--source", default="reactome", help="Source database in Pathway Commons to get pathways from. See https://www.pathwaycommons.org/pc2/datasources for a list of possible data sources.")
    args = parser.parse_args()
    outDir = args.outputDirectory
    source = args.source
    updateReactome(outDir,source)
