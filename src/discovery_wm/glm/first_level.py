from pathlib import Path
from discovery_wm.glm.qa import qa_design_matrix, add_to_html_summary, get_all_contrast_vif

import numpy as np
import pandas as pd
from nilearn.glm.contrasts import compute_fixed_effects
from nilearn.glm.first_level import (
    FirstLevelModel,
    compute_regressor,
)
from nilearn.image import load_img

from discovery_wm.glm.config import contrasts_config, regressor_config
from discovery_wm.glm.dual_task_config import dual_tasks_config, dual_tasks_regressor_config
from discovery_wm.glm.quality_control import get_all_contrast_vif
from discovery_wm.utils import get_path_config, get_parser, get_subj_id
import re

def get_mean_rt_query(task_name: str):
    if 'stopSignal' in task_name:
        return (
            "(trial_id == 'test_trial' and ("
            "((trial_type == 'go') | (trial_type == 'go_pos') | (trial_type == 'go_neg') | (trial_type == 'go_con') | (trial_type == 'go_congruent') | (trial_type == 'go_incongruent')) & "  # Use | for OR
            "(response_time >= 0.2) & (key_press == correct_response) | "  # Use & for AND
            "((trial_type == 'stop_failure') | (trial_type == 'stop_failure_pos') | (trial_type == 'stop_failure_neg') | (trial_type == 'stop_failure_con') | (trial_type == 'stop_failure_congruent') | (trial_type == 'stop_failure_incongruent')) & "
            "(response_time >= 0.2)))"
        )

    return (
        "(key_press == correct_response) & (trial_id == 'test_trial') & (response_time >= 0.2)"  # Use & for AND
    )

def calculate_mean_rt(files: dict, task_name: str):
    mean_rts = []
    query_string = get_mean_rt_query(task_name)
    
    for session in files:
        for run in files[session]:
            # Read the events file once and store in df
            df = pd.read_csv(files[session][run]["events"], sep='\t')
            subset = df.query(query_string)
            mean_rt = subset['response_time'].mean()
            if pd.notna(mean_rt):
                mean_rts.append(mean_rt)
        
    return np.mean(mean_rts) if mean_rts else np.nan

def get_nscans(datafile: Path):
    """
    Get the number of timepoints from a 4D image file.
    
    Args:
        datafile (Path): Path to the image file
        
    Returns:
        int: Number of timepoints
        
    Raises:
        ValueError: If the file cannot be read or doesn't have 4 dimensions
    """
    try:
        img = load_img(datafile)
        if len(img.shape) != 4:
            raise ValueError(f"Image {datafile} does not have 4 dimensions (found {len(img.shape)})")
        return img.shape[3]
    except Exception as e:
        raise ValueError(f"Failed to read image file {datafile}: {str(e)}") from e

