# from scraper import Scraper as sc
from bs4_scraper import Scraper_bs as sc_bs
import numpy as np
# scraper_obj = sc()
# scraper_obj.scrape_nwt()

scraper_obj = sc_bs()
clues = scraper_obj.scrape_puzzle()
shape = scraper_obj.scrape_puzzle_numbers()
print(shape)
nparr = np.array(shape)
nparr = nparr.reshape(5, 5)
print(nparr)
# scraper_obj.scrape_sols()