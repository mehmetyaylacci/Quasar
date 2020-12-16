from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import json
from urllib import request
import re
from bs4_scraper import Scraper_bs as sc_bs
import numpy as np
import string
nltk.download('stopwords')

class NLP:
    def __init__(self):
        self.stopwords = stopwords
        self.starting_url = "https://api.datamuse.com/words?"
        self.url_adds = ["ml=", "rel_bga=", "rel_bgb="]
    
    def datamuse_close_neighs(self, clue, url_add, visited = []):
        clue = clue.lower()
        clue = clue.replace(" ", "+")
        results = []        
        lookup_url = self.starting_url + url_add + clue + "&max=999"       # number can be changed
        response = request.urlopen(lookup_url)
        data = json.loads(response.read())
        for j in data: 
            if j["word"] not in visited:
                results.append(j["word"])
        return results

    def datamuse_loop(self, clue_len, known_re, next_iteration, visited = [], depth = 0, matched = []):
        if next_iteration == [] or depth >= 10:
            return matched

        temp = next_iteration.pop(0)
        visited_temp = []

        # print(temp)
        for i in self.url_adds:
            close_neigh = self.datamuse_close_neighs(temp, i, visited)

            for word_cn in close_neigh:
                # if len(word_cn) == clue_len and re.match(known_re, word_cn):
                if re.match(known_re, word_cn):
                    matched.append(word_cn[:clue_len])
                if len(word_cn) == clue_len - 1:
                    matched.append(word_cn + "s")

                visited_temp.append(word_cn)

            for j in range(len(close_neigh)):
                if j <= 20 and close_neigh[j] not in visited:
                    next_iteration.append(close_neigh[j])     # number can be changed
                    # visited.append(word_cn)
                else:
                    break
        
        for i in visited_temp:
            visited.append(i)

        return self.datamuse_loop(clue_len, known_re, next_iteration, visited, depth + 1, matched)


    def get_scraped_clues(self):
        scraper_obj = sc_bs()
        self.clues = scraper_obj.scrape_puzzle()
        self.shape = scraper_obj.scrape_puzzle_shape()
        clue_lengths = self.clue_lengths(self.shape, len(self.clues))
        return [self.clues, clue_lengths]

    def clue_lengths(self, shape_clues, num_clues):
        rs = np.reshape(shape_clues, (5,5))
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

    def send_clues(self):
        combo = self.get_scraped_clues()
        clues_temp = self.purify_clues(combo[0])
        clue_lengths = combo[1]
        ct = 0
        for a_clue in clues_temp:
            print(a_clue)
            temp = self.datamuse_loop(next_iteration = [a_clue[1]], clue_len = clue_lengths[ct], known_re = "")
            self.clues[ct][0] = temp
            ct += 1
        
        # print(self.clues)
        return self.clues
        

    def purify_clues(self, clues):
        purified_clues = []
        for a_clue in clues:
            text = (a_clue[1].translate(str.maketrans('', '', string.punctuation))).lower()
            tokenized = word_tokenize(text)
            stopwords_removed = [word for word in tokenized if not word in stopwords.words()]
            stringified = ""
            for word in stopwords_removed:
                stringified += word + " "
            purified_clues.append(stringified)
        return purified_clues

    def fill_first(self):

        answers = []
        for i in self.clues:
            check = i[0][0]
            answers.append(check)
            # print(check)
        return answers

'''
[0, 0, 0, 1, 1]
[0, 0, 0, 0, 1]
[0, 0, 0, 0, 0]
[0, 0, 0, 0, 0]
[0, 0, 0, 0, 0]
'''




def test():
    nlp = NLP()
    nlp.send_clues()
    print(nlp.fill_first())
    # print(nlp.get_scraped_clues())
    # print(nlp.send_clues())
    # answer = nlp.datamuse_loop(next_iteration = ["Salad green peppery taste"], clue_len = 5, known_re = some_regex)

    # print(answer)
    # print("cress" in answer)
    

test()

# lookup = "minus+plus"
# url = "https://api.datamuse.com/words?rel_gen=" + lookup + "&max=999"
# response = request.urlopen(url)
# data = json.loads(response.read())

# res = []

# for i in data:
#   res.append(i["word"])
#   if i["word"] == "maths":
#     print("siktik")

# print(res)

# def datamuse_loop(array):