def get_files(subj_dir: Path, task_name: str):
    """
    Parse the GLM directory and return a dictionary of files, nested by session and run.
    
    Files identified:
    - "events": events.tsv file
    - "confounds": desc-confounds_timeseries.tsv file
    - "ica_mixing": ICA_mixing.tsv file
    - "ica_status": ICA_status_table.tsv file
    - "t1w_data": T1w_desc-optcom_bold.nii.gz file
    - "t1w_brain_mask": T1w_desc-brain_mask.nii.gz file
    - "mni_data": MNI152NLin2009cAsym_res-2_desc-optcom_bold.nii.gz file (when tedana transform is done)
    - "mni_brain_mask": MNI152NLin2009cAsym_res-2_desc-brain_mask.nii.gz file (when tedana transform is done)
    """

    files = {}
    run_pattern = re.compile(r'run-\d+')

    for file in sorted(
        subj_dir.glob(f"ses-*/func/*task-{task_name}_*"),
        key=lambda x: (x.parts[-3], x.name) # Sort by session then filename
    ):
        session_name = file.parts[-3]
        
        run_match = run_pattern.search(file.name)
        if not run_match:
            print(f"Skipping file without run number: {file.name}")
            continue
        run_name = run_match.group(0)

        # Correctly initialize nested dictionaries
        if session_name not in files:
            files[session_name] = {}
        if run_name not in files[session_name]:
            files[session_name][run_name] = {}

        file_name = file.name
        if "events.tsv" in file_name:
            files[session_name][run_name]["events"] = file
        elif "desc-confounds_timeseries.tsv" in file_name:
            files[session_name][run_name]["confounds"] = file
        elif "ICA_mixing.tsv" in file_name:
            files[session_name][run_name]["ica_mixing"] = file
        elif "ICA_status_table.tsv" in file_name:
            files[session_name][run_name]["ica_status"] = file
        elif "T1w_desc-optcom_bold.nii.gz" in file_name:
            files[session_name][run_name]["t1w_data"] = file
        elif "T1w_desc-brain_mask.nii.gz" in file_name:
            files[session_name][run_name]["t1w_brain_mask"] = file
        elif "MNI152NLin2009cAsym_res-2_desc-optcom_bold.nii.gz" in file_name:
            files[session_name][run_name]["mni_data"] = file
        elif "MNI152NLin2009cAsym_res-2_desc-brain_mask.nii.gz" in file_name:
            files[session_name][run_name]["mni_brain_mask"] = file

    # Define required files (everything except ICA files)
    required_keys = ["events", "confounds", "t1w_data", "t1w_brain_mask", 
                     "mni_data", "mni_brain_mask"]
    
    # Collect only sessions and runs with all required files
    valid_files = {}
    for session_name, runs in files.items():
        valid_runs = {}
        for run_name, run_files in runs.items():
            missing = [key for key in required_keys if key not in run_files]
            if missing:
                print(f"Skipping {session_name}/{run_name}: missing required files: {', '.join(missing)}")
                continue
            valid_runs[run_name] = run_files
        
        if valid_runs:
            valid_files[session_name] = valid_runs

    return valid_files


def get_fmriprep_confounds(confounds_file: Path, task_name: str, is_discovery_sample: bool):
    confounds_df = pd.read_csv(confounds_file, sep="\t", na_values=["n/a"]).fillna(0)
 
    if is_discovery_sample and task_name == 'nBack':
        # NOTE: Discovery sample nBack had an issue with blocked design
        # so we are using the following regex to select the confounds
        # which includes more cosine terms
        confounds = confounds_df.filter(
            regex=(
                'cosine0[0-4]|trans_x$|trans_x_derivative1$|trans_x_power2$|'
                'trans_x_derivative1_power2$|trans_y$|trans_y_derivative1$|'
                'trans_y_power2$|trans_y_derivative1_power2$|trans_z$|'
                'trans_z_derivative1$|trans_z_power2$|trans_z_derivative1_power2$|'
                'rot_x$|rot_x_derivative1$|rot_x_power2$|rot_x_derivative1_power2$|'
                'rot_y$|rot_y_derivative1$|rot_y_power2$|rot_y_derivative1_power2$|'
                'rot_z$|rot_z_derivative1$|rot_z_power2$|rot_z_derivative1_power2$'
            )
        )
    else:
        confounds = confounds_df.filter(
            regex=(
                'cosine|trans_x$|trans_x_derivative1$|trans_x_power2$|'
                'trans_x_derivative1_power2$|trans_y$|trans_y_derivative1$|'
                'trans_y_power2$|trans_y_derivative1_power2$|trans_z$|'
                'trans_z_derivative1$|trans_z_power2$|trans_z_derivative1_power2$|'
                'rot_x$|rot_x_derivative1$|rot_x_power2$|rot_x_derivative1_power2$|'
                'rot_y$|rot_y_derivative1$|rot_y_power2$|rot_y_derivative1_power2$|'
                'rot_z$|rot_z_derivative1$|rot_z_power2$|rot_z_derivative1_power2$'
            )
        )
                
    return confounds.reset_index(drop=True)


