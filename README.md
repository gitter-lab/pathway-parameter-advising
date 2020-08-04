# Pathway parameter advising
[![Build Status](https://travis-ci.com/gitter-lab/pathway-parameter-advising.svg?branch=master)](https://travis-ci.com/gitter-lab/pathway-parameter-advising)

Parameter advising for biological pathway creation algorithms.

## Citation

Pathway parameter advising is described in the following preprint:

[Automating parameter selection to avoid implausible biological pathway models](https://doi.org/10.1101/845834).
Chris S Magnano, Anthony Gitter.
*bioRxiv* 2019. doi:10.1101/845834

## Dependencies

Pathway parameter advising was written and tested using Python 3.6 and requires the packages `networkx`, `numpy`, and `requests`.

Graphlet decomposition is performed using the PGD library.
The PGD library can be installed from its [GitHub repository](https://github.com/nkahmed/pgd) and complied using `make`.
The script `setupPGD.sh` requires git, and has been provided to aid in installing the PGD library.
However, it is not guaranteed to work and has only been tested on Ubuntu 18.04.
In general, these scripts have only been tested in a Linux environment initially.

## Installation
Pathway parameter advising can be download from either PyPi or Github.

This package includes example data and scripts to manage reference pathways and aid in performing graphlet decomposition which are not a part of the binary Python package in PyPi. 
Therefore, it is reccomended to download the package source.

### PiPy download instructions 
In order to download all example scripts and data with pathway paramter advising, run `pip` using the following flags:
> `pip download --no-deps --no-binary :all: pathwayParameterAdvising`

This will download a `.tar` file into the current directory. 
Untar the resulting archive file: 
> `tar -xf pathwayParameterAdvising-*.tar.gz`

From inside the `pathway-parameter-advising-X.X` directory (where X.X is the current version of pathway paramtere advising), run
> `python setup.py install`

to install pathway parameter advising. 

### Github download instructions

Pathway parameter advising can also be downloaded from [its GitHub repository](https://github.com/gitter-lab/pathway-parameter-advising/). 

From inside the `pathway-parameter-advising` directory, run
> `python setup.py install`

to install pathway parameter advising. 

## Usage

### Using helper scripts 

The pathway parameter advisor creates a ranking of pathways based on their
topological distance to a set of reference pathways. 

The recommended way to use pathway parameter advising is through the script `bin/runPPA.sh`. 

`runPPA.sh` takes the following positional arguments:
>   dataDirectory: The directory where the networks are stored as sif or edgelist files in a subdirectory named 'pathways'. See Wnt and Prolactin for examples.
>
>   outFile:       The output filename for the final parameter ranking.
>
>   pgdDirectory:  (Optional) The directory where pgd is installed. Will default to '../lib/pgd'
>
>   delim:         (Optional) The limiter used for edges in the input network files. Assumed to be whitespace.


### Running Python package directly

Pathway paramter advising can also be run directly as a python script or libary, if different options are desired. 

`ppa.py` can be run as a command line script, or used as a Python package in which case the main entry point is the method `pathwayParameterAdivsing.rankParameters`.
`ppa.py` takes the following arguments:
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
>  --saveGraphlets       If set, will save graphlet distributions as pickled dictionaries.
>
>  --verbose             If set, will print intermediate status updates. Optional, default = False.

## Examples

`bin/runPPA.sh` runs pathway parameter advising on any set of sif or edgelist networks.
The following commands will run `runPPA.sh` with the included `Wnt` and `Prolactin` datasets from the `bin` directory, where `../lib/pgd` is installation location of the PGD library:

> `bash runPPA.sh ../data/Wnt wnt_ranking.txt ../lib/pgd`
>
> `bash runPPA.sh ../data/Prolactin prolactin_ranking.txt ../lib/pgd`

`bin/runNetBoxIL2.sh` runs pathway parameter advising for the precomputed graphlet files for NetBox IL2 pathways using Reactome reference pathways.

These scripts must be run from the `bin` directory, and file path arguments are relative to the `bin` directory.


## Graphlet Creation
Graphlet decomposition files are created with  the [Parallel Graphlet Decomposition library](http://nesreenahmed.com/graphlets/).
Files are the piped output from the pgd script: `./pgd -f inputGraphFile >> graphletOutputFile.gOut`.

## Other Scripts
`bin/setupPGD.sh` installs the PGD library into the `lib` directory, which is created if it does not exist.
PGD is cloned from its [github repository](https://github.com/nkahmed/pgd) and complied using `make`.
It can then be run from the base pathway-parameter-advising directory as `lib/pgd/pgd -f inputGraphFile`.

`bin/updateReactome.sh` downloads the latest version of all human reactome pathways from [Pathway Commons](https://www.pathwaycommons.org/) and performs graphlet decomposition on them. Requires the location of the PGD library as a command line argument. 
