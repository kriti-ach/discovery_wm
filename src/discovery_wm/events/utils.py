import numpy as np
import pandas as pd

def cal_time_elapsed(df):
    '''adjust time elapsed to account for trigger wait. returns updated data frame
    :df: pandas dataframe'''
    start_point = df.loc[df['trial_id'] == 'fmri_trigger_initial']

    start = start_point["time_elapsed"]
    start = start.values[0]
    df["time_elapsed"] = df["time_elapsed"] - start
    df['time_elapsed'] = df['time_elapsed'] - df['block_duration']
    return df

def get_neg_rt_correction(df):
    df.dropna(subset=['block_duration'], inplace=True)
    negative_rt = df.loc[df['rt'] < -1]
    if not negative_rt.empty:
        i = df.loc[df.rt < -1].index.values.astype(int)[0]
        trial_before = df.loc[i-1]['time_elapsed']
        problematic = df.loc[i:]
        block_durations=problematic['block_duration'].to_list()
        new_time_elapsed = []
        for n in range(len(block_durations)):
            if block_durations[n] != np.nan:
                new_time_elapsed.append(trial_before+block_durations[n])
                trial_before = trial_before+block_durations[n]
            else:
                new_time_elapsed.append(np.nan())
        new_time = df.loc[:i-1].time_elapsed.to_list()+new_time_elapsed
        df['time_elapsed'] = new_time
        return df
    else:
        return df

def add_choice_acc(df):
    '''compares key press with correct response to calculate accuracy on choice
    tasks. returns data frame with added column for choice_acc
    :df: pandas dataframe'''
    df['choice_acc'] = np.where(df['key_press'] == df['correct_response'], 1 , 0)
    return df

def get_cols_list(exp_id):
    '''uses exp_id to identify which columns to add to final event file and returns list of strings
    :exp_id: string of experiment task type'''
    common = ['trial_id', 'time_elapsed', 'rt', 'stim_duration', 'choice_acc', 'key_press', 'correct_response']
    lookup = {'stop_signal_single_task_network__fmri': common + ['SS_delay', 'SS_duration', 'stop_signal_condition',
                                                                'stop_acc', 'go_acc', 'stim'],
                'shape_matching_single_task_network__fmri': common + ['shape_matching_condition', 'probe_id', 'target_id', 'distractor_id'],
                'n_back_single_task_network__fmri': common + ['n_back_condition', 'delay', 'probe', 'letter_case'],
                'go_nogo_single_task_network__fmri': common + ['go_nogo_condition'],
                'spatial_task_switching_single_task_network__fmri': common + ['task_switch', 'whichQuadrant', 'predictable_dimension', 'number'],
                'cued_task_switching_single_task_network__fmri': common + ['cue', 'task', 'task_condition', 'cue_condition', 'stim_number'],
                'directed_forgetting_single_task_network__fmri': common + ['directed_forgetting_condition', 'cue', 'top_stim', 'bottom_stim'],
                'flanker_single_task_network__fmri': common + ['flanker_condition', 'center_letter'],
                'directed_forgetting_with_flanker__fmri': common + ['flanker_condition', 'directed_forgetting_condition'],
                'stop_signal_with_directed_forgetting__fmri': common + ['SS_delay', 'SS_duration', 'stop_signal_condition',
                                                                        'directed_forgetting_condition', 'stop_acc'],
                'stop_signal_with_flanker__fmri': common + ['SS_delay', 'SS_duration', 'stop_signal_condition', 'flanker_condition',
                                                            'SSD_congruent', 'SSD_incongruent', 'stop_acc'],
                'cued_task_switching_with_directed_forgetting__fmri': common + ['task_condition', 'cue_condition', 'task_cue',
                                                                            'directed_forgetting_condition'],
                'spatial_task_switching_with_cued_task_switching__fmri': common + ['task_switch', 'whichQuadrant', 'left_number', 'right_number', 'curr_cue'],
                'flanker_with_shape_matching__fmri': common + ['flanker_condition', 'shape_matching_condition', 'flankers', 'probe', 'target', 'distractor'],
                'flanker_with_cued_task_switching__fmri': common + ['flanker_condition', 'cue', 'task_condition', 'cue_condition', 'flanking_number'],
                'flanker_with_cued_task_switching': common + ['flanker_condition', 'cue', 'task_condition', 'cue_condition', 'flanking_number'],
                'n_back_with_shape_matching__fmri': common + ['n_back_condition', 'shape_matching_condition', 'probe', 'distractor', 'delay'],
                'shape_matching_with_spatial_task_switching__fmri': common + ['shape_matching_condition', 'task_switch', 'probe', 'target', 'distractor', 'whichQuadrant'],
                'shape_matching_with_cued_task_switching__fmri': common + ['cue', 'task_condition', 'cue_condition', 'shape_matching_condition', 'probe', 'target', 'distractor'],
                'shape_matching_with_cued_task_switching': common + ['cue', 'task_condition', 'cue_condition', 'shape_matching_condition', 'probe', 'target', 'distractor'],
                'n_back_with_spatial_task_switching__fmri': common + ['n_back_condition', 'task', 'probe', 'whichQuadrant']}
    to_add = lookup.get(exp_id)
    return to_add


