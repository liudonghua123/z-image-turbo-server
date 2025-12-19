import torch
import asyncio
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
        self.queue = asyncio.Queue()

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

    async def start_worker(self):
        """Background worker to process requests from the queue."""
        print("Starting model worker...")
        while True:
            params, future = await self.queue.get()
            try:
                # Run generation in a separate thread to avoid blocking the event loop
                # self.generate is CPU blocking (even with GPU, the python side waits)
                result = await asyncio.to_thread(self.generate, **params)
                future.set_result(result)
            except Exception as e:
                future.set_exception(e)
            finally:
                self.queue.task_done()

    async def process_request(self, **kwargs):
        """Enqueue a request and wait for the result."""
        loop = asyncio.get_running_loop()
        future = loop.create_future()
        await self.queue.put((kwargs, future))
        return await future

service = ModelService()
