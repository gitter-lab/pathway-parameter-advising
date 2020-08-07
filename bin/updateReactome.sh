#################################################
# Author: Chris Magnano
#
# 07/20/2020
#
# This script downloads the latest version of reactome and performs graphlet
# decomposition.
#
# Usage: bash updateReactome.sh reactomeDirectory pgdDirectory
#   pgdDirectory:      (Optional) The directory where pgd is installed. Will default to '../lib/pgd'
#   reactomeDirectory: (Optional) The directory where reactome pathways and graphlets
#                      will be stored. If not given will default to
#                      '../referencePathways'.
#################################################

#Command line args
if [ -z "$1" ]
    then
        pgdDir="../lib/pgd";
    else
        pgdDir=$1;
fi

if [ -z "$2" ]
    then
        reactDir="../referencePathways";
    else
        reactDir=$2;
fi

mkdir -p "${reactDir}";

#This will probably take ~10 minutes
python ../pathwayParameterAdvising/getReactomePaths.py --outputDirectory=${reactDir};

#Run PGD
for pgdNet in `ls ${reactDir}/graphlets/* | grep -v '\.gOut$'`;
do
    echo $pgdNet;
    ${pgdDir}/pgd -f $pgdNet >> ${pgdNet%.*}.gOut;
done;

#Collect graphletNames into a text file
rm -f ${reactDir}/reactomeGraphlets.txt;
ls ${reactDir}/graphlets/*.gOut >> ${reactDir}/reactomeGraphlets.txt;

#Create new pickled dictionary to save time and space later
python ../pathwayParameterAdvising/graphletUtils.py --graphletsFile=${reactDir}/reactomeGraphlets.txt --minSize=15;
