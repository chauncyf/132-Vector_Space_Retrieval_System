"""
boolean_search.py
author: 

Students: Modify this file to include functions that implement 
Boolean search, snippet generation, and doc_data presentation.
"""

import json
import nltk
import shelve
from nltk.stem.snowball import SnowballStemmer


def intersect_list(index_dict):
    lists = [value for value in index_dict.values()]
    if len(lists) <= 1:
        return lists
    intersected_list = lists[0]
    for list in lists:
        intersected_list = [value for value in intersected_list if value in list]
    return intersected_list


def get_inverted_index(word_list):
    word_index = {}
    with shelve.open('posting_list.db') as f:
        for key, value in f.items():
            if key in word_list:
                word_index[key] = value
    return intersect_list(word_index)


def get_term_dict():
    with shelve.open('posting_list.db') as f:
        keys = f.keys()
    return keys


def dummy_search(query):
    """Return a list of movie ids that match the query."""
    stemmer = SnowballStemmer("english")
    key_words = [stemmer.stem(word) for word in nltk.word_tokenize(query)]
    return get_inverted_index(key_words)
    # return range(1, 25)


def dummy_movie_data(doc_id):
    """
    Return data fields for a movie.
    Your code should use the doc_id as the key to access the shelf entry for the movie doc_data.
    You can decide which fields to display, but include at least title and text.
    """
    with open('corpus/film_corpus.json') as f:
        json_data = json.load(f)
    return json_data.get(doc_id)
    # movie_object = {"title": " John goes to NYC",
    #                 "director": "John Doe",
    #                 "location": "New York City",
    #                 "text": "John heads to New York on the train..."
    #                 }
    # return movie_object


def dummy_movie_snippet(doc_id):
    """
    Return a snippet for the results page.
    Needs to include a title and a short description.
    Your snippet does not have to include any query terms, but you may want to think about implementing
    that feature. Consider the effect of normalization of index terms (e.g., stemming), which will affect
    the ease of matching query terms to words in the text.
    """
    movie_object = dummy_movie_data(doc_id)
    return doc_id, movie_object['Title'][0], movie_object['Text'][:140]


if __name__ == '__main__':
    # print(dummy_search('good day right'))
    # print(dummy_movie_data('1'))
    # print(dummy_movie_snippet('555'))
    doc_ids = dummy_search('good day right')
    results = [dummy_movie_snippet(i) for i in doc_ids]
    print(results)
