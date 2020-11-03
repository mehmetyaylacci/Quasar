# from scraper import Scraper as sc
from bs4_scraper import Scraper_bs as sc_bs

# scraper_obj = sc()
# scraper_obj.scrape_nwt()

scraper_obj = sc_bs()
clues = scraper_obj.scrape_puzzle()
