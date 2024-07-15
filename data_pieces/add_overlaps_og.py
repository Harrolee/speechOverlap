from pydub import AudioSegment
import os
import random
import shutil
import json

# Load the "wait" recording
# wait_sound = AudioSegment.from_wav("interrupts/to/wait.wav")

MODIFIED = "modified"
UNMODIFIED = "unmodified"

dir_data = {
    # Directory containing the 3000 audio files
    "input_directory" : "audio_25k",
    "output_directory" : "dataset",
    "interrupt_directory" : "interrupts",
    "curr_dir" : "",
    "filename" : ""
}

def source_file():
    return os.path.join(dir_data.get("input_directory"), dir_data.get("curr_dir"), dir_data.get("filename"))

def dest_file(tag = ""):
    return os.path.join(dir_data.get("output_directory"), dir_data.get("curr_dir"), tag, dir_data.get("filename"))

def select_interrupt():
    interrupts = [file for file in os.listdir(dir_data.get("interrupt_directory")) if file.endswith(".wav")]
    interrupt = random.choice(interrupts)
    interrupt = AudioSegment.from_wav(os.path.join(dir_data.get("interrupt_directory"),interrupt))
    return interrupt

def handle_unmodified():   
    # just move the file to the new directory
    # dest = os.path.join(dir_data.get("output_directory"), dir_data.get("curr_dir"), dir_data.get("filename"))
    shutil.copy(source_file(), dest_file(UNMODIFIED))

def handle_modified():
    # Load the original audio file
    original_audio = AudioSegment.from_wav(source_file())
    interrupt = select_interrupt()
    # Calculate a random insertion point
    max_insert_position = len(original_audio) - (int) ( len(interrupt) + .1*len(original_audio) )
    insert_position = random.randint(0, max_insert_position)
    # Overlay the "wait" sound at the random insertion point
    combined_audio = original_audio.overlay(interrupt, position=insert_position)
    # Export the combined audio to the output directory
    combined_audio.export(dest_file(MODIFIED), format="wav")


# Ensure the output directory exists
os.makedirs(dir_data.get("output_directory"), exist_ok=True)


processed_dirs = {"dirs": {}}

dirs = [dir for dir in os.listdir(dir_data.get("input_directory")) if os.path.isdir(dir_data.get("input_directory") + "/" + dir)]
for curr_dir in dirs: 
    dir_data["curr_dir"] = curr_dir
    processed_files = {MODIFIED: 0, UNMODIFIED: 0, "files": []}
    os.makedirs(os.path.join(dir_data.get("output_directory"), dir_data.get("curr_dir"), MODIFIED), exist_ok=True)
    os.makedirs(os.path.join(dir_data.get("output_directory"), dir_data.get("curr_dir"), UNMODIFIED), exist_ok=True)

    # all of the recordings for a given speaker
    filenames = [filename for filename in os.listdir(os.path.join(dir_data.get("input_directory"), dir_data.get("curr_dir"))) if filename.endswith(".wav")]
    for filename in filenames:
        dir_data["filename"] = filename

        processed_files.get("files").append(dir_data.get("filename"))
        os.makedirs(os.path.join(dir_data.get("output_directory"), dir_data.get("curr_dir")), exist_ok=True)
        set_name = random.choice([MODIFIED,UNMODIFIED])
        if set_name == UNMODIFIED:
            processed_files[UNMODIFIED] += 1
            # copy file into different directory
            handle_unmodified()
        else:
            processed_files[MODIFIED] += 1
            # modify file and copy to new directory
            handle_modified()
    processed_dirs.get("dirs").update({curr_dir: processed_files})
                
json.dumps(processed_dirs)
with open("report.json", "+w") as f:
    json.dump(processed_dirs, f, indent=4)

    # randomly select 500 files
        # copy those into dataset/{name of current speaker}/
    # the others:
        # modify them and put them into dataset/{name of current speaker}/


print("Processing complete.")




