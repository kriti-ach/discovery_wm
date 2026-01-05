import logging
import os
from discovery_wm.utils import get_path_config, get_all_subj_paths, get_subj_sessions
from discovery_wm.events.utils import cal_time_elapsed, get_neg_rt_correction, add_choice_acc, add_cols, response_time_and_junk
from pathlib import Path
import pandas as pd
import numpy as np
import re

def get_unique_tasks(func_files):
    """Get all unique tasks in the behavioral directory."""
    # Extract unique tasks using regex
    tasks = set()
    for file in func_files:
        parts = file.name.split("_")
        for p in parts:
            if p.startswith("task-"):
                task = p.split("-")[-1]
                tasks.add(task)
    
    return [t for t in tasks if t != "rest"]

def find_matching_behavioral_dir(subj, ses, behavioral_dir):
    """Find the matching behavioral directory for a given session and task."""
    subj = subj.replace("sub-", "")
    target_dir = os.path.join(behavioral_dir, subj, ses)
    if not os.path.exists(target_dir):
        print(f"Skipping: No matching behavioral directory found for {subj} {ses}")
        return None
    return target_dir

def long_name_to_short_name(long_name):
    """Convert a long name to a short name."""
    mapping = {
        'stop_signal': 'stopSignal', 
        'stop_signal_with_flanker': 'stopSignalWFlanker', 
        'spatial_switching': 'spatialTS', 
        'spatial_task_switching': 'spatialTS',
        'cued_task_switching': 'cuedTS',
        'n_back': 'nBack', 
        'directed_forgetting': 'directedForgetting', 
        'flanker': 'flanker', 
        'go_nogo': 'goNogo', 
        'shape_matching': 'shapeMatching', 
        'stop_signal_with_directed_forgetting': 'stopSignalWDirectedForgetting', 
        'directed_forgetting_with_flanker': 'directedForgettingWFlanker', 
        'cued_switching': 'cuedTS',
        's43_stop_w_flanker.csv': 'stopSignalWFlanker',
        's43.csv': 'stopSignalWFlanker',
        'directed_forgetting_with_cued_task_switching': 'directedForgettingWCuedTS',
        'cued_task_switching_with_directed_forgetting': 'directedForgettingWCuedTS',
        'spatial_task_switching_with_cued_task_switching': 'spatialTSWCuedTS',
        'flanker_with_shape_matching': 'flankerWShapeMatching',
        'cued_task_switching_with_flanker': 'cuedTSWFlanker',
        'spatial_task_switching_with_shape_matching': 'spatialTSWShapeMatching',
        'shape_matching_with_spatial_task_switching': 'spatialTSWShapeMatching',
        'n_back_with_shape_matching': 'nBackWShapeMatching',
        'n_back_with_spatial_task_switching': 'nBackWSpatialTS',
        'flanker_with_cued_task_switching': 'cuedTSWFlanker',
        'shape_matching_with_cued_task_switching': 'shapeMatchingWCuedTS'
    }
    return mapping[long_name]
        
def get_task_from_filename(filename):
    """Get the task from the filename."""
    long_name = filename.split("__fmri")[0]
    if "_single_task_network" in long_name:
        long_name = long_name.split("_single_task_network")[0]
    elif "task-" in long_name:
        parts = long_name.split('_')
        for p in parts:
            if p.startswith("task-"):
                long_name = p.replace("task-", "").replace("-", "_")
                break
    return long_name


def set_default_event_cols(df):
    df = df[df.time_elapsed > 0]
    df = df.rename(columns = {'time_elapsed': 'onset', 'choice_acc': 'acc', 'stim_duration': 'duration', 'rt': 'response_time'})
    df['onset'] = df['onset']/1000
    df['duration'] = df['duration']/1000
    df['response_time'] = df['response_time']/1000
    df['response_time'] = df['response_time'].replace(-0.001, np.nan)
    first_columns = ['onset', 'duration', 'response_time', 'trial_id', 'trial_type', 'key_press', 'correct_response']
    new_column_order = first_columns + [col for col in df.columns if col not in first_columns]
    df = df[new_column_order]
    return df


