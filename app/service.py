import torch
from diffusers import DiffusionPipeline
# Try importing ZImagePipeline, fallback to DiffusionPipeline if it's auto-mapped
try:
    from diffusers import ZImagePipeline
except ImportError:
    ZImagePipeline = None
    
from app.config import settings
import base64
from io import BytesIO

class ModelService:
    def __init__(self):
        self.pipe = None

    def load_model(self):
        print(f"Loading model {settings.PRETRAINED_MODEL_NAME}...")
        dtype = torch.bfloat16 if settings.DTYPE == "bfloat16" else torch.float16
        
        # If ZImagePipeline is available, use it. Otherwise rely on auto-loading via DiffusionPipeline
        if ZImagePipeline:
            self.pipe = ZImagePipeline.from_pretrained(
                settings.PRETRAINED_MODEL_NAME,
                torch_dtype=dtype,
                low_cpu_mem_usage=False,
            )
        else:
            self.pipe = DiffusionPipeline.from_pretrained(
                settings.PRETRAINED_MODEL_NAME,
                torch_dtype=dtype,
                low_cpu_mem_usage=False,
            )

        if settings.DEVICE == "cuda" and torch.cuda.is_available():
            self.pipe.to("cuda")
        else:
            print("Warning: CUDA not found or not requested, running on CPU might be slow/impossible for bfloat16")
            # You might need to switch to float32 for CPU or compatible types

    def generate(self, prompt: str, height: int = 1024, width: int = 1024, steps: int = 9, seed: int = 42):
        if not self.pipe:
            raise RuntimeError("Model not loaded")
        
        generator = torch.Generator(device=settings.DEVICE).manual_seed(seed)
        
        # Guidance scale 0 for Turbo
        image = self.pipe(
            prompt=prompt,
            height=height,
            width=width,
            num_inference_steps=steps,
            guidance_scale=0.0,
            generator=generator
        ).images[0]
        
        return image

service = ModelService()
