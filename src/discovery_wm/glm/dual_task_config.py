dual_tasks_regressor_config = {
    "directedForgettingWCuedTS": {
        "omission": {
            "amplitude_column": "omission",
            "duration_column": "constant_1_column",
            "subset": 'trial_type != "n/a"',
        },
        "commission": {
            "amplitude_column": "commission",
            "duration_column": "constant_1_column",
            "subset": 'trial_type != "n/a"',
        },
        "rt_fast": {
            "amplitude_column": "rt_fast",
            "duration_column": "constant_1_column",
            "subset": 'trial_type != "n/a"',
        },
        "neg_tswitch_cswitch": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                'trial_type == "neg_tswitch_cswitch" and '
                'key_press == correct_response and response_time >= 0.2'
            ),
        },
        "neg_tstay_cswitch": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                'trial_type == "neg_tstay_cswitch" and '
                'key_press == correct_response and response_time >= 0.2'
            ),
        },
        "neg_tstay_cstay": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                'trial_type == "neg_tstay_cstay" and '
                'key_press == correct_response and response_time >= 0.2'
            ),
        }, 
        "pos_tswitch_cswitch": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                'trial_type == "pos_tswitch_cswitch" and '
                'key_press == correct_response and response_time >= 0.2'
            ),
        },
        "pos_tstay_cswitch": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                'trial_type == "pos_tstay_cswitch" and '
                'key_press == correct_response and response_time >= 0.2'
            ),
        },
        "pos_tstay_cstay": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                'trial_type == "pos_tstay_cstay" and '
                'key_press == correct_response and response_time >= 0.2'
            ),
        },
        "con_tswitch_cswitch": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                'trial_type == "con_tswitch_cswitch" and '
                'key_press == correct_response and response_time >= 0.2'
            ),
        },
        "con_tstay_cswitch": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                'trial_type == "con_tstay_cswitch" and '
                'key_press == correct_response and response_time >= 0.2'
            ),
        },
        "con_tstay_cstay": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                'trial_type == "con_tstay_cstay" and '
                'key_press == correct_response and response_time >= 0.2'
            ),
        },
        "response_time": {
            "amplitude_column": "response_time_centered",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_id == 'test_trial' and trial_type != 'n/a' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        }
    },
    "directedForgettingWFlanker": {
        "omission": {
            "amplitude_column": "omission",
            "duration_column": "constant_1_column",
            "subset": None,
        },
        "commission": {
            "amplitude_column": "commission",
            "duration_column": "constant_1_column",
            "subset": None,
        },
        "rt_fast": {
            "amplitude_column": "rt_fast",
            "duration_column": "constant_1_column",
            "subset": None,
        },
        "memory_and_cue": {
            "amplitude_column": "constant_1_column",
            "duration_column": "duration",
            "subset": 'trial_id == "test_four_letters" or trial_id == "test_cue"',
        },
        "congruent_pos": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                'key_press == correct_response and response_time >= 0.2 '
                'and trial_type == "congruent_pos"'
            ),
        },
        "congruent_neg": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                'key_press == correct_response and response_time >= 0.2 '
                'and trial_type == "congruent_neg"'
            ),
        },
        "congruent_con": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                'key_press == correct_response and response_time >= 0.2 '
                'and trial_type == "congruent_con"'
            ),
        },
        "incongruent_pos": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                'key_press == correct_response and response_time >= 0.2 '
                'and trial_type == "incongruent_pos"'
            ),
        },
        "incongruent_neg": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                'key_press == correct_response and response_time >= 0.2 '
                'and trial_type == "incongruent_neg"'
            ),
        },
        "incongruent_con": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                'key_press == correct_response and response_time >= 0.2 '
                'and trial_type == "incongruent_con"'
            ),
        },
        "response_time": {
            "amplitude_column": "response_time_centered",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 "
                "and trial_id == 'test_trial'"
            ),
        }
    },
    "stopSignalWDirectedForgetting": {
        "go_omission": {
            "amplitude_column": "omission",
            "duration_column": "constant_1_column",
            "subset": None,
        },
        "go_commission": {
            "amplitude_column": "commission",
            "duration_column": "constant_1_column",
            "subset": None,
        },
        "go_rt_fast": {
            "amplitude_column": "rt_fast",
            "duration_column": "constant_1_column",
            "subset": None,
        },
        "go_pos": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 "
                "and trial_type == 'go_pos'"
            ),
        },
        "go_neg": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 "
                "and trial_type == 'go_neg'"
            ),
        },
        "go_con": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 "
                "and trial_type == 'go_con'"
            ),
        },
        "stop_success_pos": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'stop_success_pos'"
            ),
        },
        "stop_success_neg": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'stop_success_neg'"
            ),
        },
        "stop_success_con": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'stop_success_con'"
            ),
        },
        "stop_failure_pos": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'stop_failure_pos'"
            ),
        },
        "stop_failure_neg": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'stop_failure_neg'"
            ),
        },
        "stop_failure_con": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'stop_failure_con'"
            ),
        },
        "memory_and_cue": {
            "amplitude_column": "constant_1_column",
            "duration_column": "duration",
            "subset": 'trial_id == "test_cue"',
        },
        "response_time": {
            "amplitude_column": "response_time_centered",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 "
                "and trial_type.isin(['go_pos', 'go_neg', 'go_con'])"
            ),
        }
    },
    "stopSignalWFlanker": {
        "go_omission": {
            "amplitude_column": "omission",
            "duration_column": "constant_1_column",
            "subset": None,
        },
        "go_commission": {
            "amplitude_column": "commission",
            "duration_column": "constant_1_column",
            "subset": None,
        },
        "go_rt_fast": {
            "amplitude_column": "rt_fast",
            "duration_column": "constant_1_column",
            "subset": None,
        },
        "go_congruent": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 "
                "and trial_type == 'go_congruent'"
            ),
        },
        "go_incongruent": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 "
                "and trial_type == 'go_incongruent'"
            ),
        },
        "stop_success_congruent": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'stop_success_congruent'"
            ),
        },
        "stop_success_incongruent": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'stop_success_incongruent'"
            ),
        },
        "stop_failure_congruent": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'stop_failure_congruent'"
            ),
        },
        "stop_failure_incongruent": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'stop_failure_incongruent'"
            ),
        },
        "response_time": {
            "amplitude_column": "response_time_centered",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 "
                "and trial_type.isin(['go_congruent', 'go_incongruent'])"
            ),
        }
    },
    "spatialTSWCuedTS": {
        "omission": {
            "amplitude_column": "omission",
            "duration_column": "constant_1_column",
            "subset": "trial_type != 'tn/a_cn/a'",
        },
        "commission": {
            "amplitude_column": "commission",
            "duration_column": "constant_1_column",
            "subset": "trial_type != 'tn/a_cn/a'",
        },
        "rt_fast": {
            "amplitude_column": "rt_fast",
            "duration_column": "constant_1_column",
            "subset": "trial_type != 'tn/a_cn/a'",
        },
        "cuedtstaycstay_spatialtstaycstay": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                'trial_type == "cuedtstaycstay_spatialtstaycstay" and '
                'key_press == correct_response and response_time >= 0.2'
            ),
        },
        "cuedtstaycstay_spatialtstaycswitch": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                'trial_type == "cuedtstaycstay_spatialtstaycswitch" and '
                'key_press == correct_response and response_time >= 0.2'
            ),
        },
        "cuedtstaycstay_spatialtswitchcswitch": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                'trial_type == "cuedtstaycstay_spatialtswitchcswitch" and '
                'key_press == correct_response and response_time >= 0.2'
            ),
        },
        "cuedtstaycswitch_spatialtstaycstay": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                'trial_type == "cuedtstaycswitch_spatialtstaycstay" and '
                'key_press == correct_response and response_time >= 0.2'
            ),
        },
        "cuedtstaycswitch_spatialtstaycswitch": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                'trial_type == "cuedtstaycswitch_spatialtstaycswitch" and '
                'key_press == correct_response and response_time >= 0.2'
            ),
        },
        "cuedtstaycswitch_spatialtswitchcswitch": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                'trial_type == "cuedtstaycswitch_spatialtswitchcswitch" and '
                'key_press == correct_response and response_time >= 0.2'
            ),
        },
        "cuedtswitchcswitch_spatialtstaycstay": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                'trial_type == "cuedtswitchcswitch_spatialtstaycstay" and key_press == correct_response and '
                'response_time >= 0.2'
            ),
        },
        "cuedtswitchcswitch_spatialtstaycswitch": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                'trial_type == "cuedtswitchcswitch_spatialtstaycswitch" and key_press == correct_response and '
                'response_time >= 0.2'
            ),
        },
        "cuedtswitchcswitch_spatialtswitchcswitch": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                'trial_type == "cuedtswitchcswitch_spatialtswitchcswitch" and key_press == correct_response and '
                'response_time >= 0.2'
            ),
        },
        "response_time": {
            "amplitude_column": "response_time_centered",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_id == 'test_trial' and trial_type != 'n/a' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        }
    },
    "flankerWShapeMatching": {
        "omission": {
            "amplitude_column": "omission",
            "duration_column": "constant_1_column",
            "subset": None,
        },
        "commission": {
            "amplitude_column": "commission",
            "duration_column": "constant_1_column",
            "subset": None,
        },
        "rt_fast": {
            "amplitude_column": "rt_fast",
            "duration_column": "constant_1_column",
            "subset": None,
        },
        "congruent_SSS": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 and "
                "trial_type == 'congruent_SSS'"
            ),
        },
        "congruent_SDD": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 and "
                "trial_type == 'congruent_SDD'"
            ),
        },
        "congruent_SNN": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 and "
                "trial_type == 'congruent_SNN'"
            ),
        },
        "congruent_DSD": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 and "
                "trial_type == 'congruent_DSD'"
            ),
        },
        "congruent_DDD": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 and "
                "trial_type == 'congruent_DDD'"
            ),
        },
        "congruent_DDS": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 and "
                "trial_type == 'congruent_DDS'"
            ),
        },
        "congruent_DNN": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 and "
                "trial_type == 'congruent_DNN'"
            ),
        },
        "incongruent_SSS": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 and "
                "trial_type == 'incongruent_SSS'"
            ),
        },
        "incongruent_SDD": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 and "
                "trial_type == 'incongruent_SDD'"
            ),
        },
        "incongruent_SNN": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 and "
                "trial_type == 'incongruent_SNN'"
            ),
        },
        "incongruent_DSD": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 and "
                "trial_type == 'incongruent_DSD'"
            ),
        },
        "incongruent_DDD": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 and "
                "trial_type == 'incongruent_DDD'"
            ),
        },
        "incongruent_DDS": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 and "
                "trial_type == 'incongruent_DDS'"
            ),
        },
        "incongruent_DNN": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 and "
                "trial_type == 'incongruent_DNN'"
            ),
        },
        "response_time": {
            "amplitude_column": "response_time_centered",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 and "
                "trial_id == 'test_trial'"
            ),
        }
    },
    "cuedTSWFlanker": {
        "omission": {
            "amplitude_column": "omission",
            "duration_column": "constant_1_column",
            "subset": "trial_type != 'n/a'",
        },
        "commission": {
            "amplitude_column": "commission",
            "duration_column": "constant_1_column",
            "subset": "trial_type != 'n/a'",
        },
        "rt_fast": {
            "amplitude_column": "rt_fast",
            "duration_column": "constant_1_column",
            "subset": "trial_type != 'n/a'",
        },
        "cstay_tstay_congruent": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'cstay_tstay_congruent' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "cstay_tstay_incongruent": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'cstay_tstay_incongruent' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "cswitch_tswitch_congruent": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'cswitch_tswitch_congruent' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "cswitch_tswitch_incongruent": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'cswitch_tswitch_incongruent' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "cswitch_tstay_congruent": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'cswitch_tstay_congruent' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "cswitch_tstay_incongruent": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'cswitch_tstay_incongruent' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "response_time": {
            "amplitude_column": "response_time_centered",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_id == 'test_trial' and trial_type != 'n/a' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        }
    },
    "spatialTSWShapeMatching": {
        "omission": {
            "amplitude_column": "omission",
            "duration_column": "constant_1_column",
            "subset": "trial_type != 'tn/a_cn/a'",
        },
        "commission": {
            "amplitude_column": "commission",
            "duration_column": "constant_1_column",
            "subset": "trial_type != 'tn/a_cn/a'",
        },
        "rt_fast": {
            "amplitude_column": "rt_fast",
            "duration_column": "constant_1_column",
            "subset": "trial_type != 'tn/a_cn/a'",
        },
        "tstay_cstay_SSS": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'tstay_cstay_SSS' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "tstay_cstay_SDD": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'tstay_cstay_SDD' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "tstay_cstay_SNN": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'tstay_cstay_SNN' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "tstay_cstay_DSD": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'tstay_cstay_DSD' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "tstay_cstay_DNN": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'tstay_cstay_DNN' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "tstay_cstay_DDD": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'tstay_cstay_DDD' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "tstay_cstay_DDS": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'tstay_cstay_DDS' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "tstay_cswitch_SSS": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'tstay_cswitch_SSS' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "tstay_cswitch_SDD": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'tstay_cswitch_SDD' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "tstay_cswitch_SNN": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'tstay_cswitch_SNN' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "tstay_cswitch_DSD": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'tstay_cswitch_DSD' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "tstay_cswitch_DNN": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'tstay_cswitch_DNN' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "tstay_cswitch_DDD": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'tstay_cswitch_DDD' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "tstay_cswitch_DDS": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'tstay_cswitch_DDS' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "tswitch_cswitch_SSS": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'tswitch_cswitch_SSS' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "tswitch_cswitch_SDD": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'tswitch_cswitch_SDD' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "tswitch_cswitch_SNN": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'tswitch_cswitch_SNN' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "tswitch_cswitch_DSD": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'tswitch_cswitch_DSD' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "tswitch_cswitch_DNN": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'tswitch_cswitch_DNN' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "tswitch_cswitch_DDD": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'tswitch_cswitch_DDD' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "tswitch_cswitch_DDS": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'tswitch_cswitch_DDS' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "response_time": {
            "amplitude_column": "response_time_centered",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_id == 'test_trial' and trial_type != 'n/a' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        }
    },
    "nBackWShapeMatching": {
        "omission": {
            "amplitude_column": "omission",
            "duration_column": "constant_1_column",
            "subset": "trial_type != 'n/a'",
        },
        "commission": {
            "amplitude_column": "commission",
            "duration_column": "constant_1_column",
            "subset": "trial_type != 'n/a'",
        },
        "rt_fast": {
            "amplitude_column": "rt_fast",
            "duration_column": "constant_1_column",
            "subset": "trial_type != 'n/a'",
        },
        "match_td_same_1back": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'match_td_same_1back' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "match_td_same_2back": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'match_td_same_2back' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "match_td_diff_1back": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'match_td_diff_1back' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "match_td_diff_2back": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'match_td_diff_2back' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "match_td_na_1back": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'match_td_na_1back' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "match_td_na_2back": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'match_td_na_2back' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "mismatch_td_same_1back": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'mismatch_td_same_1back' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "mismatch_td_same_2back": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'mismatch_td_same_2back' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "mismatch_td_diff_1back": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'mismatch_td_diff_1back' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "mismatch_td_diff_2back": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'mismatch_td_diff_2back' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "mismatch_td_na_1back": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'mismatch_td_na_1back' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "mismatch_td_na_2back": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'mismatch_td_na_2back' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "response_time": {
            "amplitude_column": "response_time_centered",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_id == 'test_trial' and trial_type != 'n/a' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        }
    },
    "nBackWSpatialTS": {
        "omission": {
            "amplitude_column": "omission",
            "duration_column": "constant_1_column",
            "subset": "trial_type != 'tn/a_cn/a'",
        },
        "commission": {
            "amplitude_column": "commission",
            "duration_column": "constant_1_column",
            "subset": "trial_type != 'tn/a_cn/a'",
        },
        "rt_fast": {
            "amplitude_column": "rt_fast",
            "duration_column": "constant_1_column",
            "subset": "trial_type != 'tn/a_cn/a'",
        },
        "match_tstay_cstay_1back": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'match_tstay_cstay' and task == '1-back' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "match_tstay_cswitch_1back": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'match_tstay_cswitch' and task == '1-back' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "match_tswitch_cswitch_1back": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'match_tswitch_cswitch' and task == '1-back' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "mismatch_tstay_cstay_1back": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'mismatch_tstay_cstay' and task == '1-back' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "mismatch_tstay_cswitch_1back": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'mismatch_tstay_cswitch' and task == '1-back' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "mismatch_tswitch_cswitch_1back": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'mismatch_tswitch_cswitch' and task == '1-back' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "match_tstay_cstay_2back": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'match_tstay_cstay' and task == '2-back' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "match_tstay_cswitch_2back": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'match_tstay_cswitch' and task == '2-back' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "match_tswitch_cswitch_2back": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'match_tswitch_cswitch' and task == '2-back' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "mismatch_tstay_cstay_2back": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'mismatch_tstay_cstay' and task == '2-back' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "mismatch_tstay_cswitch_2back": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'mismatch_tstay_cswitch' and task == '2-back' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "mismatch_tswitch_cswitch_2back": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_type == 'mismatch_tswitch_cswitch' and task == '2-back' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        },
        "response_time": {
            "amplitude_column": "response_time_centered",
            "duration_column": "constant_1_column",
            "subset": (
                "trial_id == 'test_trial' and trial_type != 'n/a' and "
                "key_press == correct_response and response_time >= 0.2"
            ),
        }
    },
    "shapeMatchingWCuedTS": {
        "omission": {
            "amplitude_column": "omission",
            "duration_column": "constant_1_column",
            "subset": None,
        },
        "commission": {
            "amplitude_column": "commission",
            "duration_column": "constant_1_column",
            "subset": None,
        },
        "rt_fast": {
            "amplitude_column": "rt_fast",
            "duration_column": "constant_1_column",
            "subset": None,
        },
        "SSS_tswitch_cswitch": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 and "
                "trial_type == 'SSS_tswitch_cswitch'"
            ),
        },
        "SSS_tstay_cswitch": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 and "
                "trial_type == 'SSS_tstay_cswitch'"
            ),
        },
        "SSS_tstay_cstay": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 and "
                "trial_type == 'SSS_tstay_cstay'"
            ),
        },
        "SDD_tswitch_cswitch": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 and "
                "trial_type == 'SDD_tswitch_cswitch'"
            ),
        },
        "SDD_tstay_cswitch": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 and "
                "trial_type == 'SDD_tstay_cswitch'"
            ),
        },
        "SDD_tstay_cstay": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 and "
                "trial_type == 'SDD_tstay_cstay'"
            ),
        }, 
        "SNN_tswitch_cswitch": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 and "
                "trial_type == 'SNN_tswitch_cswitch'"
            ),
        },
        "SNN_tstay_cswitch": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 and "
                "trial_type == 'SNN_tstay_cswitch'"
            ),
        },
        "SNN_tstay_cstay": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 and "
                "trial_type == 'SNN_tstay_cstay'"
            ),
        },
        "DSD_tswitch_cswitch": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 and "
                "trial_type == 'DSD_tswitch_cswitch'"
            ),
        },
        "DSD_tstay_cswitch": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 and "
                "trial_type == 'DSD_tstay_cswitch'"
            ),
        },
        "DSD_tstay_cstay": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 and "
                "trial_type == 'DSD_tstay_cstay'"
            ),
        },
        "DDD_tswitch_cswitch": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 and "
                "trial_type == 'DDD_tswitch_cswitch'"
            ),
        },
        "DDD_tstay_cswitch": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 and "
                "trial_type == 'DDD_tstay_cswitch'"
            ),
        },
        "DDD_tstay_cstay": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 and "
                "trial_type == 'DDD_tstay_cstay'"
            ),
        },
        "DDS_tswitch_cswitch": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 and "
                "trial_type == 'DDS_tswitch_cswitch'"
            ),
        },
        "DDS_tstay_cswitch": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 and "
                "trial_type == 'DDS_tstay_cswitch'"
            ),
        },
        "DDS_tstay_cstay": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 and "
                "trial_type == 'DDS_tstay_cstay'"
            ),
        },
        "DNN_tswitch_cswitch": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 and "
                "trial_type == 'DNN_tswitch_cswitch'"
            ),
        },
        "DNN_tstay_cswitch": {
            "amplitude_column": "constant_1_column",   
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 and "
                "trial_type == 'DNN_tstay_cswitch'"
            ),
        },
        "DNN_tstay_cstay": {
            "amplitude_column": "constant_1_column",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 and "
                "trial_type == 'DNN_tstay_cstay'"
            ),
        },
        "response_time": {
            "amplitude_column": "response_time_centered",
            "duration_column": "constant_1_column",
            "subset": (
                "key_press == correct_response and response_time >= 0.2 and "
                "trial_id == 'test_trial'"
            ),
        }
    }
}

