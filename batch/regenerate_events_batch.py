#!/usr/bin/env python3
"""
Batch script to regenerate events files for multiple subjects and sessions.
"""

import subprocess
import sys
from pathlib import Path

def read_subject_list(filename):
    """Read subject IDs from a text file."""
    with open(filename, 'r') as f:
        subjects = [line.strip() for line in f if line.strip()]
    return subjects

def main():
    # Read subjects from all_subs.txt
    subjects_file = Path("validation_subs.txt")
    if not subjects_file.exists():
        print(f"Error: {subjects_file} not found")
        sys.exit(1)
    
    subjects = read_subject_list(subjects_file)
    sessions = ["ses-11", "ses-12", "ses-13"]
    
    print(f"Processing {len(subjects)} subjects for {len(sessions)} sessions")
    print(f"Subjects: {subjects}")
    print(f"Sessions: {sessions}")
    
    # Process each subject and session combination
    for subject in subjects:
        for session in sessions:
            print(f"\nProcessing {subject} {session}...")
            
            # Run the events regeneration script
            cmd = [
                "python", 
                "src/discovery_wm/tedana/04_prepare_glm_directory.py",
                "--subj-id", subject,
                "--session", session
            ]
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                print(f"✓ Successfully processed {subject} {session}")
                if result.stdout:
                    print(f"  Output: {result.stdout.strip()}")
            except subprocess.CalledProcessError as e:
                print(f"✗ Error processing {subject} {session}")
                print(f"  Error: {e.stderr.strip()}")
                continue
    
    print(f"\nBatch processing complete!")

if __name__ == "__main__":
    main() 