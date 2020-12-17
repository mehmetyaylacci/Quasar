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
        self.special_clues = []

    '''
    determines possible answers for the crossword puzzle by searching for the
    close neighbors of the clues in the network of datamuse search engine, the
    words that may relate to the clues of the puzzle
    '''

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

    '''
    purifies the clues by filtering the stopwords and punctuations before searching
    through the word engines to match the clues with possible answers for the puzzle
    '''

    def purify_clues(self, clues, lengths):
        purified_clues = []
        ct = 0
        for a_clue in clues:
            if "_" in a_clue[1]:
                ans = ""
                special = a_clue[1].split(" ")

                k = 0

                for i in range(len(special)):
                    if special[i] == "___":
                        ans = self.special_scraper(
                            special[i + 1].lower(), lengths[ct])
                        k = i + 1
                        break
                if ' ' in ans:
                    self.special_clues.append(
                        [ans.split(' ')[0].lower(), lengths[ct], special[k].lower()])
                else:
                    self.special_clues.append(
                        [ans.lower(), lengths[ct], special[k].lower()])
                # print(ans)
                # .translate(str.maketrans('', '', string.punctuation)
            else:
                text = (a_clue[1].translate(str.maketrans(
                    '', '', string.punctuation))).lower()
                tokenized = word_tokenize(text)
                with open("src/stop_words.txt", "r") as f:
                    stopwords = f.read().split("\n")
                    stopwords_removed = [
                        word for word in tokenized if not word in stopwords]
                    stringified = ""
                    for word in stopwords_removed:
                        stringified += word + " "
                    purified_clues.append(stringified)
                ct += 1
        return purified_clues

    # returns the clues and their lengths that are scraped from the puzzle
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

    '''
    The function initiates guessing by scraping the clues,
    storing the clues and creating guesses for the puzzle,
    while also assigning weights according to different lengths.
    it filters the initial list of guesses to obtain a final list.

    '''
    def initiate_guessing(self):
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
                if len(j) == lens[ct]:
                    temp.append([purified_clues[ct], j, 1])
                elif len(j) == lens[ct] - 1:
                    temp.append([purified_clues[ct], j + "s", 0.8])
                elif len(j) > lens[ct]:
                    temp.append([purified_clues[ct], j[:lens[ct]], 0.5])
                print(temp)

            final_g.append(temp)

        for s in self.special_clues:
            final_g.append([[s[0], s[2], 2]])

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

    # this function uses a site that searches Wikipedia with using regex method.
    # this site does not find answers from clues, this site is a helper tool
    # that helps us not to scrape all pages of Wikipedia
    def special_scraper(self, clue_after, clue_len):
        print("Searching Wikipedia with a regex to find ___ " + clue_after)
        url = "https://crosswordnexus.com/wiki/index.php?regex=" + "%3F" * clue_len + "+" + clue_after + \
            "&searchtype=simple&xmode=on&source=Wiki+%2B+Wiktionary&min_length=0&max_length=0&first=1\""
        resp = request.urlopen(url)
        soup = BeautifulSoup(resp, 'html.parser')
        div_find = soup.find('div', {'id': 'main'})
        return div_find.findAll('a')[0].string.strip()
