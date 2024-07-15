from transformers import AutoModelForAudioClassification, AutoFeatureExtractor

model = AutoModelForAudioClassification.from_pretrained("facebook/wav2vec2-base")
feature_extractor = AutoFeatureExtractor.from_pretrained("facebook/wav2vec2-base")