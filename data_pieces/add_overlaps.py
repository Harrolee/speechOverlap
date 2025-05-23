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
    return os.path.join(dir_data.get("output_directory"), tag, dir_data.get("curr_dir"), dir_data.get("filename"))

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

    # random offset from end of audio file
    # offset's length is in range 3-9% of the original_audio's length
    offset_from_end = (int) (random.randint(3,9)*.01 * len(original_audio)) 

    # make sure we don't add the interrupt after speech ends
    if len(original_audio) > len(interrupt):
        max_insert_position = len(original_audio) - ( len(interrupt) + offset_from_end)
    else:
        max_insert_position = len(original_audio) - offset_from_end

    # if max_insert_position == 0:
    #     insert_position = max_insert_position
    # else:
    try:
        insert_position = random.randint(0, max_insert_position)
    except:
        print(max_insert_position)
        print(f"len(interrupt) = {len(interrupt)}")
        print(f"len(original_audio) = {len(original_audio)}")
        print(f"offset_from_end = {offset_from_end}")
        print(f"len(original_audio) - ( len(interrupt) + offset_from_end) = {len(original_audio) - ( len(interrupt) + offset_from_end)}")
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
    os.makedirs(os.path.join(dir_data.get("output_directory"), MODIFIED, dir_data.get("curr_dir")), exist_ok=True)
    os.makedirs(os.path.join(dir_data.get("output_directory"), UNMODIFIED, dir_data.get("curr_dir")), exist_ok=True)

    # all of the recordings for a given speaker
    filenames = [filename for filename in os.listdir(os.path.join(dir_data.get("input_directory"), dir_data.get("curr_dir"))) if filename.endswith(".wav")]
    for filename in filenames:
        dir_data["filename"] = filename

        processed_files.get("files").append(dir_data.get("filename"))
        # os.makedirs(os.path.join(dir_data.get("output_directory"), dir_data.get("curr_dir")), exist_ok=True)
        # I think I can delete this^^
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




