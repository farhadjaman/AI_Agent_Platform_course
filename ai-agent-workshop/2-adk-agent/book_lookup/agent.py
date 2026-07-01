# book_lookup/agent.py

from google.adk.agents import Agent
from tools import search_books, get_author_works

root_agent = Agent(
    model="gemini-2.5-flash",
    name="book_lookup_agent",
    instruction="You help users find information about books and authors. Use search_books to find books by title, author, or topic. Use get_author_works when the user wants to see more books by a specific author. When reporting results, always mention the first publish year.",
    tools=[search_books, get_author_works],
)