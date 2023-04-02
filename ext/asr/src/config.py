
from pydantic import BaseSettings, Field

class BaseConfig(BaseSettings):
    """Define any config here.

    See here for documentation:
    https://pydantic-docs.helpmanual.io/usage/settings/
    """
    # KNative assigns a $PORT environment variable to the container
    port: int = Field(default=8084, env="PORT",description="Gradio App Server Port")
    asr_model_path: str = 'models/stt_en_conformer_ctc_large.nemo'
    punctuation_model_path: str = 'models/punctuation_en_bert.nemo'

config = BaseConfig()