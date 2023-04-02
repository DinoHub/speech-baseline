import logging

import gradio as gr
from config import BaseConfig
from predict import post_to_std, post_to_lid, post_to_asr, post_to_esc

logging.basicConfig(format="[%(asctime)s] %(levelname)s: %(message)s")
config = BaseConfig()

css = "footer {display: none !important;} #sp-gradio-container {min-height: 0px !important;}"

def asr_helper(language, audio_path):
    if language == 'en: English':
        return post_to_asr(audio_path)
    else:
        return 'Predicted Language is not English'

def mic_toggle(choice):
    if choice == 'Microphone':
        return gr.update(visible=True), gr.update(visible=False), gr.update(visible=True), gr.update(visible=False)
    else:
        return gr.update(visible=False), gr.update(visible=True), gr.update(visible=False), gr.update(visible=True)

def run_both_asr_esc(language, audio_path):
    return asr_helper(language, audio_path), post_to_esc(audio_path) 

with gr.Blocks(css=css) as demo:

        with gr.Row(variant='compact').style(equal_height=True):
            with gr.Column(scale=1, variant='compact'):
                r: gr.Radio = gr.Radio(['Microphone', 'File'], value='Microphone', label='How would you like to upload your audio?')
                bm: gr.Button = gr.Button()
                bf: gr.Button = gr.Button(visible=False)
            with gr.Column(scale=2, variant='compact'):
                m: gr.Mic = gr.Mic(label='Input', type='filepath')
                f: gr.Audio = gr.Audio(label='Input', type='filepath', visible=False)
                std_output: gr.Audio = gr.Audio(type='filepath')

        with gr.Column(variant='compact'):
            with gr.Row():
                with gr.Box():
                    lid_output: gr.Textbox = gr.Textbox(show_label=True, label='Language Identification')
                    asr_output: gr.Textbox = gr.Textbox(show_label=True, label='Automatic Speech Recognition', visible=True)
                esc_output: gr.Label = gr.Label(label='Environment Sounds')

        r.change(mic_toggle, r, [bm, bf, m, f])

        bm.click(post_to_std, m, std_output).then(post_to_lid, std_output, lid_output).then(run_both_asr_esc, [lid_output, std_output], [asr_output, esc_output])
        bf.click(post_to_std, f, std_output).then(post_to_lid, std_output, lid_output).then(run_both_asr_esc, [lid_output, std_output], [asr_output, esc_output])

if __name__ == "__main__":

    demo.launch(
        server_name="0.0.0.0",
        server_port=config.port,
        enable_queue=True,
    )