def get_trial_type(exp_id):
    #add break to trial_type
    lookup ={#check if this is what we want 
            'stop_signal_single_task_network__fmri': ['stop_signal_condition'],
            'shape_matching_single_task_network__fmri': ['shape_matching_condition'],
            #n-back: first two rows missing condition value
            'n_back_single_task_network__fmri':['n_back_condition'],
            'go_nogo_single_task_network__fmri': ['go_nogo_condition'],
            #spatialTS: check if this is what we want
            'spatial_task_switching_single_task_network__fmri': ['task_switch'], # should this be predictable_condition? 
            #cuedTS: task and cue conditions combined in orderlo
            'cued_task_switching_single_task_network__fmri': ['task_condition', 'cue_condition'],
            'directed_forgetting_single_task_network__fmri': ['directed_forgetting_condition'],
            'flanker_single_task_network__fmri': ['flanker_condition'],
            'directed_forgetting_with_flanker__fmri': ['flanker_condition', 'directed_forgetting_condition'],
            'stop_signal_with_directed_forgetting__fmri': ['stop_signal_condition', "directed_forgetting_condition"],
            # stopsignal with flanker: stop signal and flanker conditions combined
            'stop_signal_with_flanker__fmri': ['stop_signal_condition', 'flanker_condition'],
            # LB: ADDED NEW ONES BELOW -> seems that some of the dual tasks ones were missing. 
            'cued_task_switching_with_directed_forgetting__fmri': ['directed_forgetting_condition', 'task_condition', 'cue_condition'],
            'spatial_task_switching_with_cued_task_switching__fmri': ['task_switch'],
            'flanker_with_shape_matching__fmri': ['flanker_condition', 'shape_matching_condition'],
            'flanker_with_cued_task_switching__fmri': ['cue_condition', 'task_condition', 'flanker_condition'],
            'flanker_with_cued_task_switching': ['cue_condition', 'task_condition', 'flanker_condition'],
            'n_back_with_shape_matching__fmri': ['n_back_condition', 'shape_matching_condition', 'delay'],
            'shape_matching_with_spatial_task_switching__fmri': ['predictable_condition', 'shape_matching_condition'],
            'shape_matching_with_spatial_task_switching': ['predictable_condition', 'shape_matching_condition'],
            'shape_matching_with_cued_task_switching__fmri': ['task_condition', 'cue_condition', 'shape_matching_condition'],
            'n_back_with_spatial_task_switching__fmri': ['n_back_condition', 'task_switch_condition']
    }
    original_col = lookup.get(exp_id)
    return original_col

