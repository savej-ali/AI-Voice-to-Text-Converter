import torch
import soundfile as snd
import librosa
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer

# Initialize tokenizer and model for audio transcription
asr_tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
asr_model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

def prepare_audio(path_to_audio):
    # Resample and save a temporary 16kHz audio file
    waveform, sample_rate = librosa.load(path_to_audio, sr=16000)
    temp_output = "resampled_audio.wav"
    snd.write(temp_output, waveform, 16000)
    return temp_output

def generate_transcription(wav_file):
    # Read audio data
    audio_data, _ = snd.read(wav_file)
    
    # Tokenize audio waveform
    tokens = asr_tokenizer(audio_data, return_tensors="pt", padding="longest").input_values

    # Get model predictions
    with torch.no_grad():
        model_output = asr_model(tokens).logits

    # Decode prediction to text
    predicted_tokens = torch.argmax(model_output, dim=-1)
    result_text = asr_tokenizer.decode(predicted_tokens[0])

    return result_text
