"""
vs_index.py
author: Chenfeng Fan (fanc@brandeis.edu)
"""

import json
import math
import nltk
import shelve
import datetime
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


def generage_postings_list(stemmed_corpus):
    """
    generate a postings list from corpus

    :param stemmed_corpus: stemmed corpus json file
    :return: postings list
    """
    text_index_dict = {}
    with open(stemmed_corpus) as input_file:
        stemmed_corpus = json.load(input_file)

    for i in stemmed_corpus:
        text = stemmed_corpus[i]['text']
        for word in text:
            if word not in text_index_dict:
                text_index_dict[word] = [i]
            else:
                if i not in text_index_dict[word]:
                    text_index_dict[word].append(i)

    with open('shelve/postings_list.json', 'w') as output_file:
        json.dump(text_index_dict, output_file)


def cal_tf(stemmed_corpus):
    """
    The term frequency tft,d of term t in document d is
    defined as the number of times that t occurs in d.
    :param stemmed_corpus:
    :return:
    """
    tf_dict = {}
    with open(stemmed_corpus) as input_file:
        stemmed_corpus = json.load(input_file)
    for i in stemmed_corpus:
        text = stemmed_corpus[i]['text']
        for word in text:
            if word not in tf_dict:
                tf_dict[word] = {i: 1}
            elif tf_dict[word].get(i):
                tf_dict[word][i] += 1
            else:
                tf_dict[word][i] = 1
    with open('shelve/tf_dict.json', 'w') as output_file:
        json.dump(tf_dict, output_file)


def cal_tf_idf(tf_dict, corups):
    """
    W(t,d) =log(1+tf(t,d)) ́log10(N/df(t))
    :param stemmed_corpus:
    :return:
    """
    tf_idf_dict = {}
    with open(corups) as f:
        N = len(json.load(f))
    with open(tf_dict) as f:
        tf_dict = json.load(f)
    for key in tf_dict:
        tf_idf_dict[key] = {}
        for index in tf_dict[key]:
            tf_idf_dict[key][index] = math.log(1 + tf_dict[key][index]) * math.log10(N / len(tf_dict[key]))
    with open('shelve/tf_idf_dict.json', 'w') as output_file:
        json.dump(tf_idf_dict, output_file)


def tf_idf_normalization(tf_idf_dict, cos_norm_list, stemmed_dict):
    tf_idf_norm_dict = {}
    with open(stemmed_dict) as f:
        json_data = json.load(f)
    with open(tf_idf_dict) as f:
        tf_idf_dict = json.load(f)
    with open(cos_norm_list) as f:
        cos_norm_list = json.load(f)
    for index in json_data:
        text = json_data[index]['text']
        for term in text:
            if term not in tf_idf_norm_dict:
                tf_idf_norm_dict[term] = {}
            tf_idf_norm_dict[term][index] = tf_idf_dict[term][index] / cos_norm_list[index]
    with open('shelve/tf_idf_norm_dict.json', 'w') as output_file:
        json.dump(tf_idf_norm_dict, output_file)


def cal_cos_norm(tf_idf_dict, stemmed_dict, stop_word_list):
    with open(stemmed_dict) as f:
        stemmed_dict = json.load(f)
    with open(tf_idf_dict) as f:
        tf_idf_dict = json.load(f)
    with shelve.open(stop_word_list) as f:
        stop_word_list = f['stop_word']

    cos_norm_list = {}
    for index in stemmed_dict:
        text = stemmed_dict[index]['text']
        weight_sum = 0
        for term in text:
            if term not in stop_word_list:
                weight_sum += tf_idf_dict[term][index] ** 2
        cos_norm_list[index] = math.sqrt(weight_sum)
    with open('shelve/cos_norm_list.json', 'w') as output_file:
        json.dump(cos_norm_list, output_file)


def cal_cos_score(query, postings_list, tf_idf_dict, tf_idf_norm_dict, cos_norm_list):
    scores = {}
    query_terms = [SnowballStemmer("english").stem(word) for word in nltk.word_tokenize(query.strip())]
    for term in query_terms:
        term_postings_list = postings_list[term]
        for index in term_postings_list:
            if index not in scores:
                scores[index] = 0
            scores[index] += tf_idf_norm_dict[term][index] * tf_idf_dict[term][index]
    for index in scores:
        scores[index] /= cos_norm_list[index]
    return scores


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

    with shelve.open('shelve/shelve.db') as db:
        db['stop_word'] = stop_words


def json_into_shelve(json_file, key_name):
    """
    trans json file into shelve file

    :param key_name:
    :param json_file: json file
    :return: shelve file
    """
    with open(json_file) as f:
        json_data = json.load(f)
    with shelve.open('shelve/shelve.db') as db:
        db[key_name] = json_data
        # for key, value in json_data.items():
        #     db[key] = value


def generate_shelve_files():
    print('> Loading stop words..')
    generate_stop_word_shelf()
    print('> Stemming corpus..')
    stemming_corpus('corpus/films_corpus.json')
    print('> Generating postings list..')
    generage_postings_list('shelve/stemmed_dict.json')
    print('> Calculating term frequency..')
    cal_tf('shelve/stemmed_dict.json')
    print('> Calculating tf-idf..')
    cal_tf_idf('shelve/tf_dict.json', 'corpus/films_corpus.json')
    print('> Calculating document vector lengths..')
    cal_cos_norm('shelve/tf_idf_dict.json', 'shelve/stemmed_dict.json', 'shelve/stop_word_list.db')
    print('> Calculating normalized tf-idf..')
    tf_idf_normalization('shelve/tf_idf_dict.json', 'shelve/cos_norm_list.json', 'shelve/stemmed_dict.json')
    print('Almost done...')
    json_into_shelve('corpus/films_corpus.json', 'films_corpus')
    print('5')
    json_into_shelve('shelve/stemmed_dict.json', 'stemmed_dict')
    print('4')
    json_into_shelve('shelve/postings_list.json', 'postings_list')
    print('3')
    json_into_shelve('shelve/tf_idf_dict.json', 'tf_idf_dict')
    print('2')
    json_into_shelve('shelve/tf_idf_norm_dict.json', 'tf_idf_norm_dict')
    print('1')
    json_into_shelve('shelve/cos_norm_list.json', 'cos_norm_list')
    print('Done')


if __name__ == '__main__':
    time = datetime.datetime.now()
    print('Start generating shelve files...')
    generate_shelve_files()
    print('Total time cost: ', datetime.datetime.now() - time)
