# A database of Curie and Néel temperatures auto-generated with ChemDataExtractor and the Snowball algorithm 


**Author:** ***C. R. Kelly***   
**Email:** ***CK598@cam.ac.uk*** 

This repository contains the codebase for the paper and [database](https://doi.org/10.6084/m9.figshare.29559686): "A database of Curie and Néel temperatures auto-generated with ChemDataExtractor and the Snowball algorithm" 

The workflow is as follows:

1. The records are extracted with [record_extraction_polaris.py](/record_extraction_polaris.py) using the models in [CustomModels.py](/CustomModels.py)
2. The extracted records are scrubbed of records containing values with negative Kelvin using [negative_kelvin_data_cleaning.py](/negative_kelvin_data_cleaning.py)
3. The records are consolidated into a single .json and .csv database using [consolidate_json_db.py](/consolidate_json_db.py)
