"""
boolean_search.py
author: Chenfeng Fan (fanc@brandeis.edu)
"""

import json
import nltk
import heapq
import shelve
from nltk.stem.snowball import SnowballStemmer


def get_dicts():
    try:
        with shelve.open('shelve/posting_list.db') as f:
            postings_list = dict(f)
            term_dict = list(f.keys())
        with shelve.open('shelve/stop_word_list.db') as f:
            stop_word_list = [word for word in f['stop_word']]

        with shelve.open('shelve/tf_idf_dict.db') as f:
            tf_idf_dict = dict(f)
        with open('shelve/tf_idf_dict.json') as f:
            tf_idf_dict = json.load(f)
        with open('shelve/tf_idf_norm_dict.json') as f:
            tf_idf_norm_dict = json.load(f)
        with open('shelve/cos_norm_list.json') as f:
            cos_norm_list = json.load(f)

        return term_dict, postings_list, stop_word_list, tf_idf_dict, tf_idf_norm_dict, cos_norm_list
    except:
        print('shelve file open failed')
        exit()


def get_shelve():
    return


def get_corpus():
    with open('corpus/films_corpus.json') as f:
        films_corpus = json.load(f)
    return films_corpus


def process_query_string(query, shelve_file):
    query_terms = []
    skipped_terms = []
    unknown_terms = []
    for term in [SnowballStemmer("english").stem(word) for word in nltk.word_tokenize(query)]:
        if term not in list(shelve_file['postings_list'].keys()):
            unknown_terms.append(term)
        elif term in shelve_file['stop_word']:
            skipped_terms.append(term)
        else:
            query_terms.append(term)
    return query_terms, skipped_terms, unknown_terms


def cal_cos_score(query_terms, result_index, shelve_file):
    scores = {}
    for term in query_terms:
        term_postings_list = shelve_file['postings_list'][term]
        for index in term_postings_list:
            if index not in scores:
                scores[index] = 0
            scores[index] += shelve_file['tf_idf_norm_dict'][term][index] * shelve_file['tf_idf_dict'][term][index]
    for index in scores:
        scores[index] /= shelve_file['cos_norm_list'][index]

    largest_score = heapq.nlargest(result_index * 10, scores.items(), key=lambda x: x[1])
    return largest_score[(result_index - 1) * 10: result_index * 10], len(scores)


def dummy_search(query, result_index, shelve_file):
    """Return a list of movie ids that match the query."""
    query_terms, skipped_terms, unknown_terms = process_query_string(query, shelve_file)
    # movie_ids, num_hits = cal_cos_score(query_terms, result_index, postings_list, tf_idf_dict, tf_idf_norm_dict,
    #                                     cos_norm_list)
    movie_ids, num_hits = cal_cos_score(query_terms, result_index, shelve_file)
    return movie_ids, num_hits, skipped_terms, unknown_terms


def dummy_movie_data(doc_id, shelve_file):
    """
    Return data fields for a movie.
    Your code should use the doc_id as the key to access the shelf entry for the movie doc_data.
    You can decide which fields to display, but include at least title and text.
    """
    return shelve_file['films_corpus'].get(doc_id)


def dummy_movie_snippet(doc, shelve_file):
    """
    Return a snippet for the results page.
    Needs to include a title and a short description.
    Your snippet does not have to include any query terms, but you may want to think about implementing
    that feature. Consider the effect of normalization of index terms (e.g., stemming), which will affect
    the ease of matching query terms to words in the text.
    """
    movie_object = dummy_movie_data(doc[0], shelve_file)
    return doc[0], round(doc[1], 5), movie_object['Title'][0], '. '.join(movie_object['Text'].split('. ')[:3]) + '.'


# preload dict files
# term_dict, postings_list, stop_word_list, tf_idf_dict, tf_idf_norm_dict, cos_norm_list = get_dicts()
# films_corpus = get_corpus()
