from google.adk.agents import LlmAgent
from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.tool_context import ToolContext
from app.core.config import settings
from app.video_pipeline_app.root_agent.sub_agents.domain_concept_parallel_agent.concept_writer_agent.schema import ConceptWriterOutput, Concept


# -----------------------------------------------------------
# Utility: Filter concept from {concept_writer_output}
# -----------------------------------------------------------

async def select_concept(concepts_output: dict, concept_name: str, tool_context: ToolContext) -> dict:
    """
    Human-in-the-loop concept selection.
    - Always requires human confirmation.
    - First call: show list of concepts + ask human to pick one.
    - Second call: read ToolConfirmation and return the selected concept.
    """

    print("------------- select_concept invoked -------------")
    print("invocation_id:", tool_context.invocation_id)
    print("concept_name:", concept_name)
    print("---------------------------------------------------")

    confirmation = tool_context.tool_confirmation

    # ------------------------------------------------
    # CASE A — First call: Ask human which concept to pick
    # ------------------------------------------------
    if not confirmation:
        concept_names = [c.get("Concept_Name") for c in concepts_output.get("concepts", [])]

        tool_context.request_confirmation(
            hint=(
                "Please select ONE concept.\n"
                "Available Concept Names:\n"
                f"{concept_names}\n\n"
                "Respond with a FunctionResponse containing ToolConfirmation like:\n"
                "{ 'concept_name': 'YourSelectedConcept' }"
            ),
            payload={"concept_name": None}
        )

        return {
            "status": "awaiting_selection",
            "available_concepts": concept_names,
            "message": (
                "Please pick ONE concept from available_concepts using ToolConfirmation."
            )
        }

    # ------------------------------------------------
    # CASE B — Second call: Human has selected a concept
    # ------------------------------------------------
    selected_name = confirmation.payload.get("concept_name")

    # Locate concept
    concepts = concepts_output.get("concepts", [])
    selected_concept = next(
        (c for c in concepts if c.get("Concept_Name") == selected_name),
        None
    )

    return {
        "status": "selected",
        "requested_concept_name": selected_name,
        "selected_concept": selected_concept,
        "message": (
            f"Concept '{selected_name}' successfully selected."
            if selected_concept
            else f"Concept '{selected_name}' not found in list."
        )
    }



# -----------------------------------------------------------
# ROOT AGENT
# -----------------------------------------------------------

concept_selector_agent = LlmAgent(
    model=settings.google_model_name,
    name="concept_selector_agent",
    instruction="Call the select_concept tool with parameters {concept_writer_output} .You may select the most suitable Concept_Name on your own.",
#     instruction="""
# You MUST NOT choose or guess any Concept_Name yourself.

# Your ONLY job is to:
# 1. Call the `select_concept` tool with parameters {concept_writer_output}.
# 2. Pass through whatever concept_name value is given by the user or tool.
# 3. NEVER invent or select a concept on your own.
# 4. If the user has not provided a concept_name, still call the tool with concept_name="".
# 5. The HUMAN will choose the concept via ToolConfirmation.

# STRICT RULE:
# - Do NOT infer, guess, or assume a Concept_Name.
# - Do NOT pick a concept yourself.
# """,
    # tools=[FunctionTool(select_concept)],
    output_key="concept_selector_output",
    output_schema=Concept,
    input_schema=ConceptWriterOutput
)
