#!/bin/bash
#
#SBATCH -J launch-all-lev2
#SBATCH --time=1-00:00:00
#SBATCH -n 1
#SBATCH --cpus-per-task=4
#SBATCH --mem-per-cpu=4G
#SBATCH -p russpold,hns,normal 
# Outputs ----------------------------------
#SBATCH -o ./log/%x-%A-%a.out
#SBATCH -e ./log/%x-%A-%a.err
#SBATCH --mail-user=kritiach@stanford.edu
#SBATCH --mail-type=END
# ------------------------------------------


: '

Name: launch_all_lev2.sbatch

Description: This script launches second-level models for dual tasks (tasks with W in the name) on the discovery sample dataset. 

Usage: sbatch ./batch/launch_all_lev2.sbatch

Notes: 

'
# Run the second-level model script
echo "Running second-level models for dual tasks"
second_level_script="src/discovery_wm/glm/second_level.py"

# List of dual tasks
DUAL_TASKS=(
    "directedForgettingWCuedTS"
    # "directedForgettingWFlanker"
    # "stopSignalWDirectedForgetting"
    # "stopSignalWFlanker"
    # "spatialTSWCuedTS"
    # "flankerWShapeMatching"
    # "cuedTSWFlanker"
    # "spatialTSWShapeMatching"
    # "nBackWShapeMatching"
    # "nBackWSpatialTS"
    # "shapeMatchingWCuedTS"
)

# Run the script for each dual task
for task in "${DUAL_TASKS[@]}"; do
    echo "Processing task: $task"
    cmd="uv run $second_level_script --task-name $task"
    echo "Running command: $cmd"
    $cmd
done

# Zip the output directory after completion
echo "Zipping output directory"
cmd="zip -r output_lev2_mni.zip output_lev2_mni"
echo "Running command: $cmd"
$cmd

exit $?