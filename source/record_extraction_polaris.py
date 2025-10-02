import sys
sys.path.append(r'')
from e2e_workflow.extraction.extractor_cooley import CDEDatabaseExtractor
from CustomModels import CurieTemperature, NeelTemperature
import datetime
import wandb
import os
from chemdataextractor.relex.snowball import Snowball



document_dir = r''
output_dir = r''


wandb_api_key = ''
use_wandb = True
wandb_config = None
wandb_project = os.getenv('wandb_project')
wandb_run_name = os.getenv('wandb_run_name')
num_of_nodes = os.getenv('num_of_nodes')
num_of_ranks = os.getenv('num_of_ranks')
num_of_depth = os.getenv('num_of_depth')
num_of_threads = os.getenv('num_of_threads')
conda_env = os.getenv('ACTIVE_ENV')
use_gpu = os.getenv('USE_GPU')
use_mpi = True


sb1 = Snowball(model=CurieTemperature, tsim_l=0.5)
sb1.import_from_list(path=r'', confidence_limit=1.0)
sb1.tsim_l = 0.5
sb1.tc = 0.9
sb1.cluster_all()
CurieTemperature.parsers = [sb1]

sb2 = Snowball(model=NeelTemperature, tsim_l=0.5)
sb2.import_from_list(path=r'', confidence_limit=1.0)
sb2.tsim_l = 0.5
sb2.tc = 0.9
sb2.cluster_all()
NeelTemperature.parsers = [sb2]


if use_wandb:
    wandb.login(key=wandb_api_key)
    if use_wandb:
        wandb_config = {
            'data_root_dir': document_dir,
            'save_root_dir': output_dir,
            'use_mpi': use_mpi,
            'use_gpu': use_gpu,
            'model_name': os.getenv('model_name'),
            'num_of_nodes': num_of_nodes,
            'num_of_ranks': num_of_ranks,
            'num_of_depth': num_of_depth,
            'num_of_threads': num_of_threads,
            'conda_env': conda_env
            }


extractor = CDEDatabaseExtractor(save_root_dir=output_dir, models=[CurieTemperature, NeelTemperature], use_mpi=use_mpi, use_wandb=use_wandb, wandb_config=wandb_config, wandb_run_name=wandb_run_name, wandb_project=wandb_project)

all_start_time = datetime.datetime.now()

extractor.extract(document_dir)

print(f'Extraction time was: {datetime.datetime.now() - all_start_time}')

