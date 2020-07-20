#################################################
# Author: Chris Magnano
#
# 07/20/2020
#
# This script downloads the latest version of reactome and performs graphlet
# decompition.
#
# Usage: bash createNewReactomeGraphlets.sh reactomeDirectory pgdDirectory
#   reactomeDirectory: The directory where reactome pathways and graphlets
#                      will be stored. If not given will default to
#                      'referencePathways'.
#   pgdDirectory:      (Optional) The directory where pgd is installed. If
#                      none, pgd will be installed using the setupPGD.sh
#                      script.
#################################################

#Check for command line args
if [ -z "$1"]
    then
        reactDir="referencePathways";
    else
        reactDir=$1;
fi
pgdDir=$3;

homeDir=`git rev-parse --show-toplevel`;
mkdir ${reactDir};

#This will probably take ~10 minutes
#python getReactomePaths.py ${reactDir};

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
for pgdNet in `ls ${reactDir}/graphlets/* | grep -v '\.gOut$'`;
do
    echo $pgdNet;
    ${pgdDir}/pgd -f $pgdNet >> ${pgdNet%.*}.gOut;
done;

#Collect graphletNames into a text file
rm -f ${reactDir}/graphletNames.txt;
ls ${reactDir}/graphlets/*.gOut >> ${reactDir}/graphletNames.txt;
