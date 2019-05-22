#!/bin/bash

#SBATCH --job-name=projectivity_future_Att
#SBATCH --nodes=1
#SBATCH --output=/home/trr321/logs/projectivity_future_RNN_Att-R-%j.out
#SBATCH --error=/home/trr321/logs/projectivity_future_RNN_Att-R-%j.err
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=4
#SBATCH --mail-user=rao_tirupal@yahoo.com
#SBATCH --mem=24G
#SBATCH --mail-type=ALL
#SBATCH --time=12:00:00

module load libgpuarray/intel/python2.7/0.7.6
module load cudnn/8.0v5.1
DATAPATH=/scratch/trr321/RNN/
cd $DATAPATH
source /home/trr321/py2env/py2.7.12/bin/activate
THEANO_FLAGS='optimizer_excluding=scanOp_pushout_output,device=cuda' python -u train_RNN.py configs/config_RNN_onlyIntAtt_projectivity_future



