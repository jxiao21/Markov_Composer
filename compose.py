import os
import re
import string
import random
from graph import Graph, Vertex

def get_words_from_text(text_path):
        with open(text_path, 'r') as f:
            text = f.read()

            # remove [text in here for songs]
            text = re.sub(r'\[(.+)\]', ' ', text)

            text = ' '.join(text.split()) # turn all whitespace into single space
            text = text.lower()
            # remove punctuation
            text = text.translate(str.maketrans('', '', string.punctuation))

        words = text.split()
        return words

def make_graph(words):
    g = Graph()
    previous_word = None

    # for every word, see if in graph and add if not
    for word in words:
        word_vertex = g.get_vertex(word)
    # if there was previous word, add edge if not already existing
    # in graph, otherwise increment weight by 1
        if previous_word:
            previous_word.increment_edge(word_vertex)
    # set our word to rpevious word and iterate
        previous_word = word_vertex

    # good place to generate probability mappings before composing
    g.generate_probability_mappings()

    return g


def compose(g, words, length=50):
    composition = []
    word = g.get_vertex(random.choice(words))
    for _ in range(length):
        composition.append(word.value)
        word = g.get_next_word(word)

    return composition

# Steps:
def main(artist):
    # get words from text
    words = get_words_from_text('texts/hp_sorcerer_stone.txt')

    # for song lyrics
    words = []
    for song_file in os.listdir(f'songs/{artist}'):
        if song_file == '.DS_Store':
            continue
        song_words = get_words_from_text(f'songs/{artist}/{song_file}')
        words.extend(song_words)

    # make graph using those words
    g = make_graph(words)

    # get next word for x number of words
    composition = compose(g, words, 100)

    # show the user
    return ' '.join(composition)

if __name__ == '__main__':
    print(main())