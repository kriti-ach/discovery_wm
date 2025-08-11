#!/bin/bash
#SBATCH --job-name=make_zstat_heatmaps
#SBATCH --output=./log/make_zstat_heatmaps_%j.out
#SBATCH --error=./log/make_zstat_heatmaps_%j.err
#SBATCH --time=02:00:00
#SBATCH -p russpold,hns,normal
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G

# Run using uv and specify the venv directory directly
DATA_DIR=./output_lev1_mni_no_ted_comp
CURRENT_DIR=$PWD
OUTDIR=$PWD/quality_control/vif_figures
uv --directory $CURRENT_DIR run python $CURRENT_DIR/src/discovery_wm/quality_control/make_zstat_matrix_heatmaps.py \
    --data-root=$DATA_DIR \
    --output-dir=$OUTDIR \
    --output-file=contrast_grid_report.pdf
