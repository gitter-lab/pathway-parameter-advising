# Data

This directory holds pathway and graphlet output files as examples for pathway parameter advising.

`fluHF_Inputs` contains the proteins and protein scores used as input for creating Influenza host factor networks in PCSF.
The data in `mapped_metaHF_prizes.txt` are from [Tripathi et al. 2015](https://doi.org/10.1016/j.chom.2015.11.002).
The identifiers in the Name column are UniProt entry names, except when the protein could not be mapped to UniProt.
In those cases, the original gene symbol is listed in the Name column.
The human background network for the Influenza analysis was a combination of PhosphositePlus and iRefIndex.
This network is available from the [TPS repository](https://github.com/koksal/tps/blob/v2.2/data/networks/phosphosite-irefindex13.0-uniprot.txt).
