"""
boolean_search.py
author: 

Students: Modify this file to include functions that implement 
Boolean search, snippet generation, and doc_data presentation.
"""


def dummy_search(query):
    """Return a list of movie ids that match the query."""
    return range(1, 25)


def dummy_movie_data(doc_id):
    """
    Return data fields for a movie.
    Your code should use the doc_id as the key to access the shelf entry for the movie doc_data.
    You can decide which fields to display, but include at least title and text.
    """

    movie_object = {"title": " John goes to NYC",
                    "director": "John Doe",
                    "location": "New York City",
                    "text": "John heads to New York on the train..."
                    }
    return (movie_object)


def dummy_movie_snippet(doc_id):
    """
    Return a snippet for the results page.
    Needs to include a title and a short description.
    Your snippet does not have to include any query terms, but you may want to think about implementing
    that feature. Consider the effect of normalization of index terms (e.g., stemming), which will affect
    the ease of matching query terms to words in the text.
    """

    return (doc_id, "Movie title", "Place movie snippet here")
