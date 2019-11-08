#################################################
# Author: Chris Magnano
#
# 11/08/2019
#
# This script attempts to install the pgd library from github
# in the lib directory. The lib directory is made if none exists.
#################################################

#Get repository directory and set up lib
homeDir=`git rev-parse --show-toplevel`;
mkdir ${homeDir}/lib;
mkdir ${homeDir}/lib/pgd;

#Get PGD from github and compile it
git clone https://github.com/nkahmed/PGD.git ${homeDir}/lib/pgd/;
make -C ${homeDir}/lib/pgd/;

#Test run without saving any output
./${homeDir}/lib/pgd/pgd -f ${homeDir}/data/IL2/p5e-2.sif;
