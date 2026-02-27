from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from contextlib import asynccontextmanager
from anthropic import AsyncAnthropic
from app import claude, config
from app.schemas import AnalysisResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.client = AsyncAnthropic(api_key=config.ANTHROPIC_API_KEY)
    yield
    await app.state.client.close()

app = FastAPI(lifespan=lifespan)

ALLOWED_MIME_TYPES = {"image/png", "image/jpeg"}

@app.post("/summarize", response_model=AnalysisResponse)
async def summarize(
    image: UploadFile = File(...),
    caption: str = Form(...),
):
    if image.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=415, detail="Only PNG and JPEG are supported")

    image_bytes = await image.read()

    if len(image_bytes) > config.MAX_IMAGE_SIZE_BYTES:
        raise HTTPException(status_code=413, detail=f"Image exceeds {config.MAX_IMAGE_SIZE_MB}MB limit")

    return await claude.summarize(app.state.client, image_bytes, image.content_type, caption)