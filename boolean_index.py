import json
import nltk
import shelve
from nltk.stem.snowball import SnowballStemmer


def stemming_corpus(movie_corpus):
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

    with open('stemmed_dict.json', 'w') as output_file:
        json.dump(stemmed_dict, output_file)


def indexing(stemmed_corpus):
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

    with open('posting_list.json', 'w') as output_file:
        json.dump(text_index_dict, output_file)


def json_to_shelf(json_file):
    with open(json_file) as f:
        json_data = json.load(f)

    with shelve.open('posting_list.db') as db:
        for key, value in json_data.items():
            db[key] = value


if __name__ == '__main__':
    stemming_corpus('corpus/test_corpus_50.json')
    indexing('stemmed_dict.json')
    json_to_shelf('posting_list.json')
    # with shelve.open('posting_list.db') as f:
    #     for i, j in f.items():
    #         print(i, j)
