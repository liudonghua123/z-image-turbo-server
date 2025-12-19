from pydantic import BaseModel
from typing import List, Optional

class ImageGenerationRequest(BaseModel):
    prompt: str
    model: Optional[str] = "dall-e-3" # Copmaptibility
    n: Optional[int] = 1
    size: Optional[str] = "1024x1024"
    response_format: Optional[str] = "url" # or "b64_json"
    quality: Optional[str] = "standard"
    style: Optional[str] = "natural"

class ImageObject(BaseModel):
    url: Optional[str] = None
    b64_json: Optional[str] = None
    revised_prompt: Optional[str] = None

class ImageGenerationResponse(BaseModel):
    created: int
    data: List[ImageObject]

class ModelCard(BaseModel):
    id: str
    object: str = "model"
    created: int = 0
    owned_by: str = "z-image-turbo"

class ModelListResponse(BaseModel):
    object: str = "list"
    data: List[ModelCard]