def add_cols(df, exp_id):
    '''chooses and adds columns into final dataframe based on task type
    :df: pandas dataframe
    :exp_id: string of experiment id'''

    if 'cued_task_switching' in exp_id:
        #change cell value 'na' in 'task_condition' to 'n/a'
        df['task_condition'] = df['task_condition'].replace('na', 'n/a')
        df['cue_condition'] = df['cue_condition'].replace('na', 'n/a')
    
    if exp_id == 'spatial_task switching_single_task_network__fmri':
        df['task_switch'] = df['task_switch'].replace('na', 'n/a')
    
    if exp_id == 'spatial_task_switching_with_cued_task_switching__fmri':
        df['task_switch'] = df['task_switch'].replace('na', 'n/a')

    df2 = pd.DataFrame()
    to_add = get_cols_list(exp_id)
    final = df[to_add]
    trial_types = get_trial_type(exp_id)

    if trial_types == None:
        print(f'Missing trial type key for: {exp_id}')

    if len(trial_types) > 1:
        if exp_id == 'cued_task_switching_single_task_network__fmri':
            df2['trial_type'] = 't'+df[trial_types[0]]+'_c'+df[trial_types[1]]
        elif exp_id == "cued_task_switching_with_directed_forgetting__fmri":
            df2['trial_type'] = df[trial_types[0]]+"_t"+df[trial_types[1]]+"_c"+df[trial_types[2]]
        elif exp_id == "shape_matching_with_cued_task_switching__fmri":
            df2['trial_type'] = 't'+df[trial_types[0]]+'_c'+df[trial_types[1]]
        elif exp_id == "flanker_with_cued_task_switching__fmri":
            df2['trial_type'] = 'c'+df[trial_types[0]]+'_t'+df[trial_types[1]]+ "_" + df[trial_types[2]]
        elif exp_id == 'n_back_with_shape_matching__fmri':
            df2['trial_type'] = df[trial_types[0]]+"_"+df[trial_types[1]]+"_"+df[trial_types[2]].astype(str)+"back"
            df2['trial_type'] = df2['trial_type'].str.replace('.0back', 'back')
        else:
            df2['trial_type'] = df[trial_types[0]]+"_"+df[trial_types[1]]

    if exp_id == "flanker_with_cued_task_switching__fmri":
        df2['trial_type'] = df2['trial_type'].shift(1)
    
    if len(trial_types) == 1: 
        tmp = trial_types[0]
        df2['trial_type'] = df[tmp]

    if exp_id == 'shape_matching_with_spatial_task_switching__fmri':
        df2['trial_type'] = df2['trial_type'].str.split('_').str[2:].str.join('_')

    if exp_id == 'spatial_task_switching_single_task_network__fmri':
        final = final.rename(columns = {'predictable_dimension': 'task_set'})

    if exp_id == 'cued_task_switching_with_directed_forgetting__fmri':
        final.loc[final['key_press'] == 84.0, ['rt']] = pd.NA
        final.loc[final['key_press'] == 84.0, ['key_press']] = -1

    final = final.assign(trial_type = df2)
    return final

def cleanup_events(task, df):
    special_list = ['stopSignal', 'goNogo', 'stopSignalWDirectedForgetting', 'stopSignalWFlanker']
    if task in special_list:
        df2 = globals()[task](df)
        return df2
    else:
        return df

def stopSignal(df):
    # Create a copy to avoid modifying the original dataframe
    df = df.copy()
    
    # Only apply conditions to test_trial rows
    mask = df['trial_id'] == 'test_trial'
    
    # Get the subset of rows that are test_trial
    trial_rows = df[mask]
    
    choice_acc_str = trial_rows['choice_acc'].astype(str)
    
    conditions = [
        (trial_rows['trial_type']=='go'),
        (trial_rows['trial_type']=='stop') & (choice_acc_str=='1'),
        (trial_rows['trial_type']=='stop') & (choice_acc_str=='0')
    ]
    values = ['go', 'stop_success', 'stop_failure']
    result = np.select(conditions, values, default='unknown')
    
    # Update only the test_trial rows
    df.loc[mask, 'trial_type'] = result
    
    # Ensure fixation rows have a consistent trial_type
    fixation_mask = df['trial_id'] == 'test_fixation'
    df.loc[fixation_mask, 'trial_type'] = 'fixation'
    
    return df

