import os
import shutil
from pathlib import Path

import numpy as np
import pandas as pd 

from discovery_wm.utils import get_path_config, get_parser, get_subj_id, get_ses_task_run

def preprocess_events(df):
    df.fillna({'trial_type': 'na'}, inplace=True)
    df['onset'] = df['onset'] - 7 * 1.49
    neg_rt = df['response_time'] < 0
    df['junk'] = np.where(neg_rt, 1, 0)
    df['na_trials'] = np.where((df['trial_type']=='na'), 1, 0)
    df['response_time'] = np.where(neg_rt, np.nan, df['response_time'])
    return df

def preprocess_confounds(df):
    # Remove the first 7 TRs
    df = df.iloc[7:]
    return df.reset_index(drop=True)

def main():
    bids_dir, fmriprep_dir, _, tedana_denoised_dir, tedana_transformed_dir, glm_data_dir, _ = get_path_config()

    # Parse the command line arguments
    parser = get_parser()
    parser.add_argument("--session", type=str, required=False, help="Session to process (e.g., ses-01)")
    args = parser.parse_args()
    subj_id = get_subj_id(parser)
    session = args.session

    # Directories from which we will move data
    subj_bids_dir = Path(bids_dir / subj_id)
    subj_fmriprep_dir = Path(fmriprep_dir / subj_id)
    subj_tedana_dir = Path(tedana_transformed_dir / subj_id)
    subj_tedana_denoised_dir = Path(tedana_denoised_dir / subj_id)

    # Directories to which we will move data
    glm_dir = Path(glm_data_dir / subj_id)
    glm_dir.mkdir(parents=True, exist_ok=True)

    # Build session pattern for filtering
    session_pattern = session if session else "ses-*"
    
    # Copy over all masks and confounds files
    # t1w_masks = sorted(subj_fmriprep_dir.glob(f"{session_pattern}/func/*T1w*brain_mask.nii.gz"))
    # mni_masks = sorted(subj_fmriprep_dir.glob(f"{session_pattern}/func/*MNI*brain_mask.nii.gz"))
    # confounds = sorted(subj_fmriprep_dir.glob(f"{session_pattern}/func/*confounds*.tsv"))
    events = sorted(subj_bids_dir.glob(f"{session_pattern}/func/*events.tsv"))

    # Move all the above files to the glm_dir
    # Process masks
    # for file in t1w_masks + mni_masks:
    #     rel_path = os.path.relpath(file, start=subj_fmriprep_dir)
    #     dest_path = glm_dir / rel_path
    #     os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    #     shutil.copy2(file, dest_path)

    # Process confounds files
    # for file in confounds:
    #     df = pd.read_csv(file, sep='\t')
    #     df = preprocess_confounds(df)
    #     rel_path = os.path.relpath(file, start=subj_fmriprep_dir)
    #     dest_path = glm_dir / rel_path
    #     os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    #     df.to_csv(dest_path, sep='\t', index=False)

    # Process the events files
    for file in events:
        df = pd.read_csv(file, sep='\t')
        df = preprocess_events(df)
        # Write out preprocessed events file
        rel_path = os.path.relpath(file, start=subj_bids_dir)
        dest_path = glm_dir / rel_path
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        df.to_csv(dest_path, sep='\t', index=False)
        print(f"Processed events file: {file.name}")

    # Copy over all bold files
    # bold_files = sorted(subj_tedana_dir.glob(f"{session_pattern}/func/*desc-optcom_bold.nii.gz"))
    # for file in bold_files:
    #     rel_path = os.path.relpath(file, start=subj_tedana_dir)
    #     dest_path = glm_dir / rel_path
    #     os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    #     shutil.copy2(file, dest_path)

    # Copy over all tedana confounds 
    # tedana_mixing = sorted(subj_tedana_denoised_dir.glob(f"{session_pattern}/*/desc-ICA_mixing.tsv"))
    # tedana_status = sorted(subj_tedana_denoised_dir.glob(f"{session_pattern}/*/desc-ICA_status_table.tsv"))

    # for file in tedana_mixing + tedana_status:
    #     ses, task, run = get_ses_task_run(file, use_parent=True)
    #     rel_path = os.path.join(ses, "func")
    #     dest_path = glm_dir / rel_path
    #     os.makedirs(dest_path, exist_ok=True)
    #     new_filename = f"{subj_id}_{ses}_{task}"
    #     if run:
    #         new_filename += f"_{run}"
    #     desc_part = file.name.split("desc-")[1]
    #     new_filename += f"_desc-{desc_part}"
    #     print(f"Copying {file} to {dest_path / new_filename}")
    #     shutil.copy2(file, dest_path / new_filename)
    
    print(f"Events files processing complete for {subj_id}" + (f" session {session}" if session else " all sessions"))
    return

if __name__ == "__main__":
    main()
