#################################################
# Author: Chris Magnano
#
# 11/8/19
#
# This script takes a directory of network files and calculates their ranking
# using pathway parameter advising and reactome pathways as a set of references.
#
# This script assumes it is being run from within the pathway-parameter-advising repository.
#
# Usage: bash runPPA.sh dataDirectory outputFile pgdDirectory fileDelimeter
#   dataDirectory: The directory where the networks are stored as sif or edgelist files
#                  in a subdirectory named 'pathways'. See Wnt and Prolactin for examples.
#   outFile:       The output filename for the final parameter ranking.
#   pgdDirectory:  (Optional) The directory where pgd is installed. Will default to '../lib/pgd'
#   delim:         (Optional) The delimiter used for edges in the input network files. Assumed to be
#                  whitespace.
#
#################################################

dataDir=$1;
outFile=$2;
if [ -z "$3" ]
    then
        pgdDir="../lib/pgd";
    else
        pgdDir=$3;
fi
delim=$4;

#Convert networks for PGD
for net in `ls ${dataDir}/pathways/*`;
do
    #Convert the file if it doesn't already exist in the graphlets directory
    if [ ! -f "${dataDir}/graphlets/${net##*/}" ];
    then
        python ../pathwayParameterAdvising/makePGDNet.py $net --delim=${delim};
    fi;
done;

#Run PGD
for pgdNet in `ls ${dataDir}/graphlets/* | grep -v '\.gOut$'`;
do
    echo $pgdNet;
    ${pgdDir}/pgd -f $pgdNet >> ${pgdNet%.*}.gOut;
done;

#Collect graphletNames into a text file
rm -f ${dataDir}/graphletNames.txt;
ls ${dataDir}/graphlets/*.gOut >> ${dataDir}/graphletNames.txt;

#Run PPA
python ../pathwayParameterAdvising/ppa.py --genPathwayGraphlets=${dataDir}/graphletNames.txt --refPathwayGraphlets=../referencePathways/reactomeGraphlets.pkl --outFile=${outFile} --minSize=15 --outputScore --verbose;

