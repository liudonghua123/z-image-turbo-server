from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_KEY: str = "sk-dummy-key" # Placeholder for auth if needed, strict OpenAI compat might need it
    PRETRAINED_MODEL_NAME: str = "Tongyi-MAI/Z-Image-Turbo"
    MODEL_ID: str = "z-image-turbo"
    DEVICE: str = "cuda"
    DTYPE: str = "bfloat16" # 'float16' or 'bfloat16'
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    class Config:
        env_file = ".env"

settings = Settings()
