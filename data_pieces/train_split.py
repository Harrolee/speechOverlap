import os
import shutil
import random

# Paths to the original dataset
original_dir = 'dataset'
modified_dir = os.path.join(original_dir, 'modified')
unmodified_dir = os.path.join(original_dir, 'unmodified')

# New dataset directory
new_dataset_dir = 'split_dataset'
train_dir = os.path.join(new_dataset_dir, 'train')
test_dir = os.path.join(new_dataset_dir, 'test')
validate_dir = os.path.join(new_dataset_dir, 'validate')

# Function to create directories for train, test, and validate
def create_dirs(base_dir, subdirs):
    for subdir in subdirs:
        mod_path = os.path.join(base_dir, 'modified', subdir)
        unmod_path = os.path.join(base_dir, 'unmodified', subdir)
        os.makedirs(mod_path, exist_ok=True)
        os.makedirs(unmod_path, exist_ok=True)

# Get subdirectories in modified and unmodified
subdirs = sorted(os.listdir(modified_dir))

# Create corresponding directories in train, test, and validate
create_dirs(train_dir, subdirs)
create_dirs(test_dir, subdirs)
create_dirs(validate_dir, subdirs)

# Function to split files into train, test, and validate sets
def split_files(files, train_ratio=0.85, test_ratio=0.10, validate_ratio=0.05):
    random.shuffle(files)
    train_end = int(train_ratio * len(files))
    test_end = train_end + int(test_ratio * len(files))
    
    train_files = files[:train_end]
    test_files = files[train_end:test_end]
    validate_files = files[test_end:]
    
    return train_files, test_files, validate_files

# Function to copy files to the corresponding directories
def copy_files(files, src_dir, dst_dir, subdir):
    for file in files:
        shutil.copy(os.path.join(src_dir, subdir, file), os.path.join(dst_dir, subdir, file))

# Process each subdirectory in modified and unmodified
for subdir in subdirs:
    mod_files = [f for f in os.listdir(os.path.join(modified_dir, subdir)) if f.endswith('.wav')]
    unmod_files = [f for f in os.listdir(os.path.join(unmodified_dir, subdir)) if f.endswith('.wav')]
    
    train_mod_files, test_mod_files, validate_mod_files = split_files(mod_files)
    train_unmod_files, test_unmod_files, validate_unmod_files = split_files(unmod_files)
    
    copy_files(train_mod_files, modified_dir, os.path.join(train_dir, 'modified'), subdir)
    copy_files(test_mod_files, modified_dir, os.path.join(test_dir, 'modified'), subdir)
    copy_files(validate_mod_files, modified_dir, os.path.join(validate_dir, 'modified'), subdir)
    
    copy_files(train_unmod_files, unmodified_dir, os.path.join(train_dir, 'unmodified'), subdir)
    copy_files(test_unmod_files, unmodified_dir, os.path.join(test_dir, 'unmodified'), subdir)
    copy_files(validate_unmod_files, unmodified_dir, os.path.join(validate_dir, 'unmodified'), subdir)

print("Dataset distribution completed successfully.")
