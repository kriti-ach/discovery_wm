#!/bin/bash
#SBATCH --job-name=make_zstat_grids
#SBATCH --output=./log/make_zstat_grids_%j.out
#SBATCH --error=./log/make_zstat_grids_%j.err
#SBATCH --time=02:00:00
#SBATCH -p russpold,hns,normal
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G

# Run using uv and specify the venv directory directly
# uv --directory /home/users/jmumford/vif_exploration run python /home/users/jmumford/vif_exploration/make_brain_zstat_map_grids.py \
#     --data-root=/oak/stanford/groups/russpold/data/network_grant/discovery_BIDS_20250402/derivatives/output_lev1 \
#     --output-dir=/home/users/jmumford/zstat_slice_grids \
#     --output-file=zstat_slice_grid_report.pdf
DATA_DIR=./output_lev1_mni_no_ted_comp
CURRENT_DIR=$PWD
OUTDIR=$PWD/quality_control/zstat_slice_grids
uv --directory $CURRENT_DIR run python $CURRENT_DIR/src/discovery_wm/quality_control/make_brain_zstat_map_grids.py \
    --data-root=$DATA_DIR \
    --output-dir=$OUTDIR \
    --output-file=zstat_slice_grid_report_mni.pdf