def get_tedana_confounds(files, session, confounds_df=None):
    """
    Get the tedana rejected components to use as confounds.
    
    Args:
        files (dict): Dictionary of session files from get_files function
        session (str): Session name
        confounds_df (pd.DataFrame, optional): Existing confounds dataframe to append to
        
    Returns:
        pd.DataFrame: Confounds dataframe with tedana rejected components added
    """
    # Initialize confounds_df if None
    if confounds_df is None:
        confounds_df = pd.DataFrame()
    
    # Get the ICA mixing and status files
    # mixing_file = files[session]["ica_mixing"]
    # status_file = files[session]["ica_status"]
    
    # Read the mixing matrix
    mixing_df = pd.read_csv(mixing_file, sep='\t')
    
    # Read the component classification table
    status_df = pd.read_csv(status_file, sep='\t')
    
    # Find all node columns
    node_columns = [col for col in status_df.columns if col.startswith('Node ')]
    
    if not node_columns:
        raise ValueError("No Node columns found in ICA status table. Cannot determine rejected components.")
    
    # Get the last node column (assuming it has the final classification)
    # Sort numerically to handle "Node 10" coming after "Node 2" etc.
    node_columns = sorted(node_columns, key=lambda x: int(x.split(' ')[1]))
    final_node = node_columns[-1]
    
    print(f"Using {final_node} as the final classification node: {status_df.columns}")
    
    # Filter to get only the rejected components
    rejected_components = status_df[status_df[final_node] == 'rejected']['Component']
    
    # Create a dataframe with only the rejected components
    if not rejected_components.empty:
        rejected_df = mixing_df[rejected_components].reset_index(drop=True)
        
        # Rename columns to avoid conflicts
        rejected_df = rejected_df.add_prefix('tedana_rejected__')
        
        # Combine with existing confounds
        combined_confounds = pd.concat([confounds_df, rejected_df], axis=1)
        print(f"Added {len(rejected_components)} tedana rejected components as confounds")
        return combined_confounds
    else:
        print("No rejected components found")
        return confounds_df


def define_nuisance_trials(events_df: pd.DataFrame, task_name: str):
    # Add this line to handle missing values in trial_type
    events_df = events_df.copy()

    events_df['trial_type'] = events_df['trial_type'].fillna('n/a')
    
    if task_name in ["cuedTS", "nBack", "spatialTS", "flanker", "shapeMatching",
                     "spatialTSWCuedTS", "flankerWShapeMatching", "cuedTSWFlanker",
                     "spatialTSWShapeMatching", "nBackWShapeMatching", "nBackWSpatialTS",
                     "directedForgettingWCuedTS"]:
        omission = ((events_df.key_press == -1) & (events_df.trial_id == "test_trial"))
        commission = (
            (events_df.key_press != events_df.correct_response)
            & (events_df.key_press != -1)
            & (events_df.response_time >= 0.2)
            & (events_df.trial_id == "test_trial")
        )
        rt_too_fast = ((events_df.response_time < 0.2) & (events_df.trial_id == "test_trial"))
        bad_trials = omission | commission | rt_too_fast

    elif task_name in ["directedForgetting", "directedForgettingWFlanker"]: 
        omission = (events_df.key_press == -1) & (events_df.trial_id == "test_trial")
        commission = (
            (events_df.key_press != events_df.correct_response)
            & (events_df.key_press != -1)
            & (events_df.response_time >= 0.2)
            & (events_df.trial_id == "test_trial")
        )
        rt_too_fast = (events_df.response_time < 0.2) & (events_df.trial_id == "test_trial")
        bad_trials = omission | commission | rt_too_fast

    elif task_name in ["stopSignal", "goNogo"]:
        omission = (events_df.key_press == -1) & (events_df.trial_type == "go")
        commission = (
            (events_df.key_press != events_df.correct_response)
            & (events_df.key_press != -1)
            & (events_df.trial_type == "go")
            & (events_df.response_time >= 0.2)
        )
        rt_too_fast = (events_df.response_time < 0.2) & (events_df.trial_type == "go")
        bad_trials = omission | commission | rt_too_fast

    elif task_name in ["stopSignalWDirectedForgetting"]:
        omission = (events_df.key_press == -1) & (
            events_df.trial_type.isin(["go_pos", "go_neg", "go_con"])
        )
        commission = (
            (events_df.key_press != events_df.correct_response)
            & (events_df.key_press != -1)
            & (events_df.trial_type.isin(["go_pos", "go_neg", "go_con"]))
            & (events_df.response_time >= 0.2)
        )
        rt_too_fast = (events_df.response_time < 0.2) & (
            events_df.trial_type.isin(["go_pos", "go_neg", "go_con"])
        )
        bad_trials = omission | commission | rt_too_fast

    elif task_name in ["stopSignalWFlanker"]:
        omission = (events_df.key_press == -1) & (
            events_df.trial_type.isin(["go_incongruent", "go_congruent"])
        )
        commission = (
            (events_df.key_press != events_df.correct_response)
            & (events_df.key_press != -1)
            & (events_df.trial_type.isin(["go_incongruent", "go_congruent"]))
            & (events_df.response_time >= 0.2)
        )
        rt_too_fast = (events_df.response_time < 0.2) & (
            events_df.trial_type.isin(["go_incongruent", "go_congruent"])
        )
        bad_trials = omission | commission | rt_too_fast


    return 1 * bad_trials, 1 * omission, 1 * commission, 1 * rt_too_fast


