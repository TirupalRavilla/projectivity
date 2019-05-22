#!/bin/bash

#SBATCH --job-name=projectivity_Future_RNN
#SBATCH --nodes=1
#SBATCH --output=/home/trr321/logs/projectivity_data_prep_future_RNN-%j.out
#SBATCH --error=/home/trr321/logs/projectivity_data_prep_future_RNN-%j.err
#SBATCH --cpus-per-task=4
#SBATCH --mail-user=rao_tirupal@yahoo.com
#SBATCH --mem=24G
#SBATCH --mail-type=ALL
#SBATCH --time=12:00:00

DATAPATH=/scratch/trr321/RNN/
cd $DATAPATH
source /home/trr321/py2env/py2.7.12/bin/activate
python -u createRNNdataStream_projectivity_blocks.py prep/config_new_data_future
