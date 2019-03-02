"""
boolean_search.py
author: Chenfeng Fan (fanc@brandeis.edu)

Students: Modify this file to include functions that implement 
Boolean search, snippet generation, and doc_data presentation.
"""

import json
import nltk
import shelve
from nltk.stem.snowball import SnowballStemmer


def intersect_list(index_dict):
    """
    do intersection for two lists

    :param index_dict: dict of indexes
    :return: intersected list
    """
    lists = [value for value in index_dict.values()]
    if len(lists) == 0:
        return []
    elif len(lists) == 1:
        return lists[0]
    intersected_list = lists[0]
    for list in lists:
        intersected_list = [value for value in intersected_list if value in list]
    return intersected_list


def get_inverted_index(word_list):
    """
    generate a inverted index list

    :param word_list: list of words to index
    :return: inverted index list
    """
    word_index = {}
    with shelve.open('static/posting_list.db') as f:
        for key, value in f.items():
            if key in word_list:
                word_index[key] = value
    return intersect_list(word_index)


def get_term_dict():
    """
    return a dict of terms

    :return: dict of terms
    """
    # f = shelve.open('static/posting_list.db')
    # return [key for key in f.keys()]
    with shelve.open('static/posting_list.db') as f:
        term_dict = [key for key in f.keys()]
    # with open('static/posting_list.json') as f:
    #     f = json.load(f)
    #     term_dict = [key for key in f.keys()]
    return term_dict


def get_stop_word_dict():
    """
    return a dict of stop words

    :return: dict of stop words
    """
    with shelve.open('static/stop_word_list.db') as f:
        word_dict = [word for word in f['stop_word']]
    return word_dict


def dummy_search(query):
    """Return a list of movie ids that match the query."""
    stemmer = SnowballStemmer("english")
    key_words = [stemmer.stem(word) for word in nltk.word_tokenize(query)]
    return get_inverted_index(key_words)


def dummy_movie_data(doc_id):
    """
    Return data fields for a movie.
    Your code should use the doc_id as the key to access the shelf entry for the movie doc_data.
    You can decide which fields to display, but include at least title and text.
    """
    with open('corpus/film_corpus.json') as f:
        json_data = json.load(f)
    return json_data.get(doc_id)


def dummy_movie_snippet(doc_id):
    """
    Return a snippet for the results page.
    Needs to include a title and a short description.
    Your snippet does not have to include any query terms, but you may want to think about implementing
    that feature. Consider the effect of normalization of index terms (e.g., stemming), which will affect
    the ease of matching query terms to words in the text.
    """
    movie_object = dummy_movie_data(doc_id)
    return doc_id, movie_object['Title'][0], '. '.join(movie_object['Text'].split('. ')[:3]) + '.'
