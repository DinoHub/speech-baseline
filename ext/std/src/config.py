
from pydantic import BaseSettings, Field

class BaseConfig(BaseSettings):
    """Define any config here.

    See here for documentation:
    https://pydantic-docs.helpmanual.io/usage/settings/
    """
    # KNative assigns a $PORT environment variable to the container
    port: int = Field(default=8081, env="PORT",description="Gradio App Server Port")

    sample_rate: int = 16000
    mono: bool = True

config = BaseConfig()