from pydantic import BaseModel

class AnalysisResponse(BaseModel):
    summary: str
    input_tokens: int | None = None
    output_tokens: int | None = None