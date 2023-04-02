
from pydantic import BaseSettings, Field

class BaseConfig(BaseSettings):
    """Define any config here.

    See here for documentation:
    https://pydantic-docs.helpmanual.io/usage/settings/
    """
    # KNative assigns a $PORT environment variable to the container
    port: int = Field(default=8082, env="PORT",description="Gradio App Server Port")
    model_source: str = "speechbrain/lang-id-voxlingua107-ecapa"
    model_dir: str = "models"

config = BaseConfig()