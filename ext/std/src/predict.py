import os
from typing import Union

import librosa
import gradio as gr
import soundfile as sf

from config import config

''' Gradio Input/Output Configurations '''
inputs: Union[str, gr.Audio] = gr.Audio(source='upload', type='filepath')
outputs: Union[str, gr.Audio] = gr.Audio()

''' Helper functions '''
def preprocess_audio(audio_path: str, sample_rate: int = 16000, mono: bool = True, output_filename: str = '/shared-data/output.wav') -> str:

    # loads and resamples to input sample_rate and convert to mono/stereo
    arr, sr = librosa.load(audio_path, sr=sample_rate, mono=mono)

    base_dir = os.path.dirname(audio_path)
    output_path = os.path.join(base_dir, output_filename)

    sf.write(output_path, arr, sample_rate)
    return output_path

''' Main prediction function '''
def predict(audio_path: str) -> str:

    return preprocess_audio(audio_path, sample_rate=config.sample_rate, mono=config.mono)
