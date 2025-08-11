import pandas as pd
from pathlib import Path
from discovery_wm.utils import get_path_config, get_all_subj_paths, get_subj_sessions

accuracy_thresh = 0.75
rt_thresh = 1
missed_thresh = 0.10
max_stop_correct = 0.7
min_stop_correct = 0.3

def find_num_feedback_breaks(df):
    n_break = (df['trial_id'] == 'break').sum()
    n_perf = (df['trial_id'] == 'break_with_performance_feedback').sum()
    if n_perf >= 1:
        return n_perf, n_break
    else:
        return 0, n_break
    
# find the number of subjects/blocks that should have received performance feedback breaks
def find_correct_num_feedback_breaks(df):
    go_correct, sum_go_responses, go_trials, go_rt, stop_correct, stop_trials, number_of_breaks_should_have_received = 0, 0, 0, 0, 0, 0, 0
    for _, row in df.iterrows():
        if row['trial_id'] == 'break' or row['trial_id'] == 'break_with_performance_feedback':
            accuracy = go_correct / go_trials
            if sum_go_responses > 0:
                ave_rt = go_rt / sum_go_responses
            else:
                ave_rt = 0
            missed_responses = (go_trials - sum_go_responses) / go_trials
            stop_acc = stop_correct / stop_trials
            if accuracy < accuracy_thresh or ave_rt > rt_thresh or missed_responses > missed_thresh or stop_acc < min_stop_correct or stop_acc > max_stop_correct:
                number_of_breaks_should_have_received += 1
            go_correct, sum_go_responses, go_trials, go_rt, stop_correct, stop_trials = 0, 0, 0, 0, 0, 0
        else:
            if row['stop_signal_condition'] == 'go':
                go_trials += 1
                if not pd.isna(row['response_time']):
                    go_correct += row['acc']
                    go_rt += row['response_time']
                    sum_go_responses += 1
            elif row['stop_signal_condition'] == 'stop':
                stop_trials += 1
                if pd.isna(row['response_time']):
                    stop_correct += 1
    return number_of_breaks_should_have_received

def extract_subj_ses_task_run(fname):
    parts = fname.split("_")
    subj = next(p for p in parts if p.startswith("sub-"))
    ses = next(p for p in parts if p.startswith("ses-"))
    task = next(p for p in parts if p.startswith("task-")).replace("task-", "")
    run = next(p for p in parts if p.startswith("run-"))
    return subj, ses, task, run

# Set the path to your events files directory
bids_dir, _, _, _, _, _, behavioral_dir = get_path_config()

# Initialize DataFrames to store the results
observed_breaks_data = []
actual_breaks_data = []

all_subjects = get_all_subj_paths(bids_dir)
sessions_of_interest = {"ses-11", "ses-12"}
sessions_of_interest_for_some_subjects = {'ses-12', 'ses-13'}
subjects_with_different_sessions = {'sub-s1189', 'sub-s1292'}

for subj in all_subjects:
    if subj.name in subjects_with_different_sessions:
        ses_of_interest = sessions_of_interest_for_some_subjects
    else:
        ses_of_interest = sessions_of_interest
    for ses in get_subj_sessions(subj):
        if ses.name in ses_of_interest:
            func_dir = ses / "func"
            for f in func_dir.rglob("*_events.tsv"):
                df = pd.read_csv(f, sep="\t")
                subj_str, ses_str, task_str, run_str = extract_subj_ses_task_run(f.name)
                n_perf, n_break = find_num_feedback_breaks(df)
                observed_breaks_data.append({
                    'Subject': subj_str,
                    'Session': ses_str,
                    'Task': task_str,
                    'Run': run_str,
                    'Performance Feedback Breaks': n_perf,
                    'Regular Breaks': n_break
                })
                if task_str == 'stopSignalWDirectedForgetting':
                    n_should_have_received = find_correct_num_feedback_breaks(df)
                    if n_should_have_received != n_perf:
                        actual_breaks_data.append({
                            'Subject': subj_str,
                            'Session': ses_str,
                            'Task': task_str,
                            'Run': run_str,
                            'Expected Breaks': n_should_have_received,
                            'Actual Breaks': n_perf
                        })

# Convert to DataFrames and save as CSV
observed_df = pd.DataFrame(observed_breaks_data)
actual_df = pd.DataFrame(actual_breaks_data)

# Sort DataFrames - group by task first, then sort by subject and session within each task group
observed_df = observed_df.sort_values(['Task', 'Subject', 'Session'], 
                                    ascending=[True, True, True],
                                    kind='stable')  # Use stable sort to maintain original order within groups
actual_df = actual_df.sort_values(['Task', 'Subject', 'Session'], 
                                ascending=[True, True, True],
                                kind='stable')  # Use stable sort to maintain original order within groups

# Save to CSV files
observed_df.to_csv("observed_num_feedback_breaks.csv", index=False)
actual_df.to_csv("actual_num_feedback_breaks.csv", index=False)