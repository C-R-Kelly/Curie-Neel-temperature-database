# A database of Curie and Néel temperatures auto-generated with ChemDataExtractor and the Snowball algorithm 

This repository contains the codebase for the paper and [database](https://doi.org/10.6084/m9.figshare.29559686): "A database of Curie and Néel temperatures auto-generated with ChemDataExtractor and the Snowball algorithm" 

By C. R. Kelly & J. M. Cole

# Usage
The workflow is as follows:

1. The records are extracted with [record_extraction_polaris.py](/record_extraction_polaris.py) using the models in [CustomModels.py](/CustomModels.py)
2. The extracted records are scrubbed of records containing values with negative Kelvin using [negative_kelvin_data_cleaning.py](/negative_kelvin_data_cleaning.py)
3. The records are consolidated into a single .json and .csv database using [consolidate_json_db.py](/consolidate_json_db.py)

# Acknowledgements

J.M.C. conceived the overarching project. The study was designed by S.G.J. and J.M.C. S.G.J. created the workflow, designed the CNN architecture, performed data pre-processing, featurization, hyperparameter optimization, and analysed the data under the supervision of J.M.C. G.J. assisted with the design of the CNN architecture and contributed to the hyperparameter optimization. S.G.J. drafted the manuscript with the assistance from J.M.C. The final manuscript was read and approved by all authors.

J.M.C. is grateful for the BASF/Royal Academy of Engineering Research Chair in Data-Driven Molecular Engineering of Functional Materials, which is partly sponsored by the Science and Technology Facilities Council (STFC) via the ISIS Neutron and Muon Source; this Chair also supports a PhD studentship (for S.G.J.). STFC is also thanked for a PhD studentship that is sponsored by its Scientific Computing Department (for G.J.).

# Citation
@article{huang2020database,  
  title={A database of battery materials auto-generated using ChemDataExtractor},  
  author={Huang, Shu and Cole, Jacqueline M},  
  journal={Scientific Data},  
  volume={7},  
  number={1},  
  pages={1--13},  
  year={2020},  
  publisher={Nature Publishing Group}  
}
