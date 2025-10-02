# A database of Curie and Néel temperatures auto-generated with ChemDataExtractor and the Snowball algorithm 

This repository contains the codebase for the paper and [database](https://doi.org/10.6084/m9.figshare.29559686): "A database of Curie and Néel temperatures auto-generated with ChemDataExtractor and the Snowball algorithm" 

By C. R. Kelly & J. M. Cole

# Usage
The workflow is as follows:

1. The records are extracted with [record_extraction_polaris.py](/record_extraction_polaris.py) using the models in [CustomModels.py](/CustomModels.py)
2. The extracted records are scrubbed of records containing values with negative Kelvin using [negative_kelvin_data_cleaning.py](/negative_kelvin_data_cleaning.py)
3. The records are consolidated into a single .json and .csv database using [consolidate_json_db.py](/consolidate_json_db.py)

# Acknowledgements

J.M.C. is grateful for the BASF/Royal Academy of Engineering Research Chair in Data-Driven Molecular Engineering of Functional Materials, which is partly supported by the STFC via the ISIS Neutron and Muon Source. J.M.C. also acknowledges QinetiQ for project support via an EPSRC ICASE award (voucher 210153) for PhD funding (for C.R.K.). The authors thank Qingyang Dong from the Molecular Engineering group at the Cavendish Laboratory, University of Cambridge, for his assistance in updating Snowball v2 so that it could be used with the version of ChemDataExtractor presented herein. The authors are indebted to the Argonne Leadership Computing Facility, which is a DOE Office of Science Facility, for use of its research resources, under contract No. DE-AC02-06CH11357.

# Citation
```
@article{  
  title={A database of Curie and Néel temperatures auto-generated with ChemDataExtractor and the Snowball algorithm},  
  author={Kelly, Charles R and Cole, Jacqueline M},  
  journal={Scientific Data},  
  volume={},  
  number={},  
  pages={},  
  year={},  
  publisher={Nature Publishing Group}  
}
```
