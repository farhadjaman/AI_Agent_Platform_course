import os

from google.adk.agents import LlmAgent
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag

PROJECT_ID = os.environ["PROJECT_ID"]
LOCATION = os.environ["LOCATION"]
CORPUS_ID = os.environ["CORPUS_ID"]
CORPUS_NAME = f"projects/{PROJECT_ID}/locations/{LOCATION}/ragCorpora/{CORPUS_ID}"

alphabet_search = VertexAiRagRetrieval(
    name="alphabet_investor_search",
    description=(
        "Search Alphabet's investor filings (10-Ks, earnings releases) "
        "for financial data, segment performance, and strategy commentary. "
        "Use this tool whenever the user asks about Alphabet's revenue, "
        "growth, segments, or any quantitative business question."
    ),
    rag_resources=[rag.RagResource(rag_corpus=CORPUS_NAME)],
    similarity_top_k=20,
    vector_distance_threshold=0.6,
)

root_agent = LlmAgent(
    model="gemini-3.5-flash",
    name="alphabet_analyst",
    description=(
        "Analyst that answers questions about Alphabet's financial filings."
    ),
    instruction=(
        "You are a helpful analyst answering questions about Alphabet's "
        "investor filings. Always use the alphabet_investor_search tool "
        "to find relevant information before answering. "
        "When you cite a fact, mention the source document (e.g. "
        "'according to the Q3 2022 earnings release'). "
        "If the search returns no relevant results, or if the retrieved "
        "chunks do not contain information that answers the user's question, "
        "say so explicitly. Do not guess. Do not make up numbers. "
        "It is better to say 'the filings I have access to do not cover that' "
        "than to invent an answer."
    ),
    tools=[alphabet_search],
)