def rename_cells(df, exp_id):
    '''
    based on what exp_id is, rename certain cells in the dataframe
    '''
    #dictionary for cell value and what to change it to
    task_list = {
        'stop_signal_single_task_network__fmri': {'fixation': 'test_fixation', 'practice-no-stop-feedback': 'break'},
        'shape_matching_single_task_network__fmri': {'fixation': 'test_fixation', 'mask': 'test_mask', 'practice-no-stop-feedback': 'break'},
        'n_back_single_task_network__fmri':{'practice-no-stop-feedback': 'break', 'fixation': 'test_fixation'},
        'go_nogo_single_task_network__fmri': {'update_correct_response': 'test_fixation', 'feedback_block': 'break'},
        'spatial_task_switching_single_task_network__fmri': {'feedback_block': 'break', 'practice_cue': 'blank_screen'},
        'cued_task_switching_single_task_network__fmri': {'practice-stop-feedback': 'break'},
        'directed_forgetting_single_task_network__fmri': {'fixation': 'test_fixation', 'stim': 'test_stim', 
                                                        'cue': 'test_cue', 'test_feedback': 'break'},
        'flanker_single_task_network__fmri': {'practice-no-stop-feedback': 'break'},
        'directed_forgetting_with_flanker__fmri': {'test_start_fixation': 'test_fixation', 'test_feedback': 'break'},
        'stop_signal_with_directed_forgetting__fmri': {'ITI_fixation': 'test_fixation', 'stim': 'test_stim', 'cue': 'test_cue', 
                                                        'fixation': 'test_fixation', 'feedback_block': 'break'},
        'stop_signal_with_flanker__fmri': {'feedback_block':'break', 'fixation':'test_fixation'},
        'cued_task_switching_with_directed_forgetting__fmri': {'test_start_fixation': 'test_fixation', 'test_feedback': 'break'},
        'spatial_task_switching_with_cued_task_switching__fmri': {'test_cue_block': 'test_cue', 'fixation': 'test_fixation', 'feedback_block': 'break'},
        'flanker_with_shape_matching__fmri': {'feedback_block': 'break'},
        'flanker_with_cued_task_switching__fmri': {'practice-stop-feedback': 'break'},
        'flanker_with_cued_task_switching': {'practice-stop-feedback': 'break'},
        'n_back_with_shape_matching__fmri': {'feedback_block': 'break', 'fixation': 'test_fixation'},
        'shape_matching_with_spatial_task_switching__fmri': {'feedback_block': 'break', 'fixation': 'test_fixation'},
        'shape_matching_with_cued_task_switching__fmri': {'fixation': 'test_fixation', 'cue': 'test_cue', 'feedback_block': 'break'},
        'shape_matching_with_cued_task_switching': {'fixation': 'test_fixation', 'cue': 'test_cue', 'feedback_block': 'break'},
        'n_back_with_spatial_task_switching__fmri': {'feedback_block': 'break', 'fixation': 'test_fixation'}
    }
    #get dictionary of what to change
    change = task_list.get(exp_id)
    #rename cells in dataframe
    for key, value in change.items():
        df['trial_id'] = df['trial_id'].replace(key, value)
    
    if 'cued_task_switching_' in exp_id:
        #for trial_id == 'test_cue', change 'correct_response' to 'n/a'
        df.loc[df['trial_id'] == 'test_cue', 'correct_response'] = 'n/a'
    
    return df

def flagged_feedback(text_content: str) -> bool:
    """Check if the feedback is flagged.

    Args:
        text_content (str): Feedback text.

    Returns:
        bool: Whether the feedback is flagged.
    """

    keywords = ['accuracy', 'slowly', 'respond', 'response']

    return any(keyword in text_content.lower() for keyword in keywords)

def get_rows_with_feedback(df, original_df, filename):
    feedback_block_rows = original_df[original_df['trial_id'] == 'test_feedback']
    if len(feedback_block_rows) == 0:
        feedback_block_rows = original_df[original_df['trial_id'] == 'feedback_block']

    # If there are still no feedback block rows, get the rows where "blocks of trials" in in the stimulus
    # column value of the row

    if len(feedback_block_rows) == 0:
        # Add na=False parameter to handle NaN values in the stimulus column
        feedback_block_rows = original_df[original_df['stimulus'].str.contains('completed', na=False)]

    break_rows = df[df['trial_id'] == 'break']    
    
    # assert feedback_block_rows.index.tolist() == break_rows.index.tolist(), (
    #     original_df.to_csv(f'err_feedback_block_rows.csv', index=False),
    #     f'Unique trial ids in original df: {original_df["trial_id"].unique()}'
    #     f"feedback_block_rows and break_rows have different indices: {feedback_block_rows.index.tolist()} != {break_rows.index.tolist()}"
    # )
    
    indices_to_change = []
    for index, row in feedback_block_rows.iterrows():
        # Access the stimulus value from the row
        stimulus = row['stimulus']
        if flagged_feedback(stimulus):
            indices_to_change.append(index)
            # Write this to a text file
            with open('feedback_block_rows.txt', 'a') as f:
                f.write(f"{filename} {index} {stimulus}\n")

    return feedback_block_rows, indices_to_change


