## Bin

This directory contains a number of scripts for running pathway parameter advising, updating reference pathways, and installing PGD.

Most of these scripts must be run inside the `bin` directory. 

## Files

`bin/runPPA.sh` runs pathway parameter advising on any set of sif or edgelist networks.
It will attempt to install the pgd library and setup the reactome pathway graphlets automatically. 
The following commands will run `runPPA.sh` with the included `Wnt` and `Prolactin` datasets from the `scripts` directory:

> `bash runPPA.sh ../data/Wnt wnt_ranking.txt`
>
> `bash runPPA.sh ../data/Prolactin prolactin_ranking.txt`

`bin/runNetBoxIL2.sh` runs pathway parameter advising for the precomputed graphlet files for NetBox IL2 pathways using Reactome reference pathways.


`bin/setupPGD.sh` installs the PGD library into the `lib` directory, which is created if none exists.
PGD is cloned from its [github repository](https://github.com/nkahmed/pgd) and complied using `make`.
It can then be run from the base pathway-parameter-advising directory as `lib/pgd/pgd -f inputGraphFile`.
Note this this script has been included to help install the PGD library, but is not guaranteed to run on all systems. 
It has been tested on Ubuntu 18.04. 

`bin/updateReactome.sh` downloads the latest version of all human reactome pathways from [Pathway Commons](https://www.pathwaycommons.org/) and performs graphlet decomposition on them. Requires the location of the PGD library as a command line argument. 
