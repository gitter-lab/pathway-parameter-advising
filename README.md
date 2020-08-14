# Pathway parameter advising
[![Build Status](https://travis-ci.com/gitter-lab/pathway-parameter-advising.svg?branch=master)](https://travis-ci.com/gitter-lab/pathway-parameter-advising)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3985899.svg)](https://doi.org/10.5281/zenodo.3985899)

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
However, it is not guaranteed to work on all systems and has only been tested on Ubuntu 18.04 and macOS 10.13.
In general, these scripts have only been tested in a Linux environment initially.

### Compiling PGD for macOS
Many macOS systems use clang++ instead of g++ and set g++ as an alias for clang++.
PGD requires g++ instead of clang++.
Therefore, macOS users must install g++ and set it as the compiler before running the `setupPGD.sh` script.

There are multiple options for installing g++.
We recommend [Homebrew](https://brew.sh/).
With Homebrew:

1. Install gcc with the command `brew install gcc`
2. Define the CC and CXX environmental variables according to the location of brew install. For example:
- `export CC=/usr/local/Cellar/gcc/10.1.0/bin/gcc-10`
- `export CXX=/usr/local/Cellar/gcc/10.1.0/bin/g++-10`

## Installation
Pathway parameter advising can be download from either PyPI or GitHub.

This package includes example data and scripts to manage reference pathways and aid in performing graphlet decomposition which are not a part of the binary Python package in PyPI.
Therefore, it is recommended to download the package source.

### PyPI download instructions
In order to download all example scripts and data with pathway parameter advising, run `pip` using the following flags:
> `pip download --no-deps --no-binary :all: pathwayParameterAdvising`

This will download a `.tar` file into the current directory. 
Untar the resulting archive file: 
> `tar -xf pathwayParameterAdvising-*.tar.gz`

From inside the `pathway-parameter-advising-X.X` directory (where X.X is the current version of pathway parameter advising), run
> `python setup.py install`

to install pathway parameter advising. 

### GitHub download instructions

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
>  dataDirectory: The directory where the networks are stored as sif or edgelist files in a subdirectory named 'pathways'. See Wnt and Prolactin for examples.
>
>  outFile:       The output filename for the final parameter ranking.
>
>  pgdDirectory:  (Optional) The directory where pgd is installed. Will default to '../lib/pgd'
>
>  delim:         (Optional) The limiter used for edges in the input network files. Assumed to be whitespace.

The `runPPA.sh` output is sorted from lowest to highest score.
This is because the score is a distance from the reference pathways, so the parameter combination with the smallest score is best.
See the [IL2 output](tests/reference/il2_ranking.txt) as an example.

### Running Python package directly

Pathway parameter advising can also be run directly as a Python script or library, if different options are desired.

`pathwayParameterAdvising/ppa.py` can be run as a command line script, or used as a Python package in which case the main entry point is the method `pathwayParameterAdvising.rankParameters`.
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
It has no arguments. 

These scripts must be run from the `bin` directory, and file path arguments are relative to the `bin` directory.


## Graphlet creation
Graphlet decomposition files are created with the [Parallel Graphlet Decomposition library](http://nesreenahmed.com/graphlets/).
Files are the piped output from the pgd script: `./pgd -f inputGraphFile >> graphletOutputFile.gOut`.

## Other scripts
`bin/setupPGD.sh` installs the PGD library into the `lib` directory, which is created if it does not exist.
PGD is cloned from its [GitHub repository](https://github.com/nkahmed/pgd) and complied using `make`.
It can then be run from the base pathway parameter advising directory as `lib/pgd/pgd -f inputGraphFile`.
Note this script has been included to help install the PGD library, but is not guaranteed to run on all systems.
It has been tested on Ubuntu 18.04 and macOS 10.13.
`setupPGD.sh` does not take any arguments.

`bin/updateReactome.sh` downloads the latest version of all human Reactome pathways from [Pathway Commons](https://www.pathwaycommons.org/) and performs graphlet decomposition on them. 
It takes the following positional arguments:
>   pgdDirectory:      The directory where pgd is installed. Will default to '../lib/pgd'
>
>   reactomeDirectory: (Optional) The directory where Reactome pathways and graphlets will be stored. If not given will default to '../referencePathways'.

## Pathway reconstruction algorithms
The pathway reconstruction algorithms used in the pathway parameter advising manuscript are available from:
- PathLinker: [PathLinker](https://github.com/Murali-group/PathLinker)
- NetBox: originally used [`netbox.tar.gz`](http://cbio.mskcc.org/wp-content/uploads/2012/10/netbox.tar.gz), which has since been replaced by [NetBoxR](https://www.bioconductor.org/packages/release/bioc/html/netboxr.html)
- Prize-Collecting Steiner Forest: [OmicsIntegrator](https://github.com/fraenkel-lab/OmicsIntegrator/) and [msgsteiner](https://staff.polito.it/alfredo.braunstein/code/2010/08/19/msgsteiner.html)
- Minimum-Cost Flow: [OR-Tools](https://developers.google.com/optimization/install) and [wrapper script](https://github.com/gitter-lab/influenza-pb2)
