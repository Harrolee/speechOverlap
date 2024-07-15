import os
import csv

# Define the root directory of your dataset
root_dir = 'dataset/test'
output_csv = 'output-test2.csv'

# Function to recursively get all .wav files, their labels, and speakers
def get_wav_files_labels_speakers(root_dir):
    wav_files_info = []
    for root, _, files in os.walk(root_dir):
        base_dir = os.path.basename(root)
        parent_dir = os.path.basename(os.path.dirname(root))
        if parent_dir in ['overlap', 'noOverlap']:
            label = parent_dir
            speaker = base_dir
            for file in files:
                if file.endswith('.wav'):
                    file_path = os.path.join(root, file)
                    wav_files_info.append((file_path, label, speaker))
    return wav_files_info

# Get the list of .wav files, their labels, and speakers
wav_files_info = get_wav_files_labels_speakers(root_dir)

# Write the list to a CSV file
with open(output_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['file_name', 'label', 'speaker'])
    writer.writerows(wav_files_info)

print(f"CSV file '{output_csv}' created successfully.")


# import os
# import csv

# # Define the root directory of your dataset
# root_dir = 'dataset/validate'
# output_csv = 'output-validate.csv'

# # Function to recursively get all .wav files and their labels
# def get_wav_files_and_labels(root_dir):
#     wav_files_and_labels = []
#     for root, _, files in os.walk(root_dir):
#         base_dir = os.path.basename(root)
#         parent_dir = os.path.basename(os.path.dirname(root))
#         if parent_dir in ['overlap', 'noOverlap']:
#             label = parent_dir
#             for file in files:
#                 if file.endswith('.wav'):
#                     file_path = os.path.join(root, file)
#                     wav_files_and_labels.append((file_path, label))
#     return wav_files_and_labels

# # Get the list of .wav files and their labels
# wav_files_and_labels = get_wav_files_and_labels(root_dir)

# # Write the list to a CSV file
# with open(output_csv, mode='w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(['file_name', 'label'])
#     writer.writerows(wav_files_and_labels)

# print(f"CSV file '{output_csv}' created successfully.")
