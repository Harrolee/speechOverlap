import librosa
import matplotlib.pyplot as plt
import numpy as np

path = "/Users/lee/projects/speechOverlap/split_dataset/train/modified/s1/bbaf4p.wav"

y, sr = librosa.load(path, sr=None)
S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
print("Samples", len(S))
print("Elements Per", len(S[0]))

S_dB = librosa.power_to_db(S, ref=np.max)


plt.figure()
librosa.display.specshow(S_dB)
plt.show()