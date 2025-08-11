import re
from pathlib import Path
import pandas as pd
import argparse
from discovery_wm.quality_control.find_feedback_breaks import find_num_feedback_breaks, find_correct_num_feedback_breaks

def find_vif_csv_files(base_dirs):
    """Find all VIF CSV files in the quality_control directories from multiple base directories."""
    csv_files = []
    
    for base_dir in base_dirs:
        base_path = Path(base_dir)
        
        if not base_path.exists():
            print(f"Base directory does not exist: {base_dir}")
            continue
        
        # Search for VIF CSV files in quality_control directories
        pattern = "**/quality_control/*vif_contrasts.csv"
        dir_csv_files = list(base_path.glob(pattern))
        csv_files.extend(dir_csv_files)
        print(f"Found {len(dir_csv_files)} VIF CSV files in {base_dir}")
    
    print(f"Total VIF CSV files found: {len(csv_files)}")
    return csv_files

def parse_csv_filename(filename):
    """Parse subject, session, run, and task from CSV filename."""
    # Example: sub-s247_ses-01_run-1_task-flanker_rtmodel-rt_centered_stat-vif_contrasts.csv
    filename_str = filename.name
    
    # Extract subject
    subj_match = re.search(r'(sub-s\d+)', filename_str)
    if not subj_match:
        return None
    subject = subj_match.group(1)
    
    # Extract session
    ses_match = re.search(r'(ses-\d+)', filename_str)
    if not ses_match:
        return None
    session = ses_match.group(1)
    
    # Extract run
    run_match = re.search(r'(run-\d+)', filename_str)
    if not run_match:
        return None
    run = run_match.group(1)
    
    # Extract task
    task_match = re.search(r'task-([a-zA-Z0-9_]+)_', filename_str)
    if not task_match:
        return None
    task = task_match.group(1)
    
    return {
        "subject": subject,
        "session": session,
        "run": run,
        "task": task
    }

def extract_vif_from_csv(csv_file):
    """Extract VIF data from a single CSV file."""
    try:
        # Parse filename to get metadata
        metadata = parse_csv_filename(csv_file)
        if not metadata:
            return None
        
        # Read the CSV file
        df = pd.read_csv(csv_file)
        
        # Find the task-baseline contrast VIF
        # The task-baseline contrast is the second last row
        if len(df) < 2:
            print(f"CSV file has fewer than 2 rows: {csv_file}")
            return None
        
        # Get the second last row (task-baseline contrast)
        second_last_row = df.iloc[-2]
        vif_value = second_last_row['VIF']
        
        # Create result dictionary
        result = {
            "subject": metadata["subject"],
            "session": metadata["session"],
            "run": metadata["run"],
            "task": metadata["task"],
            "vif": vif_value
        }
        
        return result
        
    except Exception as e:
        print(f"Error processing file {csv_file}: {e}")
        return None

def get_feedback_breaks_from_events(events_dirs, subject, session, task, run):
    """Get feedback breaks from events files in BIDS directories."""
    try:
        for events_dir in events_dirs:
            events_path = Path(events_dir)
            if not events_path.exists():
                continue
            
            # Look for events file in the specific subject/session/func directory
            events_file_pattern = f"{subject}/{session}/func/*{subject}_{session}_task-{task}_{run}_events.tsv"
            events_files = list(events_path.glob(events_file_pattern))
            
            if events_files:
                events_file = events_files[0]  # Take the first match
                df = pd.read_csv(events_file, sep="\t")
                performance_feedback_breaks, regular_breaks = find_num_feedback_breaks(df)
                
                # Only calculate expected breaks for stopSignalWDirectedForgetting
                if task == "stopSignalWDirectedForgetting":
                    expected_breaks = find_correct_num_feedback_breaks(df)
                else:
                    expected_breaks = None
                
                return performance_feedback_breaks, regular_breaks, expected_breaks
        
        # If no events file found, return zeros
        return 0, 0, None
        
    except Exception as e:
        print(f"Error getting feedback breaks for {subject}_{session}_{task}_{run}: {e}")
        return 0, 0, None

def main():
    """Main function to find CSV files, parse them, and save to master CSV."""
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Extract VIF values from CSV files')
    parser.add_argument('--task-name', type=str, help='Task name to filter results (e.g., flanker, stopSignal)')
    args = parser.parse_args()
    
    # Base directories containing all subjects and tasks
    base_dirs = [
        "/oak/stanford/groups/russpold/data/network_grant/discovery_BIDS_20250402/derivatives/output_lev1_mni",
        "/oak/stanford/groups/russpold/data/network_grant/validation_BIDS/derivatives/output_lev1_mni"
    ]

    events_dirs = [
        "/oak/stanford/groups/russpold/data/network_grant/discovery_BIDS_20250402/",
        "/oak/stanford/groups/russpold/data/network_grant/validation_BIDS/"
    ]
    
    # Find all VIF CSV files
    csv_files = find_vif_csv_files(base_dirs)
    
    if not csv_files:
        print("No VIF CSV files found.")
        return
    
    print(f"Processing {len(csv_files)} VIF CSV files...")
    
    # Extract VIF data from each file
    all_data = []
    for csv_file in csv_files:
        data = extract_vif_from_csv(csv_file)
        if data:
            # Only process dual tasks (with 'W' in the name)
            if 'W' not in data["task"]:
                continue
            # Filter by task name if provided
            if args.task_name and data["task"] != args.task_name:
                continue
            
            # Get feedback breaks from events files
            performance_feedback_breaks, regular_breaks, expected_breaks = get_feedback_breaks_from_events(
                events_dirs, data["subject"], data["session"], data["task"], data["run"]
            )
            
            # Add feedback breaks to the data
            data["performance_feedback_breaks"] = performance_feedback_breaks
            data["regular_breaks"] = regular_breaks
            if data["task"] == "stopSignalWDirectedForgetting":
                data["expected_breaks"] = expected_breaks
            
            all_data.append(data)
    
    if not all_data:
        print("Could not extract any VIF data.")
        return
    
    # Create master DataFrame
    master_df = pd.DataFrame(all_data)
    
    # Sort by subject, session, run, task for better organization
    # Extract numerical part of subject ID for proper sorting
    master_df['subject_num'] = master_df['subject'].str.extract(r'sub-s(\d+)').astype(int)
    master_df = master_df.sort_values(['subject_num', 'session', 'run', 'task'])
    master_df = master_df.drop(columns=['subject_num'])
    
    # Save to CSV
    task_suffix = f"_{args.task_name}" if args.task_name else ""
    output_filename = f"master_vif_table{task_suffix}.csv"
    master_df.to_csv(output_filename, index=False)
    
    print(f"Successfully created {output_filename} with {len(master_df)} entries.")
    
    # Show summary by task
    if not args.task_name:
        print("\nSummary by task:")
        if 'vif' in master_df.columns and 'performance_feedback_breaks' in master_df.columns:
            task_summary = master_df.groupby('task').agg({
                'vif': ['count', 'mean', 'std', 'min', 'max'],
                'performance_feedback_breaks': ['count', 'mean', 'std', 'min', 'max'],
                'regular_breaks': ['count', 'mean', 'std', 'min', 'max'],
                'expected_breaks': ['count', 'mean', 'std', 'min', 'max']
            })
            print(task_summary)
        else:
            task_summary = master_df.groupby('task')['vif'].agg(['count', 'mean', 'std', 'min', 'max'])
            print(task_summary)

if __name__ == "__main__":
    main() 