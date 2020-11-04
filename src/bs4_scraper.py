from bs4 import BeautifulSoup
import requests
from selenium import webdriver 
import time

class Scraper_bs:

    def __init__(self):
        url = "https://www.nytimes.com/crosswords/game/mini"
        self.url = url
        # webdriver path
        self.driver = webdriver.Chrome(
            executable_path=r"./data/chromedriver.exe")

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

    # def scrape_sols(self):
    #     final_answers = []
    #     completed_url = self.url + "?playaction=reveal-puzzle"
    #     # here we request the answer page from the website
    #     soup = BeautifulSoup(requests.get(completed_url).content, 'html.parser')
    #     # here we parse the website
    #     find_g = soup.find('g', {'data-group' : 'cells'})
    #     all_answers = find_g.findAll('g')
    #     print(all_answers)
    #     for an_answer in all_answers:
    #         all_text = an_answer.findAll('text')
    #         for a_text in all_text:
    #             print(a_text.find('text', {'class' : 'Cell-hidden--3xQI1'}))
    #     return final_answers

    # mehmet's solution
    def scrape_sols(self):
        self.driver.get("https://www.nytimes.com/crosswords/game/mini")
        # click on first question
        self.driver.find_element_by_xpath("//span[text()='OK']").click()
        # click reveal
        self.driver.find_element_by_xpath("//button[text()='reveal']").click()
        
        time.sleep(2)

        # click reveal
        self.driver.find_elements_by_xpath("//a[text()='Puzzle']")[1].click()

        time.sleep(2)

        # click reveal
        self.driver.find_element_by_xpath("//span[text()='Reveal']").click()
        
        time.sleep(2)
        
        # click close
        self.driver.find_element_by_xpath(
            "//span[@class='ModalBody-closeX--2Fmp7']").click()
        
        html = driver.page_source
        soup = BeautifulSoup(html)

        return soup
        
    def scrape_puzzle_shape(self):
        final_shape = []
        soup = BeautifulSoup(requests.get(self.url).content, 'html.parser')
        whole = soup.find('g', {'data-group' : 'cells'})
        all_g = whole.findAll('g')
        for a_g in all_g:
            current_rect = a_g.find('rect')
            if 'Cell-block--1oNaD' in current_rect['class']:
                final_shape.append(1)
            else:
                final_shape.append(0)

        return final_shape

    def scrape_puzzle_numbers(self):
        final_numbers = []
        soup = BeautifulSoup(requests.get(self.url).content, 'html.parser')
        whole = soup.find('g', {'data-group' : 'cells'})
        all_g = whole.findAll('g')
        for a_g in all_g:
            current_number = a_g.find('text', {'font-size' : '33.33'})
            if current_number != None:
                final_numbers.append(int(current_number.get_text()))
            else:
                final_numbers.append(-1)
        return final_numbers

test = Scraper_bs()
test.scrape_sols()
