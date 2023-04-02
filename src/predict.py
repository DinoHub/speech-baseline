import base64
import requests
import numpy as np
import librosa

from config import config

def post_to_std(audio_path: str) -> str:

    with open(audio_path, 'rb') as audio_str:
        byte_string = base64.b64encode(audio_str.read()).decode('utf-8')

    response = requests.post(config.std_api, json={
        "data": [
            {"name":'audio.wav',"data":f"data:audio/wav;base64,{byte_string}"},
        ]
    }).json()

    print(response)

    audio, sr = librosa.load('/shared-data/output.wav', sr=None)

    # base64_data = response['data'][0].replace('data:audio/wav;base64,', '')
    # msg = base64.b64decode(base64_data)

    # audio = np.frombuffer(msg, dtype=np.int16)
    # audio = audio.astype(np.float32, order='C') / 32767

    return (sr, audio) 


def post_to_lid(audio_path: str) -> str:

    with open(audio_path, 'rb') as audio_str:
        byte_string = base64.b64encode(audio_str.read()).decode('utf-8')

    response = requests.post(config.lid_api, json={
        "data": [
            {"name":'audio.wav',"data":f"data:audio/wav;base64,{byte_string}"},
        ]
    }).json()

    data = response["data"][0]

    return data


def post_to_asr(audio_path: str) -> str:

    with open(audio_path, 'rb') as audio_str:
        byte_string = base64.b64encode(audio_str.read()).decode('utf-8')

    response = requests.post(config.asr_api, json={
        "data": [
            {"name":'audio.wav',"data":f"data:audio/wav;base64,{byte_string}"},
        ]
    }).json()

    data = response["data"][0]
    print(data)

    return data


def post_to_esc(audio_path: str) -> str:

    with open(audio_path, 'rb') as audio_str:
        byte_string = base64.b64encode(audio_str.read()).decode('utf-8')

    response = requests.post(config.esc_api, json={
        "data": [
            {"name":'audio.wav',"data":f"data:audio/wav;base64,{byte_string}"},
        ]
    }).json()

    data = response["data"][0]['confidences']
    data = {x['label']:x['confidence'] for x in data}
    print(data)

    return data
