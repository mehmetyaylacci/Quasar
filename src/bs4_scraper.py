from bs4 import BeautifulSoup
import requests

class Scraper_bs:

    def __init__(self):
        url = "https://www.nytimes.com/crosswords/game/mini"
        self.url = url

    def scrape_puzzle(self):
        final_clues = []
        soup = BeautifulSoup(requests.get(self.url).content, 'html.parser')
        all_clues_lists = soup.findAll('ol', {'class' : 'ClueList-list--2dD5-'})
        for i in range(len(all_clues_lists)):
            seperated = all_clues_lists[i].findAll('li', {'class' : 'Clue-li--1JoPu'})
            for a_clue in seperated:
                number = a_clue.find('span', {'class': 'Clue-label--2IdMY'}).string.strip()
                ext_clue = a_clue.find('span', {'class' : 'Clue-text--3lZl7'}).string.strip()
                if i == 0:
                    final_clues.append([number, ext_clue, 'A'])
                else:
                    final_clues.append([number, ext_clue, 'D'])
        return final_clues

    def scrape_sols(self):
        final_answers = []
        completed_url = "https://www.nytimes.com/crosswords/game/mini?playaction=reveal-puzzle"
        # here we request the answer page from the website
        soup = BeautifulSoup(requests.get(completed_url).content, 'html.parser')
        # here we parse the website
        find_g = soup.find('g', {'data-group' : 'cells'})
        all_answers = find_g.findAll('g')
        print(all_answers)
        for an_answer in all_answers:
            all_text = an_answer.findAll('text')
            for a_text in all_text:
                print(a_text.find('text', {'class' : 'Cell-hidden--3xQI1'}))
        return final_answers
