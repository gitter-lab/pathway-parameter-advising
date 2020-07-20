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
import networkx as nx

def main():
    outDir = sys.argv[1]
    names = getPathwayNames()
    print("Found %d pathways." %(len(names)))

    allPaths, delList =getPathwayFiles(names)
    allData={"allPaths":allPaths,"delList":delList}
    saveOutput(allPaths, outDir, delList)
    return

def saveOutput(allPaths, outDir, delList):
    #Make subdirectories
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
        net = nx.parse_edgelist(eList)
        net = nx.convert_node_labels_to_integers(net, first_label=1)
        nx.write_edgelist(net, os.path.join(outDir,"graphlets",path+".sif"), delimiter="\t", data=False)

        #Save pathways with node names for use in any other analyses
        pathF = open(os.path.join(outDir,"pathways",path+".sif"),"w")
        pathF.write(allPaths[path])
        pathF.close()
    return

def getPathwayNames(source="reactome"):
    #Get all reactome (or other source) pathways from pathwaycommons via web API
    allPathNames = []

    reqTxt = "http://www.pathwaycommons.org/pc2/search.json"
    pagesLeft = True
    currentPage = 0
    reqParams= {"type":"pathway","datasource":source,"q":"*"}

    while pagesLeft:
        reqParams["page"]=str(currentPage)
        try:
            #Pathway commons reccomends using post, download can be slow so wait up to 10 minutes
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
            name = r["uri"].split("/")[-1]
            allPathNames.append(name)
    return allPathNames

def getPathwayFiles(reactomeNames):
    allPaths=dict()

    #Initialize dictionary
    for name in reactomeNames:
        allPaths[name] = ""

    #Get pathways from pathwaycommons via web API
    reqTxt = "http://www.pathwaycommons.org/pc2/get"
    reqParams= {"uri":"http://identifiers.org/reactome/","format":"SIF"}
    idURI="http://identifiers.org/reactome/"
    delList = [] #List of errors to skip

    i=0
    print("Getting files", end="", flush=True)
    for path in allPaths:
        i+=1
        if i%50==0:
            print(str(i), end="", flush=True)
        else:
            print(".", end="", flush=True)
        reqParams["uri"] = idURI+path

        #Pathway commons reccomends using post, download can be slow so wait up to 10 minutes
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
main()