def goNogo(df):
    choice_acc_str = df['choice_acc'].astype(str)
    
    conditions = [
        (df['trial_type']=='nogo') & (choice_acc_str=='1'),
        (df['trial_type']=='nogo') & (choice_acc_str=='0'),
        (df['trial_type']=='go')
    ]
    values = ['nogo_success', 'nogo_failure', 'go']
    result = np.select(conditions, values, default='unknown')
    df['trial_type'] = pd.Series(result).astype(object)
    return df


def stopSignalWDirectedForgetting(df):
    # Convert numeric columns to strings for comparison
    mask = df['trial_id'] == 'test_trial'
    trial_rows = df[mask]
    
    conditions = [
        (trial_rows['stop_signal_condition']=='go') & (trial_rows['directed_forgetting_condition']=='con'),
        (trial_rows['stop_signal_condition']=='go') & (trial_rows['directed_forgetting_condition']=='pos'),
        (trial_rows['stop_signal_condition']=='go') & (trial_rows['directed_forgetting_condition']=='neg'),
        (trial_rows['stop_signal_condition']=='stop') & (trial_rows['directed_forgetting_condition']=='con') & (trial_rows['stop_acc']==1),
        (trial_rows['stop_signal_condition']=='stop') & (trial_rows['directed_forgetting_condition']=='pos') & (trial_rows['stop_acc']==1),
        (trial_rows['stop_signal_condition']=='stop') & (trial_rows['directed_forgetting_condition']=='neg') & (trial_rows['stop_acc']==1),
        (trial_rows['stop_signal_condition']=='stop') & (trial_rows['directed_forgetting_condition']=='con') & (trial_rows['stop_acc']==0),
        (trial_rows['stop_signal_condition']=='stop') & (trial_rows['directed_forgetting_condition']=='pos') & (trial_rows['stop_acc']==0),
        (trial_rows['stop_signal_condition']=='stop') & (trial_rows['directed_forgetting_condition']=='neg') & (trial_rows['stop_acc']==0),
        (trial_rows['trial_type']=='memory_cue')
    ]
    values = ['go_con', 'go_pos', 'go_neg', 'stop_success_con', 'stop_success_pos', 'stop_success_neg', 'stop_failure_con', 'stop_failure_pos', 'stop_failure_neg', 'memory_cue']
    # Use a default value that's a string
    result = np.select(conditions, values, default='unknown')
    df.loc[mask, 'trial_type'] = result
    # Ensure fixation rows have a consistent trial_type
    fixation_mask = df['trial_id'] == 'test_fixation'
    df.loc[fixation_mask, 'trial_type'] = 'fixation'
    
    return df

def stopSignalWFlanker(df):

    mask = df['trial_id'] == 'test_trial'
    trial_rows = df[mask]
    
    conditions = [
        (trial_rows['stop_signal_condition']=='go') & (trial_rows['flanker_condition']=='congruent'),
        (trial_rows['stop_signal_condition']=='go') & (trial_rows['flanker_condition']=='incongruent'),
        (trial_rows['stop_signal_condition']=='stop') & (trial_rows['flanker_condition']=='congruent') & (trial_rows['stop_acc']==1),
        (trial_rows['stop_signal_condition']=='stop') & (trial_rows['flanker_condition']=='incongruent') & (trial_rows['stop_acc']==1),
        (trial_rows['stop_signal_condition']=='stop') & (trial_rows['flanker_condition']=='congruent') & (trial_rows['stop_acc']==0),
        (trial_rows['stop_signal_condition']=='stop') & (trial_rows['flanker_condition']=='incongruent') & (trial_rows['stop_acc']==0)
    ]
    values = ['go_congruent', 'go_incongruent', 'stop_success_congruent', 'stop_success_incongruent', 'stop_failure_congruent', 'stop_failure_incongruent']
    result = np.select(conditions, values, default='unknown')
    df.loc[mask, 'trial_type'] = result
    
    fixation_mask = df['trial_id'] == 'test_fixation'
    df.loc[fixation_mask, 'trial_type'] = 'fixation'
    return df

def response_time_and_junk(df, task):
    df = cleanup_events(task, df)
    df.replace('', np.nan, inplace=True)
    return df