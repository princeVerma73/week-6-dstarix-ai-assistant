from langchain_core.tools import tool


@tool
def get_project_info():
    """Get information about the DStarix AI Assistant project."""

    return {
        "project": "DStarix AI Assistant",
        "purpose": "Production-ready AI assistant with RAG, memory, and tools"
    }


@tool
def get_internship_phase():
    """Get the two phases of the DStarix internship."""

    return {
        "phase_1": "Learning Phase",
        "phase_2": "Project Phase"
    }


if __name__ == "__main__":

    print(get_project_info.invoke({}))
    print(get_internship_phase.invoke({}))