import base64
from app.schemas import AnalysisResponse

async def summarize(client, image_bytes: bytes, mime_type: str, caption: str) -> AnalysisResponse:
    b64 = base64.standard_b64encode(image_bytes).decode("utf-8")

    message = await client.messages.create(
        model="claude-opus-4-6",
        max_tokens=200,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {"type": "base64", "media_type": mime_type, "data": b64},
                    },
                    {
                        "type": "text",
                        "text": f"Caption: {caption}\n\nAnalyze this image and caption together and return a concise summary.",
                    },
                ],
            }
        ],
    )

    return AnalysisResponse(
        summary=message.content[0].text,
        input_tokens=message.usage.input_tokens,
        output_tokens=message.usage.output_tokens,
    )