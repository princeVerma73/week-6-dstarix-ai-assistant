from pathlib import Path

from fastapi import FastAPI

from api.routes import router

from tools.tools import (
    get_project_info,
    get_internship_phase
)

from rag.query_transform import transform_query
from rag.retrieval import retrieve_documents
from rag.reranker import rerank_documents
from rag.prompts import RAG_PROMPT

from memory.conversation import ConversationMemory

from llm import llm


# ============================================================
# RESPONSE TEXT NORMALIZER
# ============================================================

def extract_text(content):

    if isinstance(content, str):
        return content

    if isinstance(content, list):

        parts = []

        for item in content:

            if isinstance(item, str):
                parts.append(item)

            elif isinstance(item, dict):

                if "text" in item:
                    parts.append(
                        str(item["text"])
                    )

        return "".join(parts).strip()

    return str(content)


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="DStarix AI Assistant",
    version="1.0.0"
)

app.include_router(router)


# ============================================================
# TOOLS
# ============================================================

tools = [
    get_project_info,
    get_internship_phase
]

llm_with_tools = llm.bind_tools(tools)


# ============================================================
# MEMORY
# ============================================================

memory = ConversationMemory()


# ============================================================
# TOOL EXECUTION
# ============================================================

def run_tool(question):

    response = llm_with_tools.invoke(question)

    if not response.tool_calls:
        return None

    for tool_call in response.tool_calls:

        name = tool_call["name"]
        args = tool_call.get("args", {})

        if name == "get_project_info":

            return get_project_info.invoke(
                args
            )

        if name == "get_internship_phase":

            return get_internship_phase.invoke(
                args
            )

    return None


# ============================================================
# RAG PIPELINE
# ============================================================

def run_rag(
    question,
    include_sources=False
):

    # --------------------------------------------------------
    # 1. Transform query
    # --------------------------------------------------------

    search_query = transform_query(
        question
    )

    print("\nTransformed query:")
    print(search_query)


    # --------------------------------------------------------
    # 2. Retrieve documents
    # --------------------------------------------------------

    documents = retrieve_documents(
        search_query,
        k=5
    )

    print(
        f"\nRetrieved {len(documents)} documents."
    )


    # --------------------------------------------------------
    # 3. Rerank documents
    # --------------------------------------------------------

    reranked_documents = rerank_documents(
        question,
        documents,
        top_k=3
    )

    print(
        f"Reranked to "
        f"{len(reranked_documents)} documents."
    )


    # --------------------------------------------------------
    # 4. Create context
    # --------------------------------------------------------

    context = "\n\n".join(
        document.page_content
        for document in reranked_documents
    )


    # --------------------------------------------------------
    # 5. Conversation history
    # --------------------------------------------------------

    history = "\n".join(
        f"{message['role']}: {message['content']}"
        for message in memory.get_history()
    )


    # --------------------------------------------------------
    # 6. Create RAG prompt
    # --------------------------------------------------------

    prompt = RAG_PROMPT.format(
        context=context,
        question=question
    )

    prompt = f"""
Previous conversation:
{history}

{prompt}
"""


    # --------------------------------------------------------
    # 7. Generate answer
    # --------------------------------------------------------

    response = llm.invoke(
        prompt
    )

    answer = extract_text(
        response.content
    )


    # --------------------------------------------------------
    # 8. Save conversation
    # --------------------------------------------------------

    memory.add_message(
        "user",
        question
    )

    memory.add_message(
        "assistant",
        answer
    )


    # --------------------------------------------------------
    # 9. Extract sources
    # --------------------------------------------------------

    sources = []
    seen = set()

    for document in reranked_documents:

        metadata = document.metadata or {}


        # ----------------------------------------------------
        # Source filename
        # ----------------------------------------------------

        source = metadata.get(
            "source"
        )

        if source:

            source = Path(
                str(source)
            ).name

        else:

            source = "Unknown"


        # ----------------------------------------------------
        # Page number
        # ----------------------------------------------------

        page = metadata.get(
            "page"
        )

        if page is None:

            page = metadata.get(
                "page_number"
            )

        if page is None:

            page = metadata.get(
                "page_num"
            )


        # PyPDFLoader uses 0-based page indexing.
        # Convert it to human-readable 1-based page number.

        if page is not None:

            try:

                page = int(page) + 1

            except (
                ValueError,
                TypeError
            ):

                pass


        # ----------------------------------------------------
        # Remove duplicate source/page entries
        # ----------------------------------------------------

        source_key = (
            source,
            page
        )

        if source_key in seen:
            continue

        seen.add(
            source_key
        )

        sources.append(
            {
                "source": source,
                "page": page
            }
        )


    # --------------------------------------------------------
    # 10. Return response
    # --------------------------------------------------------

    if include_sources:

        return {
            "answer": answer,
            "sources": sources
        }

    return answer


# ============================================================
# MAIN ASSISTANT
# ============================================================

def run_assistant(
    question,
    include_sources=False
):

    try:

        q = question.lower().strip()


        # ----------------------------------------------------
        # Tool questions
        # ----------------------------------------------------

        tool_questions = [

            "purpose of the dstarix ai assistant",

            "purpose of dstarix ai assistant",

            "what is dstarix ai assistant",

            "what is the dstarix ai assistant",

            "about the dstarix ai assistant",

            "project information",

            "project info"

        ]


        use_tool = any(
            keyword in q
            for keyword in tool_questions
        )


        # ----------------------------------------------------
        # Tool execution
        # ----------------------------------------------------

        if use_tool:

            tool_result = run_tool(
                question
            )

            if tool_result is not None:

                prompt = f"""
Answer the user's question using the tool result.

User question:
{question}

Tool result:
{tool_result}

Give a clear and concise answer.
"""


                response = llm.invoke(
                    prompt
                )

                answer = extract_text(
                    response.content
                )


                # Save conversation

                memory.add_message(
                    "user",
                    question
                )

                memory.add_message(
                    "assistant",
                    answer
                )


                if include_sources:

                    return {
                        "answer": answer,
                        "sources": [
                            {
                                "source":
                                "DStarix AI Assistant Tool",

                                "page": None
                            }
                        ]
                    }


                return answer


        # ----------------------------------------------------
        # RAG execution
        # ----------------------------------------------------

        return run_rag(
            question,
            include_sources=include_sources
        )


    except Exception as e:

        import traceback

        print(
            "\n========== ASSISTANT ERROR =========="
        )

        print(
            str(e)
        )

        traceback.print_exc()

        print(
            "======================================\n"
        )

        raise