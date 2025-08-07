from google.adk.agents import Agent
from google.adk.tools import VertexAiSearchTool
from google.adk.tools import google_search  # Import the tool
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag
from dotenv import load_dotenv
from .prompt import return_instructions_root
import os

load_dotenv()

ask_vertex_retrieval = VertexAiRagRetrieval(
    name='retrieve_rag_documentation',
    description=(
        'Use this tool to retrieve documentation and reference materials for the question from the RAG corpus,'
    ),
    rag_resources=[
        rag.RagResource(
            # please fill in your own rag corpus
            # here is a sample rag corpus for testing purpose
            # e.g. projects/123/locations/us-central1/ragCorpora/456
            rag_corpus=os.environ.get("RAG_CORPUS")
        )
    ],
    similarity_top_k=10,
    vector_distance_threshold=0.6,
)

DATASTORE_ID = "projects/aisee-ahlab/locations/global/collections/default_collection/dataStores/datastore-poc_1753759382820"

root_agent = Agent(
   # A unique name for the agent.
   name="vision_agent",
   # The Large Language Model (LLM) that agent will use.
   # Please fill in the latest model id that supports live from
   # https://google.github.io/adk-docs/get-started/streaming/quickstart-streaming/#supported-models
   model="gemini-2.0-flash-exp",  # for example: model="gemini-2.0-flash-live-001" or model="gemini-2.0-flash-live-preview-04-09"
   #model = 'gemini-2.5-flash',
   # A short description of the agent's purpose.
   description="Agent to answer questions.",
   # Instructions to set the agent's behavior.
   instruction="""You are an AiSee agent that interacts with the user in a conversation.
    Your aim is to help person with vision disability. So you should be helpful to explain the vision you see to the person who use your service.
    Always introduce yourself that you are an AiSee vision agent that ready to explain the vision you see. Then make conversation with the user.
    Please ask if the user still interested in the conversation. If not say thank you and stop speaking until the user start speaking again.""",
   # Add google_search tool to perform grounding with Google search.
   tools=[google_search],
   #tools=[VertexAiSearchTool(data_store_id=DATASTORE_ID)]
)


# root_agent = Agent(
#     model='gemini-2.0-flash-exp',
#     name='vision_agent',
#     instruction=return_instructions_root(),
#     tools=[
#         ask_vertex_retrieval,
#     ]
# )