def make_regressor_and_derivative(
    n_scans,
    tr,
    events_df,
    add_deriv=False,
    amplitude_column=None,
    duration_column=None,
    onset_column="onset",
    subset=None,
    demean_amp=False,
    cond_id="cond",
):
    # THROW ERRORS IF MISSING COLUMNS
    if amplitude_column is None or duration_column is None:
        raise ValueError("Must enter amplitude and duration columns")
    if amplitude_column not in events_df.columns:
        raise ValueError("must specify amplitude column that exists in events_df")
    if duration_column not in events_df.columns:
        raise ValueError("must specify duration column that exists in events_df")

    # Handle the case when subset is None by creating a temp column
    # of all True values
    if subset is None:
        events_df = events_df.copy()  
        events_df["temp_subset"] = True
        subset = "temp_subset == True"

    # Get the selected columns
    reg_3col = events_df.query(subset)[
        [onset_column, duration_column, amplitude_column]
    ]
    
    # Check if amplitude_column and duration_column are the same
    # If they are, create a temporary copy with a different name to avoid duplicate columns
    if amplitude_column == duration_column:
        reg_3col = reg_3col.copy()
        reg_3col = reg_3col.rename(columns={duration_column: "duration"})
        reg_3col = reg_3col.rename(columns={amplitude_column: "modulation"})
    else:
        # Original renaming logic
        reg_3col = reg_3col.rename(
            columns={duration_column: "duration", amplitude_column: "modulation"}
        )

    # TODO: Check if the above is necessary 
    # reg_3col = reg_3col.rename(
    #     columns={duration_column: "duration", amplitude_column: "modulation"}
    # )

    if demean_amp:
        reg_3col["modulation"] = reg_3col["modulation"] - reg_3col["modulation"].mean()

    if add_deriv:
        hrf_model = "spm + derivative"
    else:
        hrf_model = "spm"

 
    transposed_array = np.transpose(np.array(reg_3col))
    print(f"Shape of transposed array for {cond_id}: {transposed_array.shape}")

    # NOTE: deals with slice timing issue with outputs from fMRIPrep
    slice_timing_adjustment = np.arange(n_scans) * tr + tr / 2
    
    regressor_array, regressor_names = compute_regressor(
        transposed_array,
        hrf_model,
        slice_timing_adjustment,
        con_id=cond_id,
    )
    
    
    regressors = pd.DataFrame(regressor_array, columns=regressor_names)
    return regressors, reg_3col


