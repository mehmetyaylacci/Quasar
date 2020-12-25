from bs4 import BeautifulSoup
import requests
from selenium import webdriver 
import time

class Scraper_bs:
    # Constructor
    def __init__(self):
        url = "D:\codes\quasar\Quasar\index.html"
        self.url = url
        self.driver = webdriver.Chrome(executable_path=r"data/chromedriver.exe")
        
    '''
    # not working yet
    def autoAdd(filename):
        with open(filename ,'r') as file:
            links = []
            contents = file.read()
            soup = BeautifulSoup(contents, 'html.parser')
            buttons = soup.findAll('a', {'class':'btn btn-xs btn-info'})
            for obj in buttons:
                links.append(obj.get('href'))
            # print(links) debug
    '''

    # This function scrapes the clues of the puzzle.
    def scrape_puzzle(self):
        print("Scraping the puzzle...\n-------------")
        final_clues = []
        with open("index.html", 'r') as file:
            soup = BeautifulSoup(file.read(), 'html.parser')
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


    # This function scrapes the solutions of the puzzle
    def scrape_sols(self):
        print("Scraping solutions...\n-------------")
        final_answers = []
        soup = self.get_sol_page()
        whole = soup.find('g', {'data-group' : 'cells'})
        all_g = whole.findAll('g')
        for a_g in all_g:
            if len(a_g.findAll('text', {'class' : 'Cell-hidden--3xQI1'})) == 1:
                text_extract = a_g.findAll('text', {'class' : 'Cell-hidden--3xQI1'})
                final_answers.append(text_extract[0].get_text())
            elif len(a_g.findAll('text', {'class' : 'Cell-hidden--3xQI1'})) == 2:
                text_extract = a_g.findAll('text', {'class' : 'Cell-hidden--3xQI1'})
                final_answers.append(text_extract[1].get_text())
            else:
                final_answers.append(-1)
        self.driver.quit()
        print(final_answers)
        return final_answers


    # This function gets the solution page by clicking the necessary buttons.
    def get_sol_page(self):
        print("Getting the solution page...\n-------------")
        self.driver.get("index.html")

        self.driver.find_element_by_xpath("//span[text()='OK']").click()

        self.driver.find_element_by_xpath("//button[text()='reveal']").click()
        
        self.driver.find_elements_by_xpath("//a[text()='Puzzle']")[1].click()

        self.driver.find_element_by_xpath("//span[text()='Reveal']").click()
        
        self.driver.find_element_by_xpath("//span[@class='ModalBody-closeX--2Fmp7']").click()
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        return soup


    # Function to scrape the shape of the puzzle, which means this function returns
    # where the black tiles exist
    def scrape_puzzle_shape(self):
        print("Now scraping puzzle shape...\n-------------")
        with open("index.html", 'r') as file:
            soup = BeautifulSoup(file.read(), 'html.parser')
            final_shape = []
            whole = soup.find('g', {'data-group' : 'cells'})
            all_g = whole.findAll('g')
            for a_g in all_g:
                current_rect = a_g.find('rect')
                if 'Cell-block--1oNaD' in current_rect['class']:
                    final_shape.append(1)
                else:
                    final_shape.append(0)

        return final_shape
        

    # This function finds the numbers that are in the top left corners of the boxes
    def scrape_puzzle_numbers(self):
        print("Now scraping puzzle numbers...\n-------------")
        with open("index.html", 'r') as file:
            soup = BeautifulSoup(file.read(), 'html.parser')
            final_numbers = []
            whole = soup.find('g', {'data-group' : 'cells'})
            all_g = whole.findAll('g')
            for a_g in all_g:
                current_number = a_g.find('text', {'font-size' : '33.33'})
                if current_number != None:
                    final_numbers.append(int(current_number.get_text()))
                else:
                    final_numbers.append(-1)
        return final_numbers
