from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from fastapi.responses import StreamingResponse

from pydantic import (
    BaseModel,
    Field
)

from security import verify_api_key
from llm import llm


router = APIRouter()


class ChatRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=1,
        max_length=2000
    )


class Source(BaseModel):

    source: str
    page: int | None = None


class ChatResponse(BaseModel):

    answer: str
    sources: list[Source] = Field(
        default_factory=list
    )


@router.post(
    "/chat",
    response_model=ChatResponse,
    dependencies=[
        Depends(verify_api_key)
    ]
)
def chat(
    request: ChatRequest
):

    try:

        from main import run_assistant

        result = run_assistant(
            request.question,
            include_sources=True
        )

        return ChatResponse(
            answer=str(
                result["answer"]
            ),
            sources=result.get(
                "sources",
                []
            )
        )

    except Exception as e:

        import traceback

        print(
            "\n========== CHAT ERROR =========="
        )

        print(str(e))

        traceback.print_exc()

        print(
            "================================\n"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.post(
    "/chat/stream",
    dependencies=[
        Depends(verify_api_key)
    ]
)
def chat_stream(
    request: ChatRequest
):

    def generate():

        try:

            for chunk in llm.stream(
                request.question
            ):

                content = chunk.content

                if isinstance(
                    content,
                    str
                ):

                    if content:
                        yield content

                elif isinstance(
                    content,
                    list
                ):

                    for item in content:

                        if isinstance(
                            item,
                            dict
                        ):

                            text = item.get(
                                "text",
                                ""
                            )

                            if text:
                                yield text

        except Exception as e:

            print(
                "\n========== STREAM ERROR =========="
            )

            print(str(e))

            print(
                "==================================\n"
            )

            yield f"Error: {str(e)}"

    return StreamingResponse(
        generate(),
        media_type="text/plain"
    )