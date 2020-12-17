from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import json
from urllib import request
import re
from bs4_scraper import Scraper_bs as sc_bs
import numpy as np
import string


class NLP:
    def __init__(self):
        self.starting_url = "https://api.datamuse.com/words?"
        self.url_adds = ["ml=", "rel_bga=", "rel_bgb="]

    def datamuse_close_neighs(self, clue, url_add):
        clue = clue.lower()
        clue = clue.replace(" ", "+")
        results = []
        lookup_url = self.starting_url + url_add + \
            clue + "&max=3"       # number can be changed
        response = request.urlopen(lookup_url)
        data = json.loads(response.read())
        for j in data:
            results.append(j["word"])
        return results

    def purify_clues(self, clues):
        purified_clues = []
        for a_clue in clues:
            text = (a_clue[1].translate(str.maketrans(
                '', '', string.punctuation))).lower()
            tokenized = word_tokenize(text)
            with open("stop_words.txt", "r") as f:
                stopwords = f.read().split("\n")
                stopwords_removed = [
                    word for word in tokenized if not word in stopwords]
                stringified = ""
                for word in stopwords_removed:
                    stringified += word + " "
                purified_clues.append(stringified)
        return purified_clues

    def get_scraped_clues(self):
        scraper_obj = sc_bs()
        clues = scraper_obj.scrape_puzzle()
        self.shape = scraper_obj.scrape_puzzle_shape()
        clue_lengths = self.clue_lengths(self.shape, len(clues))
        return [clues, clue_lengths]

    '''
    the function returns the length of the clues given in the
    puzzle according to the shape of the clues, creating a matrix of 
    5x5 and by checking 
    '''
    def clue_lengths(self, shape_clues, num_clues):
        rs = np.reshape(shape_clues, (5, 5))
        lens = [0] * num_clues
        ct = 0
        for i in range(5):
            for j in range(5):
                if rs[i][j] == 0:
                    lens[ct] += 1
            ct += 1
        for i in range(5):
            for j in range(5):
                if rs[j][i] == 0:
                    lens[ct] += 1
            ct += 1
        return lens

    def initiate_guessing(self):
        combo = self.get_scraped_clues()
        clues = combo[0]
        lens = combo[1]
        guesses = []
        purified_clues = self.purify_clues(clues)
        final_g = []
        ct = 0
        for i in purified_clues:
            guesses.append(self.datamuse_close_neighs(i, self.url_adds[0]))

        for guess in guesses:
            temp = []
            for j in guess:
                if len(j) == lens[ct]:
                    temp.append([purified_clues[ct], j, 1])
                elif len(j) == lens[ct] - 1:
                    temp.append([purified_clues[ct], j + "s", 0.8])
                elif len(j) > lens[ct]:
                    temp.append([purified_clues[ct], j[:lens[ct]], 0.5])
            final_g.append(temp)
            ct += 1

        max_val = 0
        rtr = []
        for i in final_g:
            for j in i:
                if j[2] > max_val:
                    max_obj = j
                    max_val = j[2]
            if max_obj not in rtr:
                rtr.append(max_obj)
            max_val = 0
        return rtr
