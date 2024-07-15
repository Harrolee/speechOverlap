import librosa
import numpy as np
import torch.nn as nn
import torch
from datasets import load_dataset
import torch.optim as optim


SAMPLE_RATE = 11025

data = load_dataset("audiofolder","dataset")
train = data["train"]
train = train.select(range(50))

# test = data["test"]
# validation = data["validation"]


# make a new dataset of pre-processed audio files
def make_melspec(datum):
    y, sr = librosa.load(datum["audio"]["path"], sr=SAMPLE_RATE)
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
    S_dB = librosa.power_to_db(S, ref=np.max)
    # Convert to tensor and add batch dimension
    S_dB_tensor = torch.tensor(S_dB, dtype=torch.float32).unsqueeze(0)  # Shape: (1, time_steps, n_mels)    
    print("S_dB_tensortype is ", (type(S_dB_tensor)))
    # print("shape of S_dB_tensortype is ", (S_dB_tensor.shape))
    label = 1 if datum["label"] == "overlap" else 0
    label = torch.tensor(label, dtype=torch.float32).unsqueeze(0)
    print("label is ", (label))
    print("label type is ", type(label))
    print("label shape is ", label.shape)
    return {"melspec": S_dB_tensor, "label": label}

preprocessed_dataset = train.map(make_melspec)
print(preprocessed_dataset)


class OverlapClassifier(nn.Module):

    def __init__(self, mel_bins, hidden_size):
        super().__init__()
        self.gru1 = nn.GRU(hidden_size=hidden_size, input_size=mel_bins, batch_first=True)
        # self.layer_norm1 = nn.LayerNorm(hidden_size)
        # self.gru2 = nn.GRU(hidden_size=hidden_size, input_size=mel_bins, batch_first=True)
        # self.layer_norm2 = nn.LayerNorm(hidden_size)
        # self.gru3 = nn.GRU(hidden_size=hidden_size//2, input_size=mel_bins, batch_first=True)
        # self.layer_norm3 = nn.LayerNorm(hidden_size//2)
        self.fc = nn.Linear(in_features=hidden_size//2, out_features=1)

    def forward(self, x):
        x, h1 = self.gru1(x)
        # x = self.layer_norm1(x)
        # x, h2 = self.gru2(x, h1)
        # x = self.layer_norm2(x)
        # x, _ = self.gru3(x, h2)
        # x = self.layer_norm3(x)
        out = self.fc(x)
        return out


mel_bins = 128
hidden_size = 256
gru_count = 3

model = OverlapClassifier(mel_bins, hidden_size)


model.train()

x_in = preprocessed_dataset[0]["melspec"]
output = model(x_in)



# Training

# EPOCHS = 10

# criterion = nn.BCEWithLogitsLoss()
# optimizer = optim.AdamW(model.parameters(), lr=0.01, weight_decay=0.0005)

# for epoch in range(EPOCHS):

#     running_loss = 0.0
#     for i, data in enumerate(preprocessed_dataset):
#         x_in = data["melspec"][i] # this seems to be a list. We need it to be a tensor.
#         label = data["label"]

#         optimizer.zero_grad()
#         output = model(x_in)
#         loss = criterion(output, label)
#         loss.backward()
#         optimizer.step()

#         running_loss += loss.item()
#         if i % 10 == 9: # print every 10 mini-batches
#             print('[%d, %5d] loss: %.3f' %(epoch + 1, i+1, running_loss / 20))
#             running_loss = 0.0

# print("Finished Training")

