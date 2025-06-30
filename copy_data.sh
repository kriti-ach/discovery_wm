# Set source and destination paths (Variables are easier to maintain)
source_dir="/scratch/users/kritiach/discovery_wm/output_lev1_mni_validation"
destination_dir="/oak/stanford/groups/russpold/data/network_grant/validation_BIDS/derivatives/output_lev1_mni"

# Find all subject directories in the source
find "$source_dir" -maxdepth 1 -type d -name "sub-*" | while read source_subject_dir; do
    # Extract subject ID (e.g., sub-s03)
    subject_id=$(basename "$source_subject_dir")

    # Construct the destination path for the subject
    destination_subject_dir="$destination_dir/$subject_id"

    # Check if the destination directory exists (important!)
    if [ -d "$destination_subject_dir" ]; then
        # Copy the contents of the source subject directory to the destination subject directory
        cp -r "$source_subject_dir/"* "$destination_subject_dir/"
        echo "Copied data for $subject_id" #  Confirmation
    else
        echo "Warning: Destination directory $destination_subject_dir does not exist. Skipping $subject_id"
    fi
done