import os
from pydub import AudioSegment
from pydub.silence import detect_leading_silence

trim_leading_silence = lambda x: x[detect_leading_silence(x) :]
trim_trailing_silence = lambda x: trim_leading_silence(x.reverse()).reverse()
strip_silence = lambda x: trim_trailing_silence(trim_leading_silence(x))

# source_path = "/Users/lee/projects/speechOverlap/interrupts"
source_path = "/Users/lee/projects/speechOverlap/vui/data/content"

for file in os.listdir(source_path):
    sound: AudioSegment = AudioSegment.from_file(os.path.join(source_path, file), format="wav")
    stripped: AudioSegment = strip_silence(sound)
    stripped.export(os.path.join(source_path, "trimmed", file), format="wav")