import wave
from pydub import AudioSegment

def match_duration(wav_file1, wav_file2, output_file):
    # Open the first wav file to get its duration
    with wave.open(wav_file1, 'r') as wf1:
        duration1 = wf1.getnframes() / wf1.getframerate()
    
    # Load the second wav file using pydub
    audio2 = AudioSegment.from_wav(wav_file2)
    
    # Calculate the duration in milliseconds
    duration1_ms = int(duration1 * 1000)
    
    # Trim the second audio to match the duration of the first audio
    if len(audio2) > duration1_ms:
        trimmed_audio2 = audio2[:duration1_ms]
    else:
        trimmed_audio2 = audio2
    
    # Export the trimmed audio
    trimmed_audio2.export(output_file, format="wav")

# Example usage
wav_file1 = 'path/to/first.wav'
wav_file2 = 'path/to/second.wav'
output_file = 'path/to/output.wav'

match_duration(wav_file1, wav_file2, output_file)
