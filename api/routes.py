from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from fastapi import APIRouter, Depends
from security import verify_api_key

from fastapi import APIRouter, Depends, HTTPException

from llm import llm
#from main import run_assistant

router = APIRouter()

from pydantic import BaseModel, Field
class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=2000
    )

class ChatResponse(BaseModel):
    answer: str

@router.post(
    "/chat",
    response_model=ChatResponse,
    dependencies=[Depends(verify_api_key)]
)
def chat(request: ChatRequest):

    try:

        from main import run_assistant

        answer = run_assistant(
            request.question
        )

        return ChatResponse(
            answer=answer
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to process the request."
        )

@router.post("/chat/stream",dependencies=[Depends(verify_api_key)])
def chat_stream(request: ChatRequest):

    def generate():

        for chunk in llm.stream(request.question):

            if chunk.content:
                yield chunk.content

    return StreamingResponse(
        generate(),
        media_type="text/plain"
    )