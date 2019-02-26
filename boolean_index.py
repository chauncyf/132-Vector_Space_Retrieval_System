"""
boolean_index.py
author: Chenfeng Fan (fanc@brandeis.edu)
"""

import json
import nltk
import shelve
from nltk.stem.snowball import SnowballStemmer


def stemming_corpus(movie_corpus):
    """
    generate a stemmed corpus

    :param movie_corpus: movie corpus json file
    :return: stemmed corpus
    """
    stemmed_dict = {}
    stemmer = SnowballStemmer("english")

    with open(movie_corpus) as input_file:
        json_data = json.load(input_file)

    for index in json_data:
        data_dict = {'title': nltk.word_tokenize(' '.join(json_data[index]['Title'])),
                     'director': nltk.word_tokenize(' '.join(json_data[index]['Director'])),
                     'location': nltk.word_tokenize(' '.join(json_data[index]['Location'])),
                     'text': [stemmer.stem(word) for word in nltk.word_tokenize(json_data[index]['Text'])]}
        stemmed_dict[index] = data_dict

    with open('shelve/stemmed_dict.json', 'w') as output_file:
        json.dump(stemmed_dict, output_file)


def indexing(stemmed_corpus):
    """
    generate a postings list from corpus

    :param stemmed_corpus: stemmed corpus json file
    :return: postings list
    """
    text_index_dict = {}
    with open(stemmed_corpus) as input_file:
        json_data = json.load(input_file)

    for i in json_data:
        text = json_data[i]['text']
        for word in text:
            if word not in text_index_dict:
                text_index_dict[word] = [i]
            else:
                if i not in text_index_dict[word]:
                    text_index_dict[word].append(i)

    with open('shelve/posting_list.json', 'w') as output_file:
        json.dump(text_index_dict, output_file)


def json_to_shelve(json_file):
    """
    trans json file into shelve file

    :param json_file: json file
    :return: shelve file
    """
    with open(json_file) as f:
        json_data = json.load(f)

    with shelve.open('shelve/posting_list.db') as db:
        for key, value in json_data.items():
            db[key] = value


def generate_stop_word_shelf():
    """
    store stop words in a shelve file

    :return: shelf file
    """
    stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
                  "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its",
                  "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom",
                  "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being",
                  "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but",
                  "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about",
                  "against", "between", "into", "through", "during", "before", "after", "above", "below", "to",
                  "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then",
                  "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few",
                  "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so",
                  "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]

    with shelve.open('shelve/stop_word_list.db') as db:
        db['stop_word'] = stop_words


if __name__ == '__main__':
    generate_stop_word_shelf()
    stemming_corpus('corpus/film_corpus.json')
    indexing('shelve/stemmed_dict.json')
    json_to_shelve('shelve/posting_list.json')
