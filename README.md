# pathway-parameter-advising
[![Build Status](https://travis-ci.com/gitter-lab/pathway-parameter-advising.svg?branch=master)](https://travis-ci.com/gitter-lab/pathway-parameter-advising)
Parameter advising for biological pathway creation algorithms

Version 0.10. 

## Dependencies

Pathway parameter advising was written and tested using Python 3.6 and requires the packages `networkx` and `numpy`. 

## Usage

The pathway parameter advisor creates a ranking of pathways based on their
topological distance to a set of reference pathways. 

Arguments:
>  -h, --help            show this help message and exit
>  --genPathwayGraphlets File where each line is a graphlets file of a
>                        generated pathway. Required.
>  --refPathwayGraphlets File where each line is a graphlets file of a
>                        reference pathway. Required.
>  --outFile OUTFILE     File to store output in. Optional, default = "parameterRanking.txt".
>  --minSize MINSIZE     Minimum size a reference pathway must be to be
>                        rankings. Optional, default=15.
>  --outputMax           If set, will return only the top pathway instead of a
>                        full ranking. Oprional, default = False.
>  --outputScore         If set, will return scores in addition to pathway
>                        rankings. Optional, default = False.
>  --nameMap NAMEMAP     Either a file mapping generated pathway fileNames to
>                        parameter values, "stripped" to exclude the directory
>                        and extension from the filename, or "fileName" to use
>                        raw file names. Optional, default = stripped.
>  --verbose             If set, will print intermediate status updates. Optional, default = False.

## Graphlet Creation

Graphlet decomposition files are created with  the [Parallel Graphlet Decomposition library](http://nesreenahmed.com/graphlets/). Files are the piped output from the pgd script: `./pgd inputGraphFile >> graphletOutputFile.gOut`.