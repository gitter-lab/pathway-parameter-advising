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
mkdir ../lib;
mkdir ../lib/pgd;

#Get PGD from github and compile it
#git clone https://github.com/nkahmed/PGD.git ${homeDir}/lib/pgd/;
#git --git-dir=${homeDir}/lib/pgd/.git checkout 05fef84db271554cc6ff2dbac9964c614e0c7981;
git clone https://github.com/rbassett3/PGD.git ../lib/pgd/;
git --git-dir=../lib/pgd/.git checkout cdccc5e92fc012de292364f8f9ded7e185dbe9cb;
make -C ../lib/pgd/;

#Test run without saving any output
python ../pathwayParameterAdvising/makePGDNet.py ../data/IL2/pathways/p5e-2.sif;
../lib/pgd/pgd -f ../data/IL2/graphlets/p5e-2.sif;
rm ../data/IL2/graphlets/p5e-2.sif;