def rename_columns(df, prefix):
    """
    Rename columns in a DataFrame by adding a prefix, preserving the onset/button_onset
    column name.

    Args:
        df (pd.DataFrame): Input DataFrame
        prefix (str): Prefix to add to column names

    Returns:
        pd.DataFrame: DataFrame with renamed columns
    """
    onset_column = 'onset' if 'onset' in df.columns else 'button_onset'
    renamed_columns = {col: f"{prefix}_{col}" for col in df.columns
                      if col != onset_column}
    return df.rename(columns=renamed_columns)

def create_simplified_events_df(dfs):
    """
    Merge multiple DataFrames on their onset column,
    adding prefixes to avoid column name conflicts.

    Args:
        dfs (list): List of tuples containing (DataFrame, prefix) pairs

    Returns:
        pd.DataFrame: Merged DataFrame containing all events
    """
    if not dfs:
        return pd.DataFrame()

    # Start with first DataFrame
    base_df = rename_columns(dfs[0][0], dfs[0][1])

    # Merge remaining DataFrames
    for df, prefix in dfs[1:]:
        df = rename_columns(df, prefix)
        base_df = base_df.merge(df, on='onset', how='outer')

    return base_df.sort_values('onset').reset_index(drop=True)

def create_regressors_from_config(config, events_df, nscans, tr, task_name=None):
    """
    Create regressors based on configuration dictionary

    Args:
        config (dict): Dictionary with regressor configurations
        events_df (pd.DataFrame): Events dataframe
        nscans (int): Number of scans
        tr (float): Repetition time
        task_name (str, optional): Task name to extract task-specific regressors

    Returns:
        tuple: (dict of regressors, list of (3col_df, name) tuples)
    """
    regressors = {}
    regressor_3cols = []

    if not task_name:
        raise ValueError("Task name is required")

    if task_name not in config:
        raise ValueError(f"Task name {task_name} not found in config")

    # Only process task-specific regressors if task_name exists in config
    for name, params in config[task_name].items():
        reg, reg_3col = make_regressor_and_derivative(
            n_scans=nscans,
            tr=tr,
            events_df=events_df,
            add_deriv=params.get('add_deriv', False),
            amplitude_column=params['amplitude_column'],
            duration_column=params['duration_column'],
            subset=params['subset'],
            demean_amp=params.get('demean_amp', False),
            cond_id=name,
        )
        regressors[name] = reg
        regressor_3cols.append((reg_3col, name))

    return regressors, regressor_3cols

def prepare_results_dir(subject_id: str, task_name: str, results_dir: Path = Path("./output_lev1_mni/")):
    subdirs = [
        "quality_control",
        "indiv_contrasts",
        "fixed_effects",
        "simplified_events"
    ]
    paths = [results_dir] + [Path(results_dir, subject_id, task_name, d) for d in subdirs]
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)
    return tuple(paths)

def log_session_files(session, run, files_dict):
    """
    Log session files in a readable format with status indicators.
    
    Args:
        session (str): Session name/ID
        files_dict (dict): Dictionary of file paths for the session
    """
    print(f"\n--- Files for {session} --- {run} ---")
    
    # Define labels for each file type for better readability
    labels = {
        "events": "Events",
        "t1w_data": "T1w data",
        "confounds": "Confounds",
        "t1w_brain_mask": "T1w brain mask",
        "mni_data": "MNI data",
        "mni_brain_mask": "MNI brain mask", 
        # "ica_mixing": "ICA mixing",
        # "ica_status": "ICA status"
    }
    
    for key, label in labels.items():
        file_path = files_dict.get(key)
        
        if file_path is None:
            status = "❌ Missing"
            path_str = "N/A"
        elif not file_path.exists():
            status = "⚠ Not found"
            path_str = str(file_path)
        elif file_path.stat().st_size == 0:
            status = "⚠ Empty"
            path_str = str(file_path)
        else:
            status = "✓ Found"
            path_str = str(file_path)
        
        # Format path to be more readable - show only the end part if it's long
        if len(path_str) > 60:
            path_str = f"...{path_str[-57:]}"
        
        print(f"{status} | {label:<15} | {path_str}")

