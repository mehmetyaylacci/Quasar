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
        print(len(all_clues_lists))
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

    # def scrape_sols(self):
