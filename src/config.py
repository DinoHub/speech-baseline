
from pydantic import BaseSettings, Field

class BaseConfig(BaseSettings):
    """Define any config here.

    See here for documentation:
    https://pydantic-docs.helpmanual.io/usage/settings/
    """
    # KNative assigns a $PORT environment variable to the container
    port: int = Field(default=8080, env="PORT",description="Gradio App Server Port")

    std_api: str = "http://std-inference:8081/run/predict"
    lid_api: str = "http://lid-inference:8082/run/predict"
    esc_api: str = "http://esc-inference:8083/run/predict"
    asr_api: str = "http://asr-inference:8084/run/predict"

    sample_rate: int = 16000
    mono: bool = True

config = BaseConfig()