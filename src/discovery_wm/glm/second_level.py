import logging
import re
from pathlib import Path

import matplotlib.pyplot as plt
import nibabel as nb
import numpy as np
import pandas as pd
from nilearn import plotting
from nilearn.glm import threshold_stats_img
from nilearn.glm.second_level import SecondLevelModel
from templateflow import api as tf

from discovery_wm.utils import extract_contrast_name, get_parser


def get_contrast_paths_by_subject_and_contrast_name(base_dir: str, task_name: str = None, contrast_name: str = None) -> dict:
    """
    Takes in the directory of the first level contrast maps in MNI space,
    and returns a dictionary of the contrast maps by each subject for each contrast.
    If task_name is provided, only returns maps for that task.
    If contrast_name is provided, only returns maps for that contrast.
    """
    contrast_maps = {}
    for subj in base_dir.glob('sub-s*'):
        contrast_maps[subj.name] = {}
        
        # Build glob pattern based on provided args
        glob_pattern = '*/indiv_contrasts/*effect-size.nii.gz'
        if task_name is not None:
            glob_pattern = f'{task_name}/indiv_contrasts/*effect-size.nii.gz'
        if contrast_name is not None:
            glob_pattern = f'*/indiv_contrasts/*contrast-{contrast_name}_*effect-size.nii.gz'
            
        for task_contrast in subj.glob(glob_pattern):
            cname = extract_contrast_name(task_contrast)
            current_task_name = task_contrast.parent.parent.name
            key = f'{current_task_name}_{cname}'
            if key not in contrast_maps[subj.name]:
                contrast_maps[subj.name][key] = []
            contrast_maps[subj.name][key].append(task_contrast)
    return contrast_maps

def sort_by_session_order(contrast_maps: dict) -> dict:
    """
    Sorts the contrast maps by session order.
    """
    for subj in contrast_maps:
        for cname in contrast_maps[subj]:
            # Extract session number from filename to use as sorting key
            # This ensures that the contrast maps are sorted in the correct
            # order: from first session to last session.
            contrast_maps[subj][cname] = sorted(
                contrast_maps[subj][cname],
                key=lambda x: int(re.search(r'ses-(\d+)', str(x)).group(1))
            )

    return contrast_maps

def fixed_effects_analysis(contrast_maps: dict) -> dict:
    """
    Performs a fixed effects analysis by combining contrast maps across encounters
    for each subject. This is done by averaging the effect size maps.
    """
    fixed_effects_maps = {}
    for subj in contrast_maps:
        fixed_effects_maps[subj] = {}
        for cname in contrast_maps[subj]:
            # Load all maps for this subject and contrast
            maps = [nb.load(cmap) for cmap in contrast_maps[subj][cname]]
            
            # Get the data arrays
            data_arrays = [map.get_fdata() for map in maps]
            
            # Average the data arrays
            avg_data = np.mean(data_arrays, axis=0)
            
            # Create a new NIfTI image with the averaged data
            avg_map = nb.Nifti1Image(avg_data, maps[0].affine, maps[0].header)
            
            fixed_effects_maps[subj][cname] = avg_map
            
    return fixed_effects_maps

def plot_stat_map(
    stat_map: nb.Nifti1Image,
    threshold: float,
    cname: str,
    outdir: Path,
    template: nb.Nifti1Image,
    title: str = None,
    cut_coords: tuple = (-10, 0, 10, 20, 30, 40, 50, 60, 70)
):
    """
    Plots the statistical map.
    """
    fig = plt.figure(figsize=(12, 3))
    plotting.plot_stat_map(
        stat_map,
        threshold=threshold,
        display_mode='z',
        cut_coords=cut_coords,
        title=title,
        figure=fig,
        draw_cross=False,
        annotate=True,
        bg_img=template,
        cmap='coolwarm',
    )
    outpath = outdir / cname / f'{cname}_threshold-{threshold:.2f}.png'
    outpath.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(outpath)
    logging.info(f"Saved plot to {outpath}")
    plt.close()

def main():
    logging.basicConfig(level=logging.INFO)

    parser = get_parser()
    args = parser.parse_args()

    # == PATHS ==
    outdir = Path('output_lev2_mni')
    oak = Path('/oak/stanford/groups/russpold/data/')
    bids_dir = oak / 'network_grant' / 'validation_BIDS'
    output_lev1_mni = bids_dir / 'derivatives' / 'output_lev1_mni'

    # == GET CONTRAST MAPS ==
    contrast_maps = get_contrast_paths_by_subject_and_contrast_name(output_lev1_mni, args.task_name, args.contrast_name)
    contrast_maps_sorted = sort_by_session_order(contrast_maps)
    
    # Perform fixed effects analysis to collapse across encounters
    fixed_effects_maps = fixed_effects_analysis(contrast_maps_sorted)

    # == THRESHOLDS ==
    liberal_threshold = 1.0
    no_threshold = 0.0
    alpha = 0.05

    # == MNI TEMPLATE FOR BACKGROUND IMG ==
    template= tf.get("MNI152NLin2009cAsym", resolution=2, suffix="T1w", desc=None) 

    logging.info("Starting execution of second level GLMs")
    
    # Get all unique contrasts across all subjects
    all_contrasts = set()
    for subj in fixed_effects_maps:
        all_contrasts.update(fixed_effects_maps[subj].keys())
    
    # == LOOP THROUGH ALL CONTRASTS AND RUN SECOND LEVEL MODEL ==
    for cname in sorted(all_contrasts):
        logging.info(f"Running GLM for contrast: {cname}")
        
        # Get all subject maps for this contrast, only including subjects that have this contrast
        cmaps = []
        subj_ids = []
        for subj_id, subj_maps in fixed_effects_maps.items():
            if cname in subj_maps:
                cmaps.append(subj_maps[cname])
                subj_ids.append(np.float64(float(subj_id.replace('sub-s', ''))))
            
        logging.info(f"Analyzing contrast {cname} with {len(cmaps)} subjects")
        
        # Create design matrix
        desmat = pd.DataFrame({
            'intercept': 1,
            'subject': subj_ids
        })

        # == FIT SECOND LEVEL MODEL ==
        second_level_model = SecondLevelModel(smoothing_fwhm=8.0)
        second_level_model.fit(cmaps, design_matrix=desmat)

        # == COMPUTE CONTRAST ==
        z_map = second_level_model.compute_contrast(
            second_level_contrast='intercept',
            output_type='z_score'
        )

        # == THRESHOLD MAP ==
        thresholded_map, threshold = threshold_stats_img(
            z_map, alpha=alpha, height_control='fpr'
        )

        # == PLOT MAPS (THRESHOLDED AND UNTHRESHOLDED) ==
        plot_stat_map(thresholded_map, threshold, cname, outdir, template, 
                     title=f'{cname} (FPR-corrected p < {alpha})')
        plot_stat_map(z_map, liberal_threshold, cname, outdir, template, 
                     title=f'{cname} (z > {liberal_threshold:.2f})')
        plot_stat_map(z_map, no_threshold, cname, outdir, template, 
                     title=f'{cname} (z > {no_threshold:.2f})')

    return

if __name__ == "__main__":
    main()
