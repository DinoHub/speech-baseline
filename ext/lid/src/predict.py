from config import config, BaseConfig
from typing import Union

import torch
import gradio as gr
from speechbrain.pretrained import EncoderClassifier

''' Gradio Input/Output Configurations '''
inputs: Union[str, gr.Audio] = gr.Audio(source='upload', type='filepath')
outputs: Union[str, gr.Textbox] = gr.Textbox()


''' CPU/GPU Configurations '''
if torch.cuda.is_available():
    DEVICE = [0]  # use 0th CUDA device
    ACCELERATOR = 'gpu'
else:
    DEVICE = 1
    ACCELERATOR = 'cpu'

MAP_LOCATION: str = torch.device('cuda:{}'.format(DEVICE[0]) if ACCELERATOR == 'gpu' else 'cpu')


''' Helper functions '''
def initialize_lid_model(cfg: BaseConfig) -> EncoderClassifier:

    lid_model = EncoderClassifier.from_hparams(source=cfg.model_source, savedir=cfg.model_dir)

    return lid_model


''' Initialize models '''
lid_model = initialize_lid_model(config)


''' Main prediction function '''
def predict(audio_path: str) -> str:

    signal = lid_model.load_audio(audio_path)
    prediction =  lid_model.classify_batch(signal)
    language = prediction[3][0]

    return language
