# Scraping work is done here.

from selenium import webdriver

class Scraper:
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=r"../data/chromedriver.exe")
    
    def scrape_nwt(self):
        self.driver.get("https://www.nytimes.com/crosswords/game/mini")
        self.driver.find_element_by_xpath("//span[text()='OK']").click()
        
        listing_clues = self.driver.find_elements_by_xpath("//span[@class='Clue-text--3lZl7']")
        
        for texts in listing_clues:
            print(texts.text)