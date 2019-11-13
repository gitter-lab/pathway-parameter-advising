# Pathway parameter advising
[![Build Status](https://travis-ci.com/gitter-lab/pathway-parameter-advising.svg?branch=master)](https://travis-ci.com/gitter-lab/pathway-parameter-advising)

Parameter advising for biological pathway creation algorithms.

## Dependencies

Pathway parameter advising was written and tested using Python 3.6 and requires the packages `networkx` and `numpy`. 

## Usage

The pathway parameter advisor creates a ranking of pathways based on their
topological distance to a set of reference pathways. 

Arguments:
>  -h, --help            show this help message and exit
>
>  --genPathwayGraphlets File where each line is a graphlets file of a generated pathway. Required.
>
>  --refPathwayGraphlets File where each line is a graphlets file of a reference pathway. Required.
>
>  --outFile OUTFILE     File to store output in. Optional, default = "parameterRanking.txt".
>
>  --minSize MINSIZE     Minimum size a reference pathway must be to be rankings. Optional, default=15.
>
>  --outputMax           If set, will return only the top pathway instead of a full ranking. Optional, default = False.
>
>  --outputScore         If set, will return scores in addition to pathway rankings. Optional, default = False.
>
>  --nameMap NAMEMAP     Either a file mapping generated pathway fileNames to parameter values, "stripped" to exclude the directory and extension from the filename, or "fileName" to use raw file names. Optional, default = stripped.
>
>  --verbose             If set, will print intermediate status updates. Optional, default = False.

## Example

`scripts/runPPA.sh` runs pathway parameter advising on any set of sif or edgelist networks.
It will attempt to install the pgd library and setup the reactome pathway graphlets automatically. 
The following commands will run `runPPA.sh` with the included `Wnt` and `Prolactin` datasets from the `scripts` directory:

> `bash runPPA.sh ../data/Wnt wnt_ranking.txt`
>
> `bash runPPA.sh ../data/Prolactin prolactin_ranking.txt`

`scripts/runNetBoxIL2.sh` runs pathway parameter advising for the precomputed graphlet files for NetBox IL2 pathways using Reactome reference pathways.
It must be run from the `scripts` directory.
Unzip the Reactome pathway graphlets file `reactomeGraphlets.zip` before running the example script.


## Graphlet Creation
Graphlet decomposition files are created with  the [Parallel Graphlet Decomposition library](http://nesreenahmed.com/graphlets/).
Files are the piped output from the pgd script: `./pgd -f inputGraphFile >> graphletOutputFile.gOut`.

`scripts/setupPGD.sh` installs the PGD library into the `lib` directory, which is created if none exists. PGD is cloned from its [github repository](https://github.com/nkahmed/pgd) and complied using `make`. It can then be run from the base pathway-parameter-advising directory as `lib/pgd/pgd -f inputGraphFile`.

