#!/bin/bash
#
# Job name specified from launch script.
#SBATCH --time=00:30:00
#SBATCH -n 1
#SBATCH --array 1-41%10
#SBATCH --cpus-per-task=8
#SBATCH --mem-per-cpu=8G
#SBATCH -p russpold,hns,normal 
# Outputs ----------------------------------
#SBATCH -o ./log/%x-%A-%a.out
#SBATCH -e ./log/%x-%A-%a.err
#SBATCH --mail-user=kritiach@stanford.edu
#SBATCH --mail-type=END
# ------------------------------------------

: '
Name: lev1_model.sbatch

Description: This script runs first-level GLM models for a specific task.

Usage: sbatch ./batch/lev1_model.sbatch TASK_NAME

Notes: 
- TASK_NAME should be one of: cuedTS, directedForgetting, flanker, goNogo, nBack, stopSignal, shapeMatching, spatialTS
'

TASK_NAME=$1

if [ -z "$TASK_NAME" ]; then
    echo "Error: Task name not provided"
    echo "Usage: sbatch ./batch/lev1_model.sbatch TASK_NAME"
    exit 1
fi

# Prepare computing environment
# source ./batch/setup_env.sh
source ./batch/setup_env_validation.sh

# Script names 
first_level_script="src/discovery_wm/glm/first_level.py"

# Get the subject ID from the command line arguments
subject=$( sed "${SLURM_ARRAY_TASK_ID}q;d" ${ALL_SUBJECTS_FILE} )
echo "Subject: $subject"

# Check if the subject has the task data
task_dir="/oak/stanford/groups/russpold/data/network_grant/validation_BIDS/derivatives/glm_data/sub-${subject}/ses-*/func/*task-${TASK_NAME}_*"
if ! ls $task_dir 1> /dev/null 2>&1; then
    echo "No data found for subject ${subject} and task ${TASK_NAME}. Skipping."
    exit 0
else
    # Run the first-level model script
    echo "Running first-level model for task: $TASK_NAME"
    cmd="uv run $first_level_script --subj-id $subject --task-name $TASK_NAME"
    echo "Running command: $cmd"
    $cmd
fi

exit $? 
