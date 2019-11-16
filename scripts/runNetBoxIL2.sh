#################################################
# Author: Chris Magnano
#
# 10/29/2019
#
# Example using included IL2 data to run pathway parameter advising and get data.
# Must be run within scripts directory.
#
#################################################
python pathwayParameterAdvising.py --genPathwayGraphlets=../data/IL2/graphletNames.txt --refPathwayGraphlets=../referencePathways/reactomeGraphlets.txt --outFile=il2_ranking.txt --minSize=15 --outputScore --verbose

