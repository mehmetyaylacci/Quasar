# @authors:
# Burak Turksever
# Mehmet Yaylaci
# Eralp Kumbasar

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import json
import requests
from urllib import request
from bs4 import BeautifulSoup
import re
from bs4_scraper import Scraper_bs as sc_bs
import numpy as np
import string

'''
NLP class uses datamuse API and sources to find possible answers
that can be matched with the clues given in the crossword while
obeying the restrictions and the layout of the puzzle
'''
class NLP:
    '''
    Uses the datamuse API to scrape possible answers corresponding
    to the clues of the crossword puzzle
    '''
    def __init__(self):
        self.starting_url = "https://api.datamuse.com/words?"
        self.url_adds = ["ml=", "rel_bga=", "rel_bgb="]

    '''
    determines possible answers for the crossword puzzle by searching for the
    close neighbors of the clues in the network of datamuse search engine, the
    words that may relate to the clues of the puzzle
    '''
    def datamuse_close_neighs(self, clue, url_add):
        print("Finding close neighbors from the Datamuse API\n-------------")
        clue = clue.lower()
        clue = clue.replace(" ", "+")
        results = []

        lookup_url = self.starting_url + url_add + \
            clue + "&max=3"       # number can be changed
        response = request.urlopen(lookup_url)
        data = json.loads(response.read())
        for j in data:
            results.append(j["word"])
        print(results)
        return results

    '''
    purifies the clues by filtering the stopwords and punctuations before searching
    through the word engines to match the clues with possible answers for the puzzle
    '''
    def purify_clues(self, clues, lengths):
        purified_clues = []
        print("Purifying clues...\n-------------")
        for a_clue in clues:
            text = (a_clue[1].translate(str.maketrans('', '', string.punctuation))).lower()
            tokenized = word_tokenize(text)
            with open("stop_words.txt", "r") as f:
                stopwords = f.read().split("\n")
                stopwords_removed = [word for word in tokenized if not word in stopwords]
                stringified = ""
                for word in stopwords_removed:
                    stringified += word + " "
                purified_clues.append(stringified)
        return purified_clues

    # returns the clues and their lengths that are scraped from the puzzle
    def get_scraped_clues(self):
        print("Getting scraped clues from the scraper...\n-------------")
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
        print("Calculating clue lengths...\n-------------")
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

    '''
    The function initiates guessing by scraping the clues,
    storing the clues and creating guesses for the puzzle,
    while also assigning weights according to different lengths.
    it filters the initial list of guesses to obtain a final list.

    '''
    def initiate_guessing(self):
        print("Starting to make educated guesses...\n-------------")
        combo = self.get_scraped_clues()
        clues = combo[0]
        lens = combo[1]
        guesses = []
        purified_clues = self.purify_clues(clues, lens)
        final_g = []
        ct = 0
        for i in purified_clues:
            guesses.append(self.datamuse_close_neighs(i, self.url_adds[0]))

        for guess in guesses:
            temp = []
            for j in guess:
                print(j)
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
            print(max_obj)
        # print(rtr)
        return rtr