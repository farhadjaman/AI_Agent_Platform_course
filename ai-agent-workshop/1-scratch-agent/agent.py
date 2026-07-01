import os
import requests
from google import genai
from google.genai import types

# --- Tool function ---

def search_books(query: str, limit: int = 3) -> dict:
    """Searches for books using the Open Library API.

    Args:
        query: A search query such as a book title, author name, or topic.
        limit: The maximum number of results to return. Defaults to 3.

    Returns:
        A dictionary containing the search results with book titles, authors,
        and first publish years.
    """

    response = requests.get(
        "https://openlibrary.org/search.json",
        params={"q": query, "limit": limit},
    )
    data = response.json()

    results = []
    for doc in data.get("docs", []):
        results.append({
            "title": doc.get("title"),
            "author": doc.get("author_name", ["Unknown"])[0],
            "first_publish_year": doc.get("first_publish_year"),
            "edition_count": doc.get("edition_count"),
        })

    return {"query": query, "results": results}

# --- Tool definition for the LLM ---

tool_definition = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="search_books",
            description="Searches for books using the Open Library API. Use this to find books by title...",
            parameters={
                "type": "OBJECT",
                "properties": {
                    "query": {
                        "type": "STRING",
                        "description": "A search query such as a book title, author name, or topic."
                    },
                    "limit": {
                        "type": "INTEGER",
                        "description": "The maximum number of results to return. Defaults to 3."
                    }
                },
                "required": ["query"]
            }
        )
    ]
)
# --- Function registry ---

available_functions = {
    "search_books": search_books,
}


# --- The agent loop ---

def run_agent(client, user_input: str) -> str:
    """Runs the agent loop until the LLM returns a natural language response."""

    config = types.GenerateContentConfig(tools=[tool_definition])

    message_history = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_input)]
        )
    ]

    while True:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=message_history,
            config=config,
        )

        model_content = response.candidates[0].content
        message_history.append(model_content)

        first_part = model_content.parts[0]

        if first_part.text:
            return first_part.text

        if first_part.function_call:
            function_call = first_part.function_call
            function_name = function_call.name
            function_args = function_call.args

            print(f"  [Tool call] {function_name}({function_args})")

            function_result = available_functions[function_name](**function_args)

            print(f"  [Tool result] {function_result}")

            message_history.append(
                types.Content(
                    role="user",
                    parts=[types.Part.from_function_response(
                        name=function_name,
                        response={"result": function_result},
                    )]
                )
            )

# --- Run it ---

if __name__ == "__main__":
    client = genai.Client(
        vertexai=True,
        project=os.environ.get("GOOGLE_CLOUD_PROJECT", "gcpstudyhub-ai-agents-1"),
        location="us-central1",
    )

    answer = run_agent(client, "Tell me about the book Dune by Frank Herbert")
    print(f"\nAgent: {answer}")