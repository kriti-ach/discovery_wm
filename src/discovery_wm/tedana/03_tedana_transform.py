import logging
import os
from pathlib import Path

from nipype.interfaces.ants import ApplyTransforms

from discovery_wm.utils import get_path_config, get_parser, get_subj_id, get_ses_task_run

def apply_xforms(scan, outpath, xforms, reference):
    at = ApplyTransforms()
    at.inputs.input_image = scan
    at.inputs.reference_image = reference
    at.inputs.output_image = outpath
    at.inputs.interpolation = "LanczosWindowedSinc"
    at.inputs.transforms = xforms
    at.inputs.input_image_type = 3
    at.run()

def main() -> None:
    logging.basicConfig(level=logging.INFO)

    _, fmriprep_dir, _, tedana_denoised_dir, tedana_transformed_dir, _, _, = get_path_config()

    # Parse the command line arguments
    parser = get_parser()
    subj_id = get_subj_id(parser)

    subj_fmriprep_dir = Path(fmriprep_dir / subj_id)
    subj_tedana_dir = Path(tedana_denoised_dir / subj_id)
    outdir = Path(tedana_transformed_dir / subj_id)
    outdir.mkdir(parents=True, exist_ok=True)

    for f in subj_tedana_dir.glob('**/*optcom*.nii.gz'):
        ses, task_name, run_number = get_ses_task_run(f.parent)

        logging.info(f'Processing {f.name} - {ses} - {task_name} - {run_number}')

        fmriprep_ses_dir = subj_fmriprep_dir / ses / "func"

        # bold_to_t1_xforms = list(fmriprep_ses_dir.glob(f"*{task_name}*from-boldref_to-T1w_mode-image_desc-coreg_xfm.txt"))
        # bold_to_t1_space = list(fmriprep_ses_dir.glob(f"*{task_name}*space-T1w_boldref.nii.gz"))
        bold_to_mni_space = list(fmriprep_ses_dir.glob(f"*{task_name}*space-MNI152NLin2009cAsym_res-2_boldref.nii.gz"))
        t1w_to_mni_space = list(subj_fmriprep_dir.glob(f'ses-*/anat/*from-T1w_to-MNI152NLin2009cAsym_mode-image_xfm.h5'))

        # prepare outdirs
        outdir_full = outdir / ses / "func"
        outdir_full.mkdir(parents=True, exist_ok=True)

        # full outpath
        outpath = outdir_full / f"{subj_id}_{ses}_{task_name}_{run_number}_space-MNI152NLin2009cAsym_res-2_desc-optcom_bold.nii.gz"

        if os.path.isfile(outpath):
            logging.warning(f"Skipping: {outpath} exists...")
            continue

        print(f'Applying transforms for {outpath}')
        apply_xforms(
            scan=str(f),
            xforms=str(bold_to_mni_space[0]),
            outpath=str(outpath),
            reference=str(t1w_to_mni_space[0]),
        )
        print(f'Finished applying transforms for {outpath}')

if __name__ == "__main__":
    main()
