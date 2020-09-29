from scraper import Scraper as sc
# from bs4 import BeautifulSoup
# import requests

"""
# Scraping without the need for a browser using beautifulsoup
def scrapedClues():
  url = 'https://www.nytimes.com/crosswords/game/mini'
  arrClues = []
  soup = BeautifulSoup(requests.get(url).content, 'html.parser')
  # print(soup) 
  listObjects = soup.findAll('span', {'class' : 'Clue-text--3lZl7'})
  for obj in listObjects: arrClues.append(obj.string.strip())
  
  # debug
  # print(arrClues)
  return arrClues

returnedClues = scrapedClues()
for i in returnedClues : print(i)
"""

scraper_obj = sc()
scraper_obj.scrape_nwt()