def is_dual_task(task_name):
    return 'W' in task_name

def get_task_configs(task_name):
    """Return the appropriate regressor and contrast configs for the task."""
    if is_dual_task(task_name):
        return dual_tasks_regressor_config, dual_tasks_config
    else:
        return regressor_config, contrasts_config

def main():
    # _, _, _, _, _, glm_data_dir, _ = get_path_config()
    glm_data_dir = Path("/oak/stanford/groups/russpold/data/network_grant/validation_BIDS/derivatives/glm_data")

    # Parse the command line arguments
    parser = get_parser()
    task_name = parser.parse_args().task_name
    subj_id = get_subj_id(parser)
    subj_glm_dir = Path(glm_data_dir / subj_id)

    # Prepare results directory
    # - These directories will contain the
    # - output for each of the models and
    # - quality control files for each model
    # _, quality_control_dir, indiv_contrasts_dir, fixed_effects_dir, \
    #     simplified_events_dir = prepare_results_dir(subj_id, task_name, Path("/oak/stanford/groups/russpold/data/network_grant/discovery_BIDS_20250402/derivatives/output_lev1_mni"))
    _, quality_control_dir, indiv_contrasts_dir, fixed_effects_dir, \
        simplified_events_dir = prepare_results_dir(subj_id, task_name, Path("/oak/stanford/groups/russpold/data/network_grant/validation_BIDS/derivatives/output_lev1_mni"))
    
    # Clear all existing files in output directories to ensure a clean start
    output_dirs = [quality_control_dir, indiv_contrasts_dir, fixed_effects_dir, simplified_events_dir]
    for output_dir in output_dirs:
        if output_dir.exists():
            print(f"Clearing existing files in: {output_dir}")
            for file_path in output_dir.rglob("*"):
                if file_path.is_file():
                    file_path.unlink()
                    print(f"  Deleted: {file_path}")
    
    # Clear the HTML summary file at the beginning to remove any previous content
    html_file = indiv_contrasts_dir / f"contrasts_task_{task_name}_rtmodel_response_time_centered_duration_constant_model_summary.html"
    if html_file.exists():
        html_file.unlink()  # Delete the file if it exists
        print(f"Cleared previous HTML summary file: {html_file}")
    
    # Prepare data directory
    # - This directory contains the BIDS data
    # - The data is organized by subject and session
    # - The necessary files include the optcom bold files,
    # - the event files, the brain masks, and the confounds files
    print(f"Launching first-level models for {subj_id}")

    # Get files for the subject and task
    files = get_files(subj_glm_dir, task_name)
    if not files:
        print(f"No files found for {subj_id} and {task_name}")
        return

    # Calculate mean RT
    # - This is used to center the RT regressor
    mean_rt = calculate_mean_rt(files, task_name)
    tr = 1.49000
    model_break = True

    print("Mean RT: ", mean_rt)
    print("The following files will be used for the first-level model: ", files)

    # Get configs for this task
    reg_config, contrast_config = get_task_configs(task_name)
    contrasts = contrast_config[task_name]
    all_contrast_names = list(contrasts.keys())

    # Process each session
    for session in files:
        for run in files[session]:
            print(f'Processing session {session}, run {run}')

            # Get files for the current session
            events = files[session][run]["events"]
            t1w_data = files[session][run]["t1w_data"]
            confounds = files[session][run]["confounds"]
            t1w_brain_mask = files[session][run]["t1w_brain_mask"]
            mni_data = files[session][run]["mni_data"]
            mni_brain_mask = files[session][run]["mni_brain_mask"]
            # ica_mixing = files[session][run]["ica_mixing"]
            # ica_status = files[session][run]["ica_status"]
        
            # Log all files for this session
            # TODO: Check this logging in next run
            log_session_files(session, run, files[session][run])

            # Get the number of timepoints in the current session
            # - this is used to create the regressors
            # nscans = get_nscans(t1w_data)
            nscans = get_nscans(mni_data)

            # - These are the confounds that are created by TEDANA / FMRIPREP
            # - These map onto motion parameters
            # TODO: change flag if running validation sample. 
            confound_regressors = get_fmriprep_confounds(confounds, task_name, is_discovery_sample=True)

            # # Add tedana rejected components to confounds
            # confound_regressors = get_tedana_confounds(files, session, confound_regressors)

            # EVENTS
            # - These are the events corresponding to the task
            # - Here, we add the nuisance trials to the events dataframe
            events_df = pd.read_csv(events, sep="\t", dtype={'response_time': float})
            (
                events_df["junk_trials"],
                events_df["omission"],
                events_df["commission"],
                events_df["rt_fast"],
            ) = define_nuisance_trials(events_df, task_name)

            # TODO: Add to quality control
            # Remove unused variable or use it
            percent_junk = np.mean(events_df["junk_trials"])

            # Add column containing all 1s
            events_df["constant_1_column"] = 1

            # Add response_time_centered column for RT regressor
            events_df["response_time_centered"] = events_df.response_time - mean_rt

            # Add break period if needed
            if model_break:
                reg_config[task_name]["break_period"] = {
                    "amplitude_column": "constant_1_column",
                    "duration_column": "duration",
                    "subset": 'trial_id == "break_with_performance_feedback"',
                }
                print(f'model_break: {model_break}')
                print(f'reg_config[task_name]["break_period"]: {reg_config[task_name]["break_period"]}')

            # Create regressors from config
            regressors_dict, regressor_dfs = create_regressors_from_config(
                reg_config, events_df, nscans, tr, task_name
            )

            # Create design matrix
            design_matrix = pd.concat(
                [regressors_dict[name] for name in regressors_dict] + [confound_regressors],
                axis=1,
            )

            simplified_events_df = create_simplified_events_df(regressor_dfs)
            simplified_events_df.to_csv(
                f"{simplified_events_dir}/{subj_id}_{session}_{run}_task-{task_name}_"
                f"simplified_events.csv",
                index=False
            )

            design_matrix['constant'] = 1

            # Print design matrix column names for debugging
            print("Design matrix columns:", design_matrix.columns.tolist())

            exclusion, any_fail = qa_design_matrix(
                indiv_contrasts_dir,
                contrasts,
                design_matrix,
                subj_id,
                task_name,
                session,  
                percent_junk=percent_junk,
            )

            print(exclusion)
            print(any_fail)

            print(f'run: {run}')
            add_to_html_summary(
                subj_id,
                contrasts,
                design_matrix,
                indiv_contrasts_dir,
                regress_rt="response_time_centered",
                duration_choice="constant",
                task=task_name,
                any_fail=any_fail,
                exclusion=exclusion,
                session=session,
                run=run,
                percent_junk=percent_junk,
                # model_break=True,
                # add_deriv=False,
                # only_breaks_with_performance_feedback=True
            )

            # Fit GLM to the data
            fmri_glm = FirstLevelModel(
                tr,
                subject_label=subj_id,
                # mask_img=t1w_brain_mask,
                mask_img=mni_brain_mask,
                noise_model="ar1",
                standardize=False,
                drift_model=None,
                smoothing_fwhm=5,
                minimize_memory=True,
            )

            # out = fmri_glm.fit(t1w_data, design_matrices=design_matrix)
            out = fmri_glm.fit(mni_data, design_matrices=design_matrix)
            # Save the contrasts
            for contrast_name, contrast_formula in contrasts.items():
                con_est = out.compute_contrast(contrast_formula, output_type="all")
                
                # Get effect size, variance, and z-score
                effect_size = con_est["effect_size"]
                variance = con_est["effect_variance"]
                z_score = con_est["z_score"]

                # Save to file
                effect_size.to_filename(
                    f"{indiv_contrasts_dir}/{subj_id}_{session}_{run}_task-{task_name}_"
                    f"contrast-{contrast_name}_rtmodel-rt_centered_stat-effect-size.nii.gz"
                )
                variance.to_filename(
                    f"{indiv_contrasts_dir}/{subj_id}_{session}_{run}_task-{task_name}_"
                    f"contrast-{contrast_name}_rtmodel-rt_centered_stat-variance.nii.gz"
                )
                z_score.to_filename(
                    f"{indiv_contrasts_dir}/{subj_id}_{session}_{run}_task-{task_name}_"
                    f"contrast-{contrast_name}_rtmodel-rt_centered_stat-z_score.nii.gz"
                )

            # QUALITY CONTROL
            # - Save out VIFs for each contrast
            vif_contrasts = get_all_contrast_vif(design_matrix, contrasts)
            vif_contrasts.to_csv(
                f"{quality_control_dir}/{subj_id}_{session}_{run}_task-{task_name}_"
                f"rtmodel-rt_centered_stat-vif_contrasts.csv",
                index=False
            )

    print("Contrasts: ", all_contrast_names)

    # Filter out task-baseline contrast for fixed effects model
    # fixed_effects_contrast_names = [c for c in all_contrast_names if c != "task-baseline"]

    # Save out fixed effects contrasts
    for contrast_name in all_contrast_names:
        print(f"Processing fixed effects contrast for {contrast_name}")
        effects_files = [
            f for f in indiv_contrasts_dir.glob(
                f"{subj_id}_*_task-{task_name}_contrast-{contrast_name}_"
                f"rtmodel-rt_centered_stat-effect-size.nii.gz"
            )
        ]
        variances_files = [
            f for f in indiv_contrasts_dir.glob(
                f"{subj_id}_*_task-{task_name}_contrast-{contrast_name}_"
                f"rtmodel-rt_centered_stat-variance.nii.gz"
            )
        ]
        z_scores_files = [
            f for f in indiv_contrasts_dir.glob(
                f"{subj_id}_*_task-{task_name}_contrast-{contrast_name}_"
                f"rtmodel-rt_centered_stat-z_score.nii.gz"
            )
        ]

        if not (len(effects_files) == len(variances_files) == len(z_scores_files)):
            error_msg = (
                f"File count mismatch for contrast '{contrast_name}':\n"
                f"  - Effects files: {len(effects_files)}\n"
                f"  - Variance files: {len(variances_files)}\n"
                f"  - Z-score files: {len(z_scores_files)}\n"
            )
            print(error_msg)
            assert False, error_msg

        fixed_fx_contrast, fixed_fx_variance, fixed_fx_stat = compute_fixed_effects(
            effects_files, variances_files, precision_weighted=True
        )

        # Save out fixed effects contrast, variance and z-score
        fixed_effects_filename = Path(
            fixed_effects_dir,
            f"{subj_id}_task-{task_name}_contrast-{contrast_name}_"
            f"rtmodel-rt_centered_stat-fixed-effects.nii.gz"
        )
        fixed_fx_contrast.to_filename(fixed_effects_filename)

        fixed_variance_filename = Path(
            fixed_effects_dir,
            f"{subj_id}_task-{task_name}_contrast-{contrast_name}_"
            f"rtmodel-rt_centered_stat-fixed-effects-variance.nii.gz"
        )
        fixed_fx_variance.to_filename(fixed_variance_filename)

        fixed_stat_filename = Path(
            fixed_effects_dir,
            f"{subj_id}_task-{task_name}_contrast-{contrast_name}_"
            f"rtmodel-rt_centered_stat-fixed-effects-z_score.nii.gz"
        )
        fixed_fx_stat.to_filename(fixed_stat_filename)

        print(f"Fixed effects results for {contrast_name} saved to {fixed_effects_dir}")


    return


if __name__ == "__main__":
    main()
