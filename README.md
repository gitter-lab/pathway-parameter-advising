# Min-Cost Flow Code

The script `minCostFlow.py` attempts to connect sources to targets in a graph
using a minimum-cost flow algorithm.

More details of the algorithm can be found in
[Automating parameter selection to avoid implausible biological pathway models](https://doi.org/10.1101/845834).
Chris S Magnano, Anthony Gitter.
*bioRxiv* 2019. doi:10.1101/845834

## Dependencies

Google's [OR-Tools library](https://developers.google.com/optimization/flow/mincostflow) is required to run this script. 

## Usage
`minCostFlow.py [-h] --edges_file EDGES_FILE --sources_file SOURCES_FILE --targets_file TARGETS_FILE [--flow FLOW] --output OUTPUT [--capacity CAPACITY]`

>  -h, --help:      Show this help message and exit.
>
>  --edges_file:   Network file. File should be in SIF file format. 
>
>  --sources_file: File which denotes source nodes, with one node per line. 
>
>  --targets_file: File whiuch denotes target nodes, with one node per line. 
>
>  --flow           The amount of flow pushed through the network. 
>
>  --output         Prefix for all output files. 
>
>  --capacity       The amount of flow which can pass through a single edge. 
