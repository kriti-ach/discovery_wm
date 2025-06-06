import os
from glob import glob
from pathlib import Path

import matplotlib.pyplot as plt
import nibabel as nf
import numpy as np
import seaborn as sns
from nilearn import masking
from nilearn.glm.contrasts import compute_fixed_effects
from nilearn.masking import apply_mask
from nilearn.plotting import plot_img
from discovery_wm.utils import get_parser, get_subj_id 

def get_unique_contrasts(indiv_contrasts_dir: Path, subj_id: str, task_name: str) -> list[str]:
    """Get unique contrasts from effect size files"""
    all_contrasts = glob(f"{indiv_contrasts_dir}/*{subj_id}*{task_name}*contrast-*_rtmodel*effect-size*")
    contrasts = [
        contrast.split('_contrast-')[1].split('_rtmodel')[0]
        for contrast in all_contrasts
    ]
    return np.unique(contrasts)

def extract_session_from_filename(filename: str) -> str:
    """Extract session from filename"""
    return (
        filename.split('_ses-')[1].split('_')[0] if '_ses-' in filename else 'unknown'
    )

def main():
    # get unique contrast names
    parser = get_parser()
    task_name = parser.parse_args().task_name
    subj_id = get_subj_id(parser)

    # Paths
    # - Input path 
    subj_lev1_dir = Path(f"./output_lev1_mni/{subj_id}/{task_name}")
    # - Contains effect size files for subject
    indiv_contrasts_dir = Path(f"{subj_lev1_dir}/indiv_contrasts")
    # - Output path
    outdir = Path("./output_lev1_mni/figures", subj_id, task_name, "brain_maps")
    # - Path to store fixed effects brain map results
    fixed_effects_dir = Path(outdir, "fixed_effects")
    # - Path to store individual contrasts brain map results
    individual_contrasts_dir = Path(outdir, "individual_contrasts")

    fixed_effects_dir.mkdir(parents=True, exist_ok=True)
    individual_contrasts_dir.mkdir(parents=True, exist_ok=True)

    # get unique contrast names
    unique_contrasts = get_unique_contrasts(indiv_contrasts_dir, subj_id, task_name)

    # carefully concatenate contrasts and variance images to keep order consistent
    all_eff_sizes, all_eff_vars, all_con_names = [], [], []
    fixed_fx_contrasts, fixed_fx_variances, fixed_fx_stats, fixed_fx_contrast_names = [], [], [], []

    for contrast in unique_contrasts:
        contrast_effect_size = glob(
            f'{indiv_contrasts_dir}/*{subj_id}*{task_name}*contrast-{contrast}_rtmodel*effect-size*'
        )
        contrast_effect_var = [
            eff_size.replace('effect-size', 'variance')
            for eff_size in contrast_effect_size
        ]

        all_eff_sizes.extend(contrast_effect_size)
        all_eff_vars.extend(contrast_effect_var)
        all_con_names.extend([contrast] * len(contrast_effect_size))
        # run fixed effects analysis
        fixed_fx_contrast, fixed_fx_variance, fixed_fx_stat = compute_fixed_effects(
            contrast_effect_size,
            contrast_effect_var,
        )
        fixed_fx_contrasts.append(fixed_fx_contrast)
        fixed_fx_variances.append(fixed_fx_variance)
        fixed_fx_stats.append(fixed_fx_stat)
        fixed_fx_contrast_names.append(contrast)

        assert len(contrast_effect_size) > 0, "No contrast effect size found"

        # Plot each individual contrast file
        for i, effect_file in enumerate(contrast_effect_size):
            img = nf.load(effect_file)
            # Get run number or some identifier from filename
            session_match = extract_session_from_filename(effect_file)
            # Create brain map figure
            plt.figure(figsize=(15, 5))
            plot_img(
                img,
                title=f"{contrast} - (ses-{session_match})",
                display_mode='z',
                cut_coords=(-10, 0, 10, 20, 30, 40, 50, 60, 70),
                colorbar=True,
                cmap='coolwarm',
                # vmin=-5,
                # vmax=5
            )    
            # Save brain map figure
            plt.savefig(f'{individual_contrasts_dir}/{subj_id}_{task_name}_contrast-{contrast}_ses-{session_match}.png')
            print(f"Saved individual contrast images for {contrast} to {individual_contrasts_dir}")
            plt.close()

        # prep data and mask
        eff_size_4d = nf.funcs.concat_images(all_eff_sizes)
        eff_size_4d_array = eff_size_4d.get_fdata()

        mask_img = masking.compute_epi_mask(eff_size_4d)

        # get min/max for colorbar (feel free to change)
        # We're mosty interested in finding outliers, so we don't really need to see
        # the full range of values
        # i.e., there will be a lot of gray in the image and those voxels are fine
        # as they will not be outliers
        data_nonzero = eff_size_4d_array[eff_size_4d_array.nonzero()]
        cutoff_max = np.quantile(data_nonzero, 0.9)
        cutoff_min = np.quantile(data_nonzero, 0.1)

        # Apply mask and plot
        data = apply_mask(eff_size_4d, mask_img)
        plt.figure(figsize=(20, 10))
        sns.heatmap(
            data,
            cmap='coolwarm',
            center=0,
            vmin=cutoff_min,
            vmax=cutoff_max
        )
        plt.xticks([], [])
        plt.xlabel('Voxels')
        plt.yticks(ticks=np.arange(len(all_con_names)), labels=all_con_names)
        plt.ylabel('Contrasts')
        plt.title(f'Effect sizes ({subj_id})')

        # plot stat maps
        nrows = len(fixed_fx_contrast_names)
        fig, axes = plt.subplots(nrows=nrows, ncols=1, figsize=(15, 2.5 * nrows))
        axes = np.ravel(axes)
        for i, fixed_fx_stat in enumerate(fixed_fx_stats):
            data = fixed_fx_stat.get_fdata()
            plot_img(
                fixed_fx_stat,
                title=fixed_fx_contrast_names[i],
                display_mode='z',
                cut_coords=(-10, 0, 10, 20, 30, 40, 50, 60, 70),
                vmin=-1 * data.max(),
                vmax=data.max(),
                colorbar=True,
                cmap='coolwarm',
                axes=axes[i],
            )
        plt.savefig(f'{fixed_effects_dir}/{subj_id}_{task_name}_effect_sizes_stat_maps.png')
        plt.close()
        print(
            f"Saved {subj_id}_{task_name}_effect_sizes_stat_maps.png to {fixed_effects_dir}"
        )



if __name__ == "__main__":
    main()
