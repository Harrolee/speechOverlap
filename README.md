# Goal

Conversational agents are sweet! See Hume's EVI, Call Alice, and Fixie's ai.town. These three know when they are being interrupted, somehow.

## My guesses

- A speaker diarization model
- A speech activity model
- DSP in the browser

# Results

## Speech Activity

### Build a dataset

I made a dataset of overlapped speech called [grid-overlap](https://huggingface.co/datasets/LeeHarrold/grid-overlap) from audio in the [GRID audiovisual sentence corpus](https://spandh.dcs.shef.ac.uk/gridcorpus/).

#### How?

- I recorded six clips of myself saying something I might say to interrupt an assistant. See the filenames in [interrupts](data_pieces/interrupts)
- I embedded the clips into one half of the total audio recordings from GRID. See [add_overlaps.py](data_pieces/add_overlaps.py)
  1.  50% with interruption, 50% without interruption.
  2.  10% validation, 20% test, 70% train

#### More info

audio_25k from the Grid AudioVisual dataset contains 1k recordings for each of 30 speakers.

### Finetune wav2vec2

See this [train_overlap Colab notebook](https://colab.research.google.com/drive/1SATrvULB7OoTaGZOXFKLxJYlGFDBAwWY?usp=sharing)

### Test inference speed

- Code for inference is at the end of the above notebook
- A finetuned wav2vec running on a T4 took about 1.41 seconds to classify a <1 second recording.
- This is too slow

## DSP in the browser

_see [vui](/vui/README.md)_

# archive

## Mission: WavSurfer

_wav2vec in the browser_

**Q:** test time it takes to

1. featureExtract 1sec of audio
2. classify that audio as overlap or not overlap
   **A:** `1.41 s ± 318 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)`
   ^^ With a T4 in python, using the pipeline abstraction:

```
path_to_model="/content/drive/MyDrive/wav2vec2-base-detect-overlap"
classifier = pipeline("audio-classification", model=path_to_model)
```

Recon:
Is there a wav2vec model that can be used in the browser?
Yes. Might be worth learning the time it takes your browser to classify audio.

Fear:
Is tokenizing input going to take a long time? Maybe not, cuz browsers have ASR and speech recognition

## Known Unknowns

- Dataset is in 44khz
- Same speaker is used for every interrupt
- there are only 6 interrupt variants. These are likely easily learned