def create_events_df(filename, short_name):
    """Create an events dataframe from a given filename."""
    original_df = pd.read_csv(filename)
    exp_id = original_df["exp_id"][0]
    print(f"Processing {filename} for {exp_id}")
    df = original_df.copy()
    df = get_neg_rt_correction(df)
    df = cal_time_elapsed(df)
    df = add_choice_acc(df)
    df = add_cols(df, exp_id)
    df = response_time_and_junk(df, short_name)
    df = set_default_event_cols(df)
    df = rename_cells(df, exp_id)

    df.fillna('n/a', inplace=True)
    # Convert all object/string columns to string type first
    # This ensures consistent handling of NaN values
    # for col in df.select_dtypes(include=['object']).columns:
    #     df[col] = df[col].astype(str)
    #     df[col] = df[col].replace('nan', 'n/a')
    
    # Fixing "na" to "n/a" for spatialTS 
    if 'spatial_task_switching' in exp_id and 'n_back' not in exp_id:
        df.loc[(df['trial_id'] == 'test_trial') & (df['trial_type'] == 'na'), 'trial_type'] = 'tn/a_cn/a'
        df.loc[(df['trial_id'] == 'test_trial') & (df['trial_type'] == 'tn/a_cn/a'), 'task_switch'] = 'tn/a_cn/a'

    return df

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Creating events files")

    bids_dir, _, _, _, _, _, behavioral_dir = get_path_config()

    # Only process nBackWSpatialTS task
    target_task = 'nBackWSpatialTS'
    
    # Create output directory
    output_base_dir = Path('/scratch/users/kritiach/discovery_wm/updated_event_files') / target_task
    output_base_dir.mkdir(parents=True, exist_ok=True)

    all_subjects = get_all_subj_paths(bids_dir)
    print(f"All subjects: {all_subjects}")
    
    for subj in all_subjects:
        sessions = get_subj_sessions(subj)
        for ses in sessions:
            if ses.name == 'ses-11' or ses.name == 'ses-12' or ses.name == 'ses-13':
                print(subj.name, ses.name)
                func_dir = ses / "func"
                if not func_dir.exists():
                    raise ValueError(f"No func directory found for {subj} {ses}")
                
                func_files = list(func_dir.glob("*.nii.gz"))
                tasks = get_unique_tasks(func_files)

                # Skip if target task is not in this session
                if target_task not in tasks:
                    continue

                # behavioral directory from which to create events files
                target_dir = find_matching_behavioral_dir(subj.name, ses.name, behavioral_dir)
                if target_dir is None:
                    continue
                
                # Group all files for the same task
                csv_files = list(Path(target_dir).glob("*.csv"))
                task_to_files = {}

                for t in csv_files:
                    long_name = get_task_from_filename(t.name)
                    short_name = long_name_to_short_name(long_name)
                    if short_name != target_task:
                        continue
                    task_to_files.setdefault(short_name, []).append(t)

                for short_name, files in task_to_files.items():
                    # Sort files: no (n) first, then by (n)
                    def extract_num(f):
                        match = re.search(r"\((\d+)\)", f.name)
                        return int(match.group(1)) if match else 0
                    files_sorted = sorted(files, key=extract_num)
                    for run_idx, t in enumerate(files_sorted, 1):
                        outname = f"{subj.name}_{ses.name}_task-{short_name}_run-{run_idx}_events.tsv"
                        df = create_events_df(t, short_name)
                        outpath = output_base_dir / outname
                        print(f"Writing {outpath}")
                        df.to_csv(outpath, sep="\t", index=False)

    return
            

    
if __name__ == "__main__":
    main()