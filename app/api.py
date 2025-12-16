from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.schemas import ImageGenerationRequest, ImageGenerationResponse, ImageObject
from app.service import service
import time
import base64
from io import BytesIO
import uuid

router = APIRouter()

def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

@router.post("/v1/images/generations", response_model=ImageGenerationResponse)
async def generate_image(request: ImageGenerationRequest):
    try:
        # Map OpenAI request to model params
        # "1024x1024" -> 1024, 1024
        size_map = {
            "1024x1024": (1024, 1024),
            "512x512": (512, 512), # Maybe support other sizes?
        }
        width, height = size_map.get(request.size, (1024, 1024))
        
        image = service.generate(
            prompt=request.prompt,
            width=width,
            height=height,
            steps=4, # Turbo is fast, maybe make configurable or stick to 4-9
        )
        
        # Determine response format
        response_data = []
        
        # In a real production app, we would upload to S3 and return URL
        # For this standalone, we might return base64 or a local URL if serving static files
        # OpenAI default is 'url'. We will assume 'b64_json' effectively or return a dummy URL if we can't serve.
        # But for 'url' to work, we need to save file and serve it.
        # Let's support b64_json for simplicity as it's self-contained.
        # If user asked for 'url', we might warn or just return b64 anyway if we don't have storage.
        # Let's try to implement b64_json properly.
        
        b64_img = image_to_base64(image)
        
        img_obj = ImageObject()
        if request.response_format == "b64_json":
           img_obj.b64_json = b64_img
        else:
           # Fallback for URL: we could host it, but let's just put the data URI in url for loose compatibility 
           # or a fake one. 'data:image/png;base64,...' works in some browsers.
           img_obj.url = f"data:image/png;base64,{b64_img}"
           
        response_data.append(img_obj)

        return ImageGenerationResponse(
            created=int(time.time()),
            data=response_data
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
