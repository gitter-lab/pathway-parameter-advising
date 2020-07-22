#################################################
# Author: Chris Magnano
#
# 07/20/2020
#
# This script downloads the latest version of reactome and performs graphlet
# decompition.
#
# Usage: bash createNewReactomeGraphlets.sh reactomeDirectory pgdDirectory
#   pgdDirectory:      The directory where pgd is installed.
#   reactomeDirectory: (Optional) The directory where reactome pathways and graphlets
#                      will be stored. If not given will default to
#                      '../referencePathways'.
#################################################

#Command line args
pgdDir=$1;

if [ -z "$2" ]
    then
        reactDir="../referencePathways";
    else
        reactDir=$2;
fi

mkdir "${reactDir}";

#This will probably take ~10 minutes
python ../pathwayParameterAdvisin/getReactomePaths.py ${reactDir};

#Run PGD
for pgdNet in `ls ${reactDir}/graphlets/* | grep -v '\.gOut$'`;
do
    echo $pgdNet;
    ${pgdDir}/pgd -f $pgdNet >> ${pgdNet%.*}.gOut;
done;

#Collect graphletNames into a text file
rm -f ${reactDir}/graphletNames.txt;
ls ${reactDir}/graphlets/*.gOut >> ${reactDir}/graphletDists.txt;

#Create new pickled dictionary to save time and space later
python ../pathwayParameterAdvising/graphletUtils.py --graphletsFile=${reactDir}/graphletNames.txt --minSize=15;
