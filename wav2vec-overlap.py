# original colab: https://colab.research.google.com/drive/1SATrvULB7OoTaGZOXFKLxJYlGFDBAwWY?usp=sharing

# below is copy-pasted from the colab

# -*- coding: utf-8 -*-
"""TrainOverlap.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1SATrvULB7OoTaGZOXFKLxJYlGFDBAwWY
"""

#!pip install datasets evaluate transformers[torch]

from transformers import AutoModelForAudioClassification, AutoFeatureExtractor

# model = AutoModelForAudioClassification.from_pretrained("facebook/wav2vec2-base")
feature_extractor = AutoFeatureExtractor.from_pretrained("facebook/wav2vec2-base")

from datasets import load_dataset, Audio

dataset = load_dataset("LeeHarrold/grid-overlap")
dataset = dataset.cast_column("audio", Audio(sampling_rate=16000))
# dataset["train"]
# dataset["test"]

train = dataset["train"].shuffle(seed=77) #.select(range(len(dataset["train"])//2))
test = dataset["test"].shuffle(seed=77) #.select(range(len(dataset["test"])//2))

# convince myself that label distribution is even
import matplotlib.pyplot as plt
plt.plot(train["label"])
count_labels = train["label"]

def preprocess_function(examples):
    audio_arrays = [x["array"] for x in examples["audio"]]
    inputs = feature_extractor(
        audio_arrays,
        sampling_rate=16000,
        padding=True,
        max_length=50000,
        truncation=True,
    )
    return inputs

train = train.map(preprocess_function, batched=True)
test = test.map(preprocess_function, batched=True)

def preprocess_labels(examples):
    label = 1 if examples["label"] == "overlap" else 0
    return {"labels": label}

train = train.map(preprocess_labels)
test = test.map(preprocess_labels)

train.remove_columns(["speaker", "label", "audio"])
test.remove_columns(["speaker", "label", "audio"])

# create a map of labels to ids

labels = train["labels"] + test["labels"]
label2id, id2label = dict(), dict()
for i, label in enumerate(labels):
    label2id[label] = str(i)
    id2label[str(i)] = label

train.set_format(type="torch", columns=["input_values", "labels"])
test.set_format(type="torch", columns=["input_values", "labels"])

"""### Eval"""

import evaluate
import numpy as np

accuracy = evaluate.load("accuracy")

def compute_metrics(eval_pred):
    predictions = np.argmax(eval_pred.predictions, axis=1)
    return accuracy.compute(predictions=predictions, references=eval_pred.label_ids)

"""### Train with Trainer"""

from transformers import AutoModelForAudioClassification, TrainingArguments, Trainer

num_labels = len(id2label)
model = AutoModelForAudioClassification.from_pretrained(
    "facebook/wav2vec2-base", num_labels=num_labels, label2id=label2id, id2label=id2label
)

import torch
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
model.to(device)

training_args = TrainingArguments(
    output_dir="detect_overlap_model",
    eval_strategy="epoch",
    save_strategy="epoch",
    learning_rate=3e-5,
    per_device_train_batch_size=32,
    gradient_accumulation_steps=4,
    per_device_eval_batch_size=32,
    num_train_epochs=10,
    warmup_ratio=0.1,
    logging_steps=10,
    load_best_model_at_end=True,
    metric_for_best_model="accuracy",
    push_to_hub=True,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train,
    eval_dataset=test,
    tokenizer=feature_extractor,
    compute_metrics=compute_metrics,
)

trainer.train()

# !mkdir drive/MyDrive/wav2vec2-base-detect-overlap
trainer.save_model("drive/MyDrive/wav2vec2-base-detect-overlap2")

#!pip install --upgrade huggingface_hub

from huggingface_hub import login
login()

"""# Inference Timing"""

# test some validation dataset examples

speed_test = test.select(range(10))
speed_test.set_format(type="torch", columns=["input_values"])

len(speed_test)

type(speed_test[0]["input_values"])
input_array = speed_test[0]["input_values"].detach().cpu().numpy()
type(input_array)

from transformers import pipeline

path_to_model="/content/drive/MyDrive/wav2vec2-base-detect-overlap"

classifier = pipeline("audio-classification", model=path_to_model)

# Commented out IPython magic to ensure Python compatibility.
# %%timeit
# classifier(input_array)