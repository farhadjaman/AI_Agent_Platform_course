# book_lookup/tools.py

import requests


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
            "author_key": doc.get("author_key", [None])[0],
        })

    return {"query": query, "results": results}


def get_author_works(author_key: str, limit: int = 5) -> dict:
    """Retrieves a list of works by a specific author from the Open Library API.

    Args:
        author_key: The Open Library author identifier (for example, OL34184A for Frank Herbert).
        limit: The maximum number of works to return. Defaults to 5.

    Returns:
        A dictionary containing the author's name and a list of their works
        with titles and first publish years.
    """

    response = requests.get(
        f"https://openlibrary.org/authors/{author_key}/works.json",
        params={"limit": limit},
    )
    data = response.json()

    works = []
    for entry in data.get("entries", []):
        works.append({
            "title": entry.get("title"),
            "first_publish_year": entry.get("first_publish_date"),
        })

    return {"author_key": author_key, "works": works}