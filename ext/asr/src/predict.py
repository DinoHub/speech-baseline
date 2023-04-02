import os
import logging
from typing import Union

import torch
import librosa
import gradio as gr
import soundfile as sf
import pytorch_lightning as pl
from nemo.utils import model_utils
from nemo.collections.asr.models import ASRModel

from config import config, BaseConfig

''' CPU/GPU Configurations '''
if torch.cuda.is_available():
    DEVICE = [0]  # use 0th CUDA device
    ACCELERATOR = 'gpu'
else:
    DEVICE = 1
    ACCELERATOR = 'cpu'

MAP_LOCATION: str = torch.device('cuda:{}'.format(DEVICE[0]) if ACCELERATOR == 'gpu' else 'cpu')

''' Gradio Input/Output Configurations '''
inputs: Union[str, gr.Audio] = gr.Audio(source='upload', type='filepath')
# inputs: Union[str, gr.inputs.Audio] = gr.inputs.Audio(source='upload', type='filepath')
outputs: str = 'text'

''' Helper functions '''
def initialize_asr_model(cfg: BaseConfig) -> ASRModel:

    model_cfg = ASRModel.restore_from(restore_path=cfg.asr_model_path, return_config=True)
    classpath = model_cfg.target  # original class path
    imported_class = model_utils.import_class_by_path(classpath)  # type: ASRModel
    logging.info(f"Restoring model : {imported_class.__name__}")
    asr_model = imported_class.restore_from(
        restore_path=cfg.asr_model_path, map_location=MAP_LOCATION,
    )

    trainer = pl.Trainer(devices=DEVICE, accelerator=ACCELERATOR)
    asr_model.set_trainer(trainer)
    asr_model = asr_model.eval()

    return asr_model

def preprocess_audio(audio_path: str, sample_rate: int = 16000, mono: bool = True, output_filename: str = 'output.wav') -> str:

    # loads and resamples to input sample_rate and convert to mono/stereo
    arr, sr = librosa.load(audio_path, sr=sample_rate, mono=mono)

    base_dir = os.path.dirname(audio_path)
    output_path = os.path.join(base_dir, output_filename)

    sf.write(output_path, arr, sample_rate)

    return output_path

''' Initialize models '''
asr_model = initialize_asr_model(config)

''' Main prediction function '''
def predict(audio_path: str) -> str:

    output_path = preprocess_audio(audio_path, sample_rate=16000, mono=True)

    with torch.no_grad():

        transcriptions = asr_model.transcribe(
            paths2audio_files=[output_path,],
            batch_size=1,
            num_workers=0,
            return_hypotheses=False,
        )

    return transcriptions[0]