dual_tasks_config = {
    "directedForgettingWCuedTS": {
        # Each trial type - baseline
        "neg_tswitch_cswitch": "neg_tswitch_cswitch",
        "neg_tstay_cswitch": "neg_tstay_cswitch",
        "neg_tstay_cstay": "neg_tstay_cstay",
        "pos_tswitch_cswitch": "pos_tswitch_cswitch",
        "pos_tstay_cswitch": "pos_tstay_cswitch",
        "pos_tstay_cstay": "pos_tstay_cstay",
        "con_tswitch_cswitch": "con_tswitch_cswitch",
        "con_tstay_cswitch": "con_tstay_cswitch",
        "con_tstay_cstay": "con_tstay_cstay",
        
        # Cue switch cost while directedForgetting is "off"
        "con_tstay_cswitch-con_tstay_cstay": "con_tstay_cswitch-con_tstay_cstay",
        
        # Task switch cost while directedForgetting is "off"
        "con_tswitch_cswitch-con_tstay_cswitch": "con_tswitch_cswitch-con_tstay_cswitch",
        
        # DirectedForgetting contrast while cuedTS is "off"
        "neg_tstay_cstay-con_tstay_cstay": "neg_tstay_cstay-con_tstay_cstay",
        
        # Cue switch cost across all DF conditions
        "directedForgettingWCuedTS_directedForgetting_cue_switch_cost":
            "1/3*(neg_tstay_cswitch+pos_tstay_cswitch+con_tstay_cswitch)-1/3*(neg_tstay_cstay+pos_tstay_cstay+con_tstay_cstay)",
        
        # Task switch cost across all DF conditions
        "directedForgettingWCuedTS_directedForgetting_task_switch_cost":
            "1/3*(neg_tswitch_cswitch+pos_tswitch_cswitch+con_tswitch_cswitch)-1/3*(neg_tstay_cswitch+pos_tstay_cswitch+con_tstay_cswitch)",
        
        # DirectedForgetting contrast across all cuedTS conditions
        "directedForgettingWCuedTS_directedForgetting_contrast_across_cuedTS":
            "1/3*(neg_tstay_cstay+neg_tstay_cswitch+neg_tswitch_cswitch)-1/3*(con_tstay_cstay+con_tstay_cswitch+con_tswitch_cswitch)",
        
        # Cue switch cost interaction
        "directedForgettingWCuedTS_cue_switch_cost_interaction":
            "1/2*(neg_tstay_cswitch-con_tstay_cswitch)-1/2*(neg_tstay_cstay-con_tstay_cstay)",
        
        # Task switch cost interaction
        "directedForgettingWCuedTS_task_switch_cost_interaction":
            "1/2*(neg_tswitch_cswitch-con_tswitch_cswitch)-1/2*(neg_tstay_cswitch-con_tstay_cswitch)",
        
        # Task - baseline
        "task-baseline":
            "1/9*(neg_tswitch_cswitch+neg_tstay_cswitch+neg_tstay_cstay+pos_tswitch_cswitch+pos_tstay_cswitch+"
            "pos_tstay_cstay+con_tswitch_cswitch+con_tstay_cswitch+con_tstay_cstay)",
        
        "response_time": "response_time"
    },
    
    "directedForgettingWFlanker": {
        "congruent_pos": "congruent_pos",
        "congruent_neg": "congruent_neg",
        "congruent_con": "congruent_con",
        "incongruent_pos": "incongruent_pos",
        "incongruent_neg": "incongruent_neg",
        "incongruent_con": "incongruent_con",
        
        "congruent_neg-congruent_con": "congruent_neg-congruent_con",
        "incongruent_con-congruent_con": "incongruent_con-congruent_con",
        
        # Interaction contrast
        "directedForgettingWFlanker_interaction":
            "1/2*(incongruent_neg+congruent_con)-1/2*(incongruent_con+congruent_neg)",

        # Task - baseline
        "task-baseline":
            "1/7*(congruent_pos+congruent_neg+congruent_con+incongruent_pos+incongruent_neg+incongruent_con+memory_and_cue)",
        
        "response_time": "response_time"
    },
    
    "stopSignalWDirectedForgetting": {
        "go_pos": "go_pos",
        "go_neg": "go_neg",
        "go_con": "go_con",
        "stop_success_pos": "stop_success_pos",
        "stop_success_neg": "stop_success_neg",
        "stop_success_con": "stop_success_con",
        "stop_failure_pos": "stop_failure_pos",
        "stop_failure_neg": "stop_failure_neg",
        "stop_failure_con": "stop_failure_con",
        "go_neg-go_con": "go_neg-go_con",
        "stop_success_con-go_con": "stop_success_con-go_con",
        "(stop_success_con+stop_success_pos+stop_success_neg)-(go_con+go_pos_+go_neg)":
            "1/3*(stop_success_con+stop_success_pos+stop_success_neg)-1/3*(go_con+go_pos+go_neg)",
        
        "(stop_failure_con+stop_failure_pos+stop_failure_neg)-(go_con+go_pos_+go_neg)":
            "1/3*(stop_failure_con+stop_failure_pos+stop_failure_neg)-1/3*(go_con+go_pos+go_neg)",
        
        # Interaction contrasts
        "(stop_success_neg-go_neg)-(stop_success_con-go_con)":
            "1/2*(stop_success_neg-go_neg)-1/2*(stop_success_con-go_con)",
        
        "(stop_failure_neg-go_neg)-(stop_failure_con-go_con)":
            "1/2*(stop_failure_neg-go_neg)-1/2*(stop_failure_con-go_con)",
        
        # Task - baseline
        "task-baseline":
            "1/10*(go_pos+go_neg+go_con+stop_success_pos+stop_success_neg+"
            "stop_success_con+stop_failure_pos+stop_failure_neg+stop_failure_con+memory_and_cue)",
        
        "response_time": "response_time"
    },
    "stopSignalWFlanker": {
        "go_congruent": "go_congruent",
        "go_incongruent": "go_incongruent",
        "stop_success_congruent": "stop_success_congruent",
        "stop_success_incongruent": "stop_success_incongruent",
        "stop_failure_congruent": "stop_failure_incongruent",
        "stop_failure_incongruent": "stop_failure_incongruent",
        "go_incongruent-go_congruent": "go_incongruent-go_congruent",

        "(stop_success_congruent+stop_success_incongruent)-(go_congruent+go_incongruent)": (
            "1/2*(stop_success_congruent+stop_success_incongruent)-1/2*(go_congruent+go_incongruent)"
            ),
        "(stop_failure_congruent+stop_failure_incongruent)-(go_congruent+go_incongruent)": (
            "1/2*(stop_failure_congruent+stop_failure_incongruent)-1/2*(go_congruent+go_incongruent)"
            ),

        # Interaction contrasts
        "(stop_success_incongruent-go_incongruent)-(stop_success_congruent-go_congruent)": (
            "1/2*(stop_success_incongruent-go_incongruent)-1/2*(stop_success_congruent-go_congruent)"
            ),
        "(stop_failure_incongruent-go_incongruent)-(stop_failure_congruent-go_congruent)": (
            "1/2*(stop_failure_incongruent-go_incongruent)-1/2*(stop_failure_congruent-go_congruent)"
            ),
        "stop_success_congruent-go_congruent": "stop_success_congruent-go_congruent",

        # Task - baseline
        "task-baseline": (
            "1/6*(go_congruent+go_incongruent+stop_success_congruent+stop_success_incongruent+stop_failure_congruent+stop_failure_incongruent)"
            ),

        "response_time": "response_time"
    },
    "spatialTSWCuedTS": {
        #each trial type - baseline
        "cuedtstaycstay_spatialtstaycstay": "cuedtstaycstay_spatialtstaycstay",
        "cuedtstaycstay_spatialtstaycswitch": "cuedtstaycstay_spatialtstaycswitch",
        "cuedtstaycstay_spatialtswitchcswitch": "cuedtstaycstay_spatialtswitchcswitch",
        "cuedtstaycswitch_spatialtstaycstay": "cuedtstaycswitch_spatialtstaycstay",
        "cuedtstaycswitch_spatialtstaycswitch": "cuedtstaycswitch_spatialtstaycswitch",
        "cuedtstaycswitch_spatialtswitchcswitch": "cuedtstaycswitch_spatialtswitchcswitch",
        "cuedtswitchcswitch_spatialtstaycstay": "cuedtswitchcswitch_spatialtstaycstay",
        "cuedtswitchcswitch_spatialtstaycswitch": "cuedtswitchcswitch_spatialtstaycswitch",
        "cuedtswitchcswitch_spatialtswitchcswitch": "cuedtswitchcswitch_spatialtswitchcswitch",

        #cue switch cost for cuedTS 
        "spatialTSWCuedTS_cuedTS_cue_switch_cost": (
            "cuedtstaycswitch_spatialtstaycstay-cuedtstaycstay_spatialtstaycstay"
            ),

        #task switch cost for cuedTS
        "spatialTSWCuedTS_cuedTS_task_switch_cost": (
            "cuedtswitchcswitch_spatialtstaycstay-cuedtstaycswitch_spatialtstaycstay"
            ),

        #cue switch cost for spatialTS
        "spatialTSWCuedTS_spatialTS_cue_switch_cost": (
            "cuedtstaycstay_spatialtstaycswitch-cuedtstaycstay_spatialtstaycstay"
            ),

        #task switch cost for spatialTS
        "spatialTSWCuedTS_spatialTS_task_switch_cost": (
            "cuedtstaycstay_spatialtswitchcswitch-cuedtstaycstay_spatialtstaycswitch"
            ),

        #cue switch cost for cuedTS averaged across other trials
        "spatialTSWCuedTS_cuedTS_cue_switch_cost": (
            "1/3*(cuedtstaycswitch_spatialtstaycstay+cuedtstaycswitch_spatialtstaycswitch+cuedtstaycswitch_spatialtswitchcswitch)"
            "-1/3*(cuedtstaycstay_spatialtstaycstay+cuedtstaycstay_spatialtstaycswitch+cuedtstaycstay_spatialtswitchcswitch)"
            ),

        #task switch cost for cuedTS averaged across other trials
        "spatialTSWCuedTS_cuedTS_task_switch_cost": (
            "1/3*(cuedtswitchcswitch_spatialtstaycstay+cuedtswitchcswitch_spatialtstaycswitch+cuedtswitchcswitch_spatialtswitchcswitch)-"
            "1/3*(cuedtstaycswitch_spatialtstaycstay+cuedtstaycswitch_spatialtstaycswitch+cuedtstaycswitch_spatialtswitchcswitch)"
            ),

        #cue switch cost for spatialTS averaged across other trials
        "spatialTSWCuedTS_spatialTS_cue_switch_cost": (
            "1/3*(cuedtstaycstay_spatialtstaycswitch+cuedtstaycswitch_spatialtstaycswitch+cuedtswitchcswitch_spatialtstaycswitch)-"
            "1/3*(cuedtstaycstay_spatialtstaycstay+cuedtstaycswitch_spatialtstaycstay+cuedtswitchcswitch_spatialtstaycstay)"
            ),

        #task switch cost for spatialTS averaged across other trials
        "spatialTSWCuedTS_spatialTS_task_switch_cost": (
            "1/3*(cuedtstaycstay_spatialtswitchcswitch+cuedtstaycswitch_spatialtswitchcswitch+cuedtswitchcswitch_spatialtswitchcswitch)-"
            "1/3*(cuedtstaycstay_spatialtstaycswitch+cuedtstaycswitch_spatialtstaycswitch+cuedtswitchcswitch_spatialtstaycswitch)"
            ),

        #interaction for cue switch cost
        "spatialTSWCuedTS_cuedTS_cue_switch_cost_interaction": (
            "1/2*(cuedtstaycswitch_spatialtstaycswitch-cuedtstaycstay_spatialtstaycswitch)"
            "-1/2*(cuedtstaycswitch_spatialtstaycstay-cuedtstaycstay_spatialtstaycstay)"
            ),

        #interaction for task switch cost
        "spatialTSWCuedTS_task_switch_cost_interaction": (
            "1/2*(cuedtswitchcswitch_spatialtswitchcswitch-cuedtstaycswitch_spatialtswitchcswitch)-"
            "1/2*(cuedtswitchcswitch_spatialtstaycswitch-cuedtstaycswitch_spatialtstaycswitch)"
            ),

        #task - baseline
        "task-baseline": (
            "1/9*"
            "(cuedtstaycstay_spatialtstaycstay+cuedtstaycstay_spatialtstaycswitch+cuedtstaycstay_spatialtswitchcswitch"
            "+cuedtstaycswitch_spatialtstaycstay+cuedtstaycswitch_spatialtstaycswitch+cuedtstaycswitch_spatialtswitchcswitch+"
            "cuedtswitchcswitch_spatialtstaycstay+cuedtswitchcswitch_spatialtstaycswitch+cuedtswitchcswitch_spatialtswitchcswitch)"
            ),
        
        "response_time": "response_time"
    },
    "flankerWShapeMatching": {
        #each trial type - baseline
        "congruent_SSS": "congruent_SSS",
        "congruent_SDD": "congruent_SDD",
        "congruent_SNN": "congruent_SNN",
        "congruent_DSD": "congruent_DSD",
        "congruent_DNN": "congruent_DNN",
        "congruent_DDD": "congruent_DDD",
        "congruent_DDS": "congruent_DDS",
        "incongruent_SSS": "incongruent_SSS",
        "incongruent_SDD": "incongruent_SDD",
        "incongruent_SNN": "incongruent_SNN",
        "incongruent_DSD": "incongruent_DSD",
        "incongruent_DNN": "incongruent_DNN",
        "incongruent_DDD": "incongruent_DDD",
        "incongruent_DDS": "incongruent_DDS",

        #incongruent-congruent while shapeMatching is "off"
        "flankerWShapeMatching_shapeMatching_off_incongruent_minus_congruent": (
            "1/2*(incongruent_SNN+incongruent_DNN)-1/2*(congruent_SNN+congruent_DNN)"
            ),

        #main vars while flanker is "off"
        "flankerWShapeMatching_flanker_off_main_vars": (
            "1/3*(congruent_SDD+congruent_DDD+congruent_DDS)-1/2*(congruent_SNN+congruent_DNN)"
            ),

        #incongruent-congruent across all other trial types in shapeMatching
        "flankerWShapeMatching_shapeMatching_incongruent_minus_congruent": (
            "1/7*(incongruent_SSS+incongruent_SDD+incongruent_SNN+incongruent_DSD+incongruent_DNN+incongruent_DDD+incongruent_DDS)"
            "-1/7*(congruent_SSS+congruent_SDD+congruent_SNN+congruent_DSD+congruent_DNN+congruent_DDD+congruent_DDS)"
            ),

        #main vars across all other flanker trial types
        "flankerWShapeMatching_flanker_main_vars": (
            "1/6*(congruent_SDD+congruent_DDD+congruent_DDS+incongruent_SDD+incongruent_DDD+incongruent_DDS)-"
            "1/4*(congruent_SNN+congruent_DNN+incongruent_SNN+incongruent_DNN)"
            ),

        #interaction for each trial type
        "flankerWShapeMatching_interaction": (
            "(1/3*(incongruent_SDD+incongruent_DDD+incongruent_DDS)-1/3*(congruent_SDD+congruent_DDD+congruent_DDS))-"
            "(1/2*(incongruent_SNN+incongruent_DNN)-1/2*(congruent_SNN+congruent_DNN))"
            ),

        #task - baseline
        "task-baseline": (
            "1/14*(congruent_SSS+congruent_SDD+congruent_SNN+congruent_DSD+congruent_DNN+"
            "congruent_DDD+congruent_DDS+incongruent_SSS+incongruent_SDD+incongruent_SNN+"
            "incongruent_DSD+incongruent_DNN+incongruent_DDD+incongruent_DDS)"
            ),

        "response_time": "response_time"
    },
    "cuedTSWFlanker": {
        #each trial type - baseline
        "cstay_tstay_congruent": "cstay_tstay_congruent",
        "cstay_tstay_incongruent": "cstay_tstay_incongruent",
        "cswitch_tswitch_congruent": "cswitch_tswitch_congruent",
        "cswitch_tswitch_incongruent": "cswitch_tswitch_incongruent",
        "cswitch_tstay_congruent": "cswitch_tstay_congruent",
        "cswitch_tstay_incongruent": "cswitch_tstay_incongruent",

        #incongruent-congruent while cuedTS is "off"
        "cstay_tstay_incongruent-cstay_tstay_congruent": "cstay_tstay_incongruent-cstay_tstay_congruent",

        #cue switch cost while flanker is "off"
        "cswitch_tstay_congruent-cstay_tstay_congruent": "cswitch_tstay_congruent-cstay_tstay_congruent",

        #task switch cost while flanker is "off"
        "cswitch_tswitch_congruent-cswitch_tstay_congruent": "cswitch_tswitch_congruent-cswitch_tstay_congruent",

        #incongruent-congruent across all cuedTS trial types
        "cuedTSWFlanker_cuedTS_incongruent_minus_congruent": (
            "1/3*(cstay_tstay_incongruent+cswitch_tswitch_incongruent+cswitch_tstay_incongruent)-"
            "1/3*(cstay_tstay_congruent+cswitch_tswitch_congruent+cswitch_tstay_congruent)"
            ),

        #cue switch cost across all flanker trial types
        "cuedTSWFlanker_across_flanker_cue_switch_cost": (
            "1/2*(cswitch_tstay_congruent+cswitch_tstay_incongruent)-1/2*(cstay_tstay_congruent+cstay_tstay_incongruent)"
            ),

        #task switch cost across all flanker trial types
        "cuedTSWFlanker_across_flanker_task_switch_cost": (
            "1/2*(cswitch_tswitch_congruent+cswitch_tswitch_incongruent)-1/2*(cswitch_tstay_congruent+cswitch_tstay_incongruent)"
            ),

        #interaction for cue switch cost
        "cuedTSWFlanker_cue_switch_cost_interaction": (
            "1/2*(cswitch_tstay_incongruent-cstay_tstay_incongruent)-1/2*(cswitch_tstay_congruent-cstay_tstay_congruent)"
            ),

        #interaction for task switch cost
        "cuedTSWFlanker_task_switch_cost_interaction": (
            "1/2*(cswitch_tswitch_incongruent-cswitch_tstay_incongruent)-1/2*(cswitch_tswitch_congruent-cswitch_tstay_congruent)"
            ),

        #task - baseline
        "task-baseline": (
            "1/6*(cstay_tstay_congruent+cstay_tstay_incongruent+cswitch_tswitch_congruent+"
            "cswitch_tswitch_incongruent+cswitch_tstay_congruent+cswitch_tstay_incongruent)"
            ),

        "response_time": "response_time"
    },
    "spatialTSWShapeMatching": {
        #each trial type - baseline
        "tstay_cstay_SSS": "tstay_cstay_SSS",
        "tstay_cstay_SDD": "tstay_cstay_SDD",
        "tstay_cstay_SNN": "tstay_cstay_SNN",
        "tstay_cstay_DSD": "tstay_cstay_DSD",
        "tstay_cstay_DNN": "tstay_cstay_DNN",
        "tstay_cstay_DDD": "tstay_cstay_DDD",
        "tstay_cstay_DDS": "tstay_cstay_DDS",
        "tstay_cswitch_SSS": "tstay_cswitch_SSS",
        "tstay_cswitch_SDD": "tstay_cswitch_SDD",
        "tstay_cswitch_SNN": "tstay_cswitch_SNN",
        "tstay_cswitch_DSD": "tstay_cswitch_DSD",
        "tstay_cswitch_DNN": "tstay_cswitch_DNN",
        "tstay_cswitch_DDD": "tstay_cswitch_DDD",
        "tstay_cswitch_DDS": "tstay_cswitch_DDS",
        "tswitch_cswitch_SSS": "tswitch_cswitch_SSS",
        "tswitch_cswitch_SDD": "tswitch_cswitch_SDD",
        "tswitch_cswitch_SNN": "tswitch_cswitch_SNN",
        "tswitch_cswitch_DSD": "tswitch_cswitch_DSD",
        "tswitch_cswitch_DNN": "tswitch_cswitch_DNN",
        "tswitch_cswitch_DDD": "tswitch_cswitch_DDD",
        "tswitch_cswitch_DDS": "tswitch_cswitch_DDS",

        #spatialTS cue switch cost while shapeMatching is "off"
        "spatialTSWShapeMatching_shapeMatching_off_cue_switch_cost": (
            "1/2*(tstay_cswitch_SNN+tstay_cswitch_DNN)-1/2*(tstay_cstay_SNN+tstay_cstay_DNN)"
            ),

        #spatialTS task switch cost while shapeMatching is "off"
        "spatialTSWShapeMatching_shapeMatching_off_task_switch_cost": (
            "1/2*(tswitch_cswitch_SNN+tswitch_cswitch_DNN)-1/2*(tstay_cswitch_SNN+tstay_cswitch_DNN)"
            ),

        #main vars while spatialTS is "off"
        "spatialTSWShapeMatching_spatialTS_off_main_vars": (
            "1/3*(tstay_cstay_SDD+tstay_cstay_DDD+tstay_cstay_DDS)-1/2*(tstay_cstay_SNN+tstay_cstay_DNN)"
            ),

        #spatialTS cue switch cost across all other shapeMatching trial types
        "spatialTSWShapeMatching_shapeMatching_cue_switch_cost": (
            "1/7*(tstay_cswitch_SSS+tstay_cswitch_SDD+tstay_cswitch_SNN+tstay_cswitch_DSD+tstay_cswitch_DNN+tstay_cswitch_DDD+tstay_cswitch_DDS)-"
            "1/7*(tstay_cstay_SSS+tstay_cstay_SDD+tstay_cstay_SNN+tstay_cstay_DSD+tstay_cstay_DNN+tstay_cstay_DDD+tstay_cstay_DDS)"
            ),

        #spatialTS task switch cost across all other shapeMatching trial types
        "spatialTSWShapeMatching_shapeMatching_task_switch_cost": (
            "1/7*(tswitch_cswitch_SSS+tswitch_cswitch_SDD+tswitch_cswitch_SNN+tswitch_cswitch_DSD+"
            "tswitch_cswitch_DNN+tswitch_cswitch_DDD+tswitch_cswitch_DDS)-"
            "1/7*(tstay_cswitch_SSS+tstay_cswitch_SDD+tstay_cswitch_SNN+tstay_cswitch_DSD+"
            "tstay_cswitch_DNN+tstay_cswitch_DDD+tstay_cswitch_DDS)"
            ),

        #main vars across all other spatialTS trial types
        "spatialTSWShapeMatching_spatialTS_main_vars": (
            "1/9*(tstay_cstay_SDD+tstay_cstay_DDD+tstay_cstay_DDS+tstay_cswitch_SDD+"
            "tstay_cswitch_DDD+tstay_cswitch_DDS+tswitch_cswitch_SDD+tswitch_cswitch_DDD+tswitch_cswitch_DDS)-"
            "1/6*(tstay_cstay_SNN+tstay_cstay_DNN+tstay_cswitch_SNN+tstay_cswitch_DNN+tswitch_cswitch_SNN+tswitch_cswitch_DNN)"
            ),

        #interaction for cue switch cost
        "spatialTSWShapeMatching_shapeMatching_cue_switch_cost_interaction": (
            "1/3*(tstay_cswitch_SDD+tstay_cswitch_DDD+tstay_cswitch_DDS)-"
            "1/3*(tstay_cstay_SDD+tstay_cstay_DDD+tstay_cstay_DDS)-"
            "1/2*(tstay_cswitch_SNN+tstay_cswitch_DNN)"
            "+1/2*(tstay_cstay_SNN+tstay_cstay_DNN)"
            ),

        #interaction for task switch cost
        "spatialTSWShapeMatching_shapeMatching_task_switch_cost_interaction": (
            "1/3*(tswitch_cswitch_SDD+tswitch_cswitch_DDD+tswitch_cswitch_DDS)-"
            "1/3*(tstay_cswitch_SDD+tstay_cswitch_DDD+tstay_cswitch_DDS)-"
            "1/2*(tswitch_cswitch_SNN+tswitch_cswitch_DNN)+"
            "1/2*(tstay_cswitch_SNN+tstay_cswitch_DNN)"
            ),

        #task - baseline
        "task-baseline": (
            "1/21*(tstay_cstay_SSS+tstay_cstay_SDD+tstay_cstay_SNN+tstay_cstay_DSD+tstay_cstay_DNN+tstay_cstay_DDD+tstay_cstay_DDS+"
            "tstay_cswitch_SSS+tstay_cswitch_SDD+tstay_cswitch_SNN+tstay_cswitch_DSD+tstay_cswitch_DNN+tstay_cswitch_DDD+tstay_cswitch_DDS+"
            "tswitch_cswitch_SSS+tswitch_cswitch_SDD+tswitch_cswitch_SNN+tswitch_cswitch_DSD+tswitch_cswitch_DNN+"
            "tswitch_cswitch_DDD+tswitch_cswitch_DDS)"
            ),

        "response_time": "response_time"
    },
    "nBackWShapeMatching": {
        #each trial type - baseline
        "mismatch_tstay_cstay_1back": "mismatch_tstay_cstay_1back",
        "mismatch_tstay_cswitch_1back": "mismatch_tstay_cswitch_1back",
        "mismatch_tswitch_cswitch_1back": "mismatch_tswitch_cswitch_1back",
        "match_tstay_cstay_1back": "match_tstay_cstay_1back",
        "match_tstay_cswitch_1back": "match_tstay_cswitch_1back",
        "match_tswitch_cswitch_1back": "match_tswitch_cswitch_1back",
        "mismatch_tstay_cstay_2back": "mismatch_tstay_cstay_2back",
        "mismatch_tstay_cswitch_2back": "mismatch_tstay_cswitch_2back",
        "mismatch_tswitch_cswitch_2back": "mismatch_tswitch_cswitch_2back",
        "match_tstay_cstay_2back": "match_tstay_cstay_2back",
        "match_tstay_cswitch_2back": "match_tstay_cswitch_2back",
        "match_tswitch_cswitch_2back": "match_tswitch_cswitch_2back",

        #2back-1back when spatialTS is "off"
        "nBackWSpatialTS_spatialTS_off_2back_minus_1back":
        "1/2*(match_tstay_cstay_2back+mismatch_tstay_cstay_2back)-1/2*(match_tstay_cstay_1back+mismatch_tstay_cstay_1back)",

        #cue switch cost when nBack is "off"
        "nBackWSpatialTS_nBack_off_cue_switch_cost":
        "1/2*(match_tstay_cswitch_1back+mismatch_tstay_cswitch_1back)-1/2*(match_tstay_cstay_1back+mismatch_tstay_cstay_1back)",

        #task switch cost when nBack is "off"
        "nBackWSpatialTS_nBack_off_task_switch_cost":
        "1/2*(match_tswitch_cswitch_1back+mismatch_tswitch_cswitch_1back)-1/2*(match_tstay_cswitch_1back+mismatch_tstay_cswitch_1back)",

        #2back-1back across all spatialTS trial types
        "nBackWSpatialTS_spatialTS_2back_minus_1back": (
            "1/6*(match_tstay_cstay_2back+match_tstay_cswitch_2back+match_tswitch_cswitch_2back+"
            "mismatch_tstay_cstay_2back+mismatch_tstay_cswitch_2back+mismatch_tswitch_cswitch_2back)-"
            "1/6*(match_tstay_cstay_1back+match_tstay_cswitch_1back+match_tswitch_cswitch_1back+"
            "mismatch_tstay_cstay_1back+mismatch_tstay_cswitch_1back+mismatch_tswitch_cswitch_1back)"
            ),

        #cue switch cost across all other nBack trial types
        "nBackWSpatialTS_nBack_cue_switch_cost": (
            "1/4*(match_tstay_cswitch_1back+match_tstay_cswitch_2back+mismatch_tstay_cswitch_1back+mismatch_tstay_cswitch_2back)-"
            "1/4*(match_tstay_cstay_1back+match_tstay_cstay_2back+mismatch_tstay_cstay_1back+mismatch_tstay_cstay_2back)"
            ),

        #task switch cost across all other nBack trial types
        "nBackWSpatialTS_nBack_task_switch_cost": (
            "1/4*(match_tswitch_cswitch_1back+match_tswitch_cswitch_2back+mismatch_tswitch_cswitch_1back+mismatch_tswitch_cswitch_2back)-"
            "1/4*(match_tstay_cswitch_1back+match_tstay_cswitch_2back+mismatch_tstay_cswitch_1back+mismatch_tstay_cswitch_2back)"
            ),

        #cue switch cost interaction
        "nBackWSpatialTS_nBack_cue_switch_cost_interaction": (
            "(1/2*(match_tstay_cswitch_2back+mismatch_tstay_cswitch_2back)-"
            "1/2*(match_tstay_cstay_2back+mismatch_tstay_cstay_2back))-"
            "(1/2*(match_tstay_cswitch_1back+mismatch_tstay_cswitch_1back)-"
            "1/2*(match_tstay_cstay_1back+mismatch_tstay_cstay_1back))"
            ),

        #task switch cost interaction
        "nBackWSpatialTS_nBack_task_switch_cost_interaction": (
            "(1/2*(match_tswitch_cswitch_2back+mismatch_tswitch_cswitch_2back)-"
            "1/2*(match_tstay_cswitch_2back+mismatch_tstay_cswitch_2back))-"
            "(1/2*(match_tswitch_cswitch_1back+mismatch_tswitch_cswitch_1back)-"
            "1/2*(match_tstay_cswitch_1back+mismatch_tstay_cswitch_1back))"
            ),

        #task - baseline
        "task-baseline": (
            "1/12*(mismatch_tstay_cstay_1back+mismatch_tstay_cswitch_1back+"
            "mismatch_tswitch_cswitch_1back+match_tstay_cstay_1back+match_tstay_cswitch_1back+"
            "match_tswitch_cswitch_1back+mismatch_tstay_cstay_2back+mismatch_tstay_cswitch_2back+"
            "mismatch_tswitch_cswitch_2back+match_tstay_cstay_2back+match_tstay_cswitch_2back+match_tswitch_cswitch_2back)"
            ),
            
        "response_time": "response_time"
    },
    "nBackWSpatialTS": {
        #each trial type - baseline
        "mismatch_tstay_cstay_1back": "mismatch_tstay_cstay_1back",
        "mismatch_tstay_cswitch_1back": "mismatch_tstay_cswitch_1back",
        "mismatch_tswitch_cswitch_1back": "mismatch_tswitch_cswitch_1back",
        "match_tstay_cstay_1back": "match_tstay_cstay_1back",
        "match_tstay_cswitch_1back": "match_tstay_cswitch_1back",
        "match_tswitch_cswitch_1back": "match_tswitch_cswitch_1back",
        "mismatch_tstay_cstay_2back": "mismatch_tstay_cstay_2back",
        "mismatch_tstay_cswitch_2back": "mismatch_tstay_cswitch_2back",
        "mismatch_tswitch_cswitch_2back": "mismatch_tswitch_cswitch_2back",
        "match_tstay_cstay_2back": "match_tstay_cstay_2back",
        "match_tstay_cswitch_2back": "match_tstay_cswitch_2back",
        "match_tswitch_cswitch_2back": "match_tswitch_cswitch_2back",

        #2back-1back when spatialTS is "off"
        "nBackWSpatialTS_spatialTS_off_2back_minus_1back": (
            "1/2*(match_tstay_cstay_2back+mismatch_tstay_cstay_2back)-1/2*(match_tstay_cstay_1back+mismatch_tstay_cstay_1back)"
            ),

        #cue switch cost when nBack is "off"
        "nBackWSpatialTS_nBack_off_cue_switch_cost": (
            "1/2*(match_tstay_cswitch_1back+mismatch_tstay_cswitch_1back)-1/2*(match_tstay_cstay_1back+mismatch_tstay_cstay_1back)"
            ),

        #task switch cost when nBack is "off"
        "nBackWSpatialTS_nBack_off_task_switch_cost": (
            "1/2*(match_tswitch_cswitch_1back+mismatch_tswitch_cswitch_1back)-1/2*(match_tstay_cswitch_1back+mismatch_tstay_cswitch_1back)"
            ),

        #2back-1back across all spatialTS trial types
        "nBackWSpatialTS_spatialTS_2back_minus_1back": (
            "1/6*(match_tstay_cstay_2back+match_tstay_cswitch_2back+match_tswitch_cswitch_2back+"
            "mismatch_tstay_cstay_2back+mismatch_tstay_cswitch_2back+mismatch_tswitch_cswitch_2back)-"
            "1/6*(match_tstay_cstay_1back+match_tstay_cswitch_1back+match_tswitch_cswitch_1back+"
            "mismatch_tstay_cstay_1back+mismatch_tstay_cswitch_1back+mismatch_tswitch_cswitch_1back)"
            ),

        #cue switch cost across all other nBack trial types
        "nBackWSpatialTS_nBack_cue_switch_cost": (
            "1/4*(match_tstay_cswitch_1back+match_tstay_cswitch_2back+mismatch_tstay_cswitch_1back+mismatch_tstay_cswitch_2back)-"
            "1/4*(match_tstay_cstay_1back+match_tstay_cstay_2back+mismatch_tstay_cstay_1back+mismatch_tstay_cstay_2back)"
            ),

        #task switch cost across all other nBack trial types
        "nBackWSpatialTS_nBack_task_switch_cost": (
            "1/4*(match_tswitch_cswitch_1back+match_tswitch_cswitch_2back+mismatch_tswitch_cswitch_1back+mismatch_tswitch_cswitch_2back)-"
            "1/4*(match_tstay_cswitch_1back+match_tstay_cswitch_2back+mismatch_tstay_cswitch_1back+mismatch_tstay_cswitch_2back)"
            ),

        #cue switch cost interaction
        "nBackWSpatialTS_cue_switch_cost_interaction": (
            "(1/2*(match_tstay_cswitch_2back+mismatch_tstay_cswitch_2back)-"
            "1/2*(match_tstay_cstay_2back+mismatch_tstay_cstay_2back))-"
            "(1/2*(match_tstay_cswitch_1back+mismatch_tstay_cswitch_1back)-"
            "1/2*(match_tstay_cstay_1back+mismatch_tstay_cstay_1back))"
            ),

        #task switch cost interaction
        "nBackWSpatialTS_nBack_task_switch_cost_interaction": (
            "(1/2*(match_tswitch_cswitch_2back+mismatch_tswitch_cswitch_2back)-"
            "1/2*(match_tstay_cswitch_2back+mismatch_tstay_cswitch_2back))-"
            "(1/2*(match_tswitch_cswitch_1back+mismatch_tswitch_cswitch_1back)-"
            "1/2*(match_tstay_cswitch_1back+mismatch_tstay_cswitch_1back))"
            ),

        #task - baseline
        "task-baseline": (
            "1/12*(mismatch_tstay_cstay_1back+mismatch_tstay_cswitch_1back+mismatch_tswitch_cswitch_1back+"
            "match_tstay_cstay_1back+match_tstay_cswitch_1back+match_tswitch_cswitch_1back+mismatch_tstay_cstay_2back+"
            "mismatch_tstay_cswitch_2back+mismatch_tswitch_cswitch_2back+match_tstay_cstay_2back+match_tstay_cswitch_2back+"
            "match_tswitch_cswitch_2back)"
            ),

        "response_time": "response_time"
    },
    "shapeMatchingWCuedTS": {
        "SSS_tswitch_cswitch": "SSS_tswitch_cswitch",
        "SSS_tstay_cswitch": "SSS_tstay_cswitch",
        "SSS_tstay_cstay": "SSS_tstay_cstay",
        "SDD_tswitch_cswitch": "SDD_tswitch_cswitch",
        "SDD_tstay_cswitch": "SDD_tstay_cswitch",
        "SDD_tstay_cstay": "SDD_tstay_cstay",
        "SNN_tswitch_cswitch": "SNN_tswitch_cswitch",
        "SNN_tstay_cswitch": "SNN_tstay_cswitch",
        "SNN_tstay_cstay": "SNN_tstay_cstay",
        "DSD_tswitch_cswitch": "DSD_tswitch_cswitch",
        "DSD_tstay_cswitch": "DSD_tstay_cswitch",
        "DSD_tstay_cstay": "DSD_tstay_cstay",
        "DDD_tswitch_cswitch": "DDD_tswitch_cswitch",
        "DDD_tstay_cswitch": "DDD_tstay_cswitch",
        "DDD_tstay_cstay": "DDD_tstay_cstay",
        "DDS_tswitch_cswitch": "DDS_tswitch_cswitch",
        "DDS_tstay_cswitch": "DDS_tstay_cswitch",
        "DDS_tstay_cstay": "DDS_tstay_cstay",
        "DNN_tswitch_cswitch": "DNN_tswitch_cswitch",
        "DNN_tstay_cswitch": "DNN_tstay_cswitch",
        "DNN_tstay_cstay": "DNN_tstay_cstay",
         #cuedTS cue switch cost while shapeMatching is "off"
        "shapeMatchingWCuedTS_shapeMatching_off_cue_switch_cost": (
            "1/2*(SNN_tstay_cswitch+DNN_tstay_cswitch)-1/2*(SNN_tstay_cstay+DNN_tstay_cstay)"
            ),

        #cuedTS task switch cost while shapeMatching is "off"
        "shapeMatchingWCuedTS_shapeMatching_off_task_switch_cost": (
            "1/2*(SNN_tswitch_cswitch+DNN_tswitch_cswitch)-1/2*(SNN_tstay_cswitch+DNN_tstay_cswitch)"
            ),

        #main vars while cuedTS is "off"
        "shapeMatchingWCuedTS_cuedTS_off_main_vars": (
            "1/3*(SDD_tstay_cstay+DDD_tstay_cstay+DDS_tstay_cstay)-1/2*(SNN_tstay_cstay+DNN_tstay_cstay)"
            ),

        #cuedTS cue switch cost across all other shapeMatching trial types
        "shapeMatchingWCuedTS_shapeMatching_cue_switch_cost": (
            "1/7*(SSS_tstay_cswitch+SDD_tstay_cswitch+SNN_tstay_cswitch+DSD_tstay_cswitch+DNN_tstay_cswitch+DDD_tstay_cswitch+DDS_tstay_cswitch)-"
            "1/7*(SSS_tstay_cstay+SDD_tstay_cstay+SNN_tstay_cstay+DSD_tstay_cstay+DNN_tstay_cstay+DDD_tstay_cstay+DDS_tstay_cstay)"
            ),

        #cuedTS task switch cost across all other shapeMatching trial types
        "shapeMatchingWCuedTS_shapeMatching_task_switch_cost": (
            "1/7*(SSS_tswitch_cswitch+SDD_tswitch_cswitch+SNN_tswitch_cswitch+DSD_tswitch_cswitch+"
            "DNN_tswitch_cswitch+DDD_tswitch_cswitch+DDS_tswitch_cswitch)-"
            "1/7*(SSS_tstay_cswitch+SDD_tstay_cswitch+SNN_tstay_cswitch+DSD_tstay_cswitch+"
            "DNN_tstay_cswitch+DDD_tstay_cswitch+DDS_tstay_cswitch)"
            ),

        #main vars across all other cuedTS trial types
        "shapeMatchingWCuedTS_cuedTS_main_vars": (
            "1/9*(SDD_tstay_cstay+DDD_tstay_cstay+DDS_tstay_cstay+SDD_tstay_cswitch+"
            "DDD_tstay_cswitch+DDS_tstay_cswitch+SDD_tswitch_cswitch+DDD_tswitch_cswitch+DDS_tswitch_cswitch)-"
            "1/6*(SNN_tstay_cstay+DNN_tstay_cstay+SNN_tstay_cswitch+DNN_tstay_cswitch+SNN_tswitch_cswitch+DNN_tswitch_cswitch)"
            ),

        #interaction for cue switch cost
        "shapeMatchingWCuedTS_cue_switch_cost_interaction": (
            "1/3*(SDD_tstay_cswitch+DDD_tstay_cswitch+DDS_tstay_cswitch)-"
            "1/3*(SDD_tstay_cstay+DDD_tstay_cstay+DDS_tstay_cstay)-"
            "1/2*(SNN_tstay_cswitch+DNN_tstay_cswitch)"
            "+1/2*(SNN_tstay_cstay+DNN_tstay_cstay)"
            ),

        #interaction for task switch cost
        "shapeMatchingWCuedTS_task_switch_cost_interaction": (
            "1/3*(SDD_tswitch_cswitch+DDD_tswitch_cswitch+DDS_tswitch_cswitch)-"
            "1/3*(SDD_tstay_cswitch+DDD_tstay_cswitch+DDS_tstay_cswitch)-"
            "1/2*(SNN_tswitch_cswitch+DNN_tswitch_cswitch)+"
            "1/2*(SNN_tstay_cswitch+DNN_tstay_cswitch)"
            ),

        #task - baseline
        "task-baseline": (
            "1/21*(SSS_tstay_cstay+SDD_tstay_cstay+SNN_tstay_cstay+DSD_tstay_cstay+DNN_tstay_cstay+DDD_tstay_cstay+DDS_tstay_cstay+"
            "SSS_tstay_cswitch+SDD_tstay_cswitch+SNN_tstay_cswitch+DSD_tstay_cswitch+DNN_tstay_cswitch+DDD_tstay_cswitch+DDS_tstay_cswitch+"
            "SSS_tswitch_cswitch+SDD_tswitch_cswitch+SNN_tswitch_cswitch+DSD_tswitch_cswitch+DNN_tswitch_cswitch+DDD_tswitch_cswitch+DDS_tswitch_cswitch)"
            ),

        "response_time": "response_time"
    }
}