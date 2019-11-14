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
#   pgdDirectory:  (Optional) The directory where pgd is installed. If none, pgd will be installed
#                  using the setupPGD.sh script.
#   delim:         (Optional) The limiter used for edges in the input network files. Assumed to be
#                  whitespace.
#
#################################################

dataDir=$1;
outFile=$2;
pgdDir=$3;
delim=$4;

homeDir=`git rev-parse --show-toplevel`;

#Unzip reference pathways if needed
if [[ ! -f "${homeDir}/referencePathways/reactome/R-HSA-109688.gOut" || "`ls ${homeDir}/referencePathways/reactome/*.gOut | wc -l`" -lt 1416 ]];
then
    unzip ${homeDir}/referencePathways/reactome/reactomeGraphlets.zip -d ${homeDir}/referencePathways/reactome/
fi

#Convert networks for PGD
for net in `ls ${dataDir}/pathways/*`;
do
    #Convert the file if it doesn't already exist in the graphlets directory
    if [ ! -f "${dataDir}/graphlets/${net##*/}" ];
    then
        python ${homeDir}/scripts/makePGDNet.py $net --delim=${delim};
    fi;
done;

#Install PGD if needed
if [ -z "$3" ]; #If no pgd directory provided
then
    if [ ! -d "${homeDir}/lib/pgd/" ]; #If pgd isn't in the default directory, install it
    then
        bash ${homeDir}/scripts/setupPGD.sh;
    fi;
    pgdDir=${homeDir}/lib/pgd;
fi;

#Run PGD
for pgdNet in `ls ${dataDir}/graphlets/* | grep -v \'\.gOut$\'`;
do
    ${pgdDir}/pgd -f $pgdNet >> ${pgdNet%.*}.gOut;
done;

#Collect graphletNames into a text file
rm -f ${dataDir}/graphletNames.txt;
ls ${dataDir}/graphlets/*.gOut >> ${dataDir}/graphletNames.txt;

rm -f ${homeDir}/referencePathways/reactomeGraphlets.txt;
ls ${homeDir}/referencePathways/reactome/*.gOut >> ${homeDir}/referencePathways/reactomeGraphlets.txt;

#Run PPA
python ${homeDir}/scripts/pathwayParameterAdvising.py --genPathwayGraphlets=${dataDir}/graphletNames.txt --refPathwayGraphlets=${homeDir}/referencePathways/reactomeGraphlets.txt --outFile=${outFile} --minSize=15 --outputScore --verbose;

