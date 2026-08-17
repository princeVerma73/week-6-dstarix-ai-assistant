from fastapi import FastAPI
from api.routes import router
app = FastAPI(
    title="DStarix AI Assistant",
    version="1.0.0"
)
app.include_router(router)

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

tools = [
    get_project_info,
    get_internship_phase
]

llm_with_tools = llm.bind_tools(tools)

memory = ConversationMemory()


def run_tool(question):

    response = llm_with_tools.invoke(question)

    if not response.tool_calls:
        return None

    for tool_call in response.tool_calls:

        if tool_call["name"] == "get_project_info":
            return get_project_info.invoke(
                tool_call["args"]
            )

        if tool_call["name"] == "get_internship_phase":
            return get_internship_phase.invoke(
                tool_call["args"]
            )

    return None


def run_rag(question):

    # Step 1: Transform query
    search_query = transform_query(question)

    print("\nTransformed query:")
    print(search_query)

    # Step 2: Retrieve documents
    documents = retrieve_documents(
        search_query,
        k=5
    )

    print(f"\nRetrieved {len(documents)} documents.")

    # Step 3: Rerank documents
    reranked_documents = rerank_documents(
        question,
        documents,
        top_k=3
    )

    print(
        f"Reranked to {len(reranked_documents)} documents."
    )

    # Step 4: Create context
    context = "\n\n".join(
        document.page_content
        for document in reranked_documents
    )

    # Step 5: Get conversation history
    history = "\n".join(
        f"{message['role']}: {message['content']}"
        for message in memory.get_history()
    )

    # Step 6: Create RAG prompt
    prompt = RAG_PROMPT.format(
        context=context,
        question=question
    )

    prompt = f"""
Previous conversation:
{history}

{prompt}
"""
    # Step 7: Generate answer
    response = llm.invoke(prompt)
    answer = response.content
    # Step 8: Save conversation
    memory.add_message(
        "user",
        question
    )
    memory.add_message(
        "assistant",
        answer
    )
    return answer


def run_assistant(question):
    try:
        # Step 1: Check whether a tool is needed
        tool_result = run_tool(question)

        if tool_result is not None:

            prompt = f"""
Answer the user's question using the tool result.

User question:
{question}

Tool result:
{tool_result}

Give a clear and concise answer.
"""
            response = llm.invoke(prompt)
            answer = response.content
            memory.add_message(
                "user",
                question
            )
            memory.add_message(
                "assistant",
                answer
            )
            return answer
        # Step 2: Use RAG
        return run_rag(question)
    except Exception as e:
        print(f"Assistant error: {e}")
        return (
            "Sorry, I couldn't process your request right now. "
            "Please try again later."
        )