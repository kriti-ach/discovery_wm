#!/bin/bash
#
#SBATCH -J launch-all-lev1
#SBATCH --time=00:05:00
#SBATCH -n 1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=1G
#SBATCH -p russpold,hns,normal 
# Outputs ----------------------------------
#SBATCH -o ./log/%x-%A-%a.out
#SBATCH -e ./log/%x-%A-%a.err
#SBATCH --mail-user=kritiach@stanford.edu
#SBATCH --mail-type=END
# ------------------------------------------


: '

Name: launch_all_lev1.sbatch

Description: This script launches all first-level models on a dataset. 

Usage: sbatch ./batch/launch_all_lev1.sbatch

Notes: 

'

# Define all task names
TASKS=(
    # "cuedTS"
    # "directedForgetting"
    # "flanker"
    # "goNogo"
    # "nBack"
    # "shapeMatching"
    # "spatialTS"
    # "stopSignal"
)

DUAL_TASKS=(
    "directedForgettingWCuedTS"
    "directedForgettingWFlanker"
    "stopSignalWDirectedForgetting"
    "stopSignalWFlanker"
    "spatialTSWCuedTS"
    "flankerWShapeMatching"
    "cuedTSWFlanker"
    "spatialTSWShapeMatching"
    "nBackWShapeMatching"
    "nBackWSpatialTS"
)

# Launch first-level models for each task
for task in "${DUAL_TASKS[@]}"; do
    echo "Launching first-level model for task: $task"
    sbatch --job-name="lev1-model-${task}-mni" ./batch/lev1_model.sbatch "$task"
done

echo "All first-level models launched"