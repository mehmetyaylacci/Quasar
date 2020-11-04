import PySimpleGUI as sg
import random
from bs4_scraper import Scraper_bs as sc_bs
import time

# constants
PUZZLE_BOX = 130

# fonts
font_letter = ("Arial Black", 32)
font_number = ("Arial", 20)
font_clues = ('Times New Roman', 16)

# themes and colors
sg.change_look_and_feel("NeutralBlue")

layout = [
    [sg.Frame('',[
        [sg.Graph(canvas_size=(1000, 720), graph_bottom_left=(0, 720), graph_top_right=(1000, 0),
         key='graph', change_submits=True, drag_submits=False), sg.Text('', key='across', 
            size=(30, 10), font=font_clues), sg.Text('', key='down', size=(30, 10),
             font=font_clues)],
        [sg.Button('Show Answers'), sg.Button('Clear'), sg.Button('Exit')]])
    ]
]

sg.Input(justification='center', size=(100, 1))

window = sg.Window('XOxygen Puzzle Solver', layout, finalize=True)

g = window['graph']


#
# -----------------------FUNCTIONS-----------------------
#


def create_scraper():
    scraper_obj = sc_bs()
    clues = scraper_obj.scrape_puzzle()
    blacks = scraper_obj.scrape_puzzle_shape()
    numbers = scraper_obj.scrape_puzzle_numbers()
    return [clues, blacks, numbers]

def display_puzzle():

    counter = 0
    for row in range(5):
        for col in range(5):
            if blacks[counter] == 1:
                g.draw_rectangle((col * PUZZLE_BOX + 5, row * PUZZLE_BOX + 3),
                (col * PUZZLE_BOX + PUZZLE_BOX + 5, row * PUZZLE_BOX + PUZZLE_BOX + 3),
                line_color='black', fill_color='black')
            else:
                g.draw_rectangle((col * PUZZLE_BOX + 5, row * PUZZLE_BOX + 3),
                (col * PUZZLE_BOX + PUZZLE_BOX + 5, row * PUZZLE_BOX + PUZZLE_BOX + 3),
                line_color='black', fill_color='white')
            if numbers[counter] != -1:
                g.draw_text('{}'.format(numbers[counter]), (col * PUZZLE_BOX + 20,
                row * PUZZLE_BOX + 20),
                font=font_number)
            counter += 1


def display_puzzle_answers():
    for row in range(5):
        for col in range(5):            
            g.draw_text('{}'.format('A'), (col * PUZZLE_BOX + (PUZZLE_BOX/2),
            row * PUZZLE_BOX + (PUZZLE_BOX/2)), 
            font=font_letter)
  

def clear_puzzle():
    for row in range(5):
        for col in range(5):
            g.draw_rectangle((col * PUZZLE_BOX + 5, row * PUZZLE_BOX + 3), 
            (col * PUZZLE_BOX + PUZZLE_BOX + 5, row * PUZZLE_BOX + PUZZLE_BOX + 3),
                line_color='black', fill_color='white')
    display_puzzle()

#
# -----------------------END-----------------------
#

print("\n-------------\nNow scraping the NYT webpage for the puzzle\n-------------")
scraped = create_scraper()
print("Scraping done!\n-------------")
clues = scraped[0]
blacks = scraped[1]
numbers = scraped[2]

across_string = "Across\n"
down_string = "Down\n"

for clue in clues:
    if clue[2] == 'A':
        across_string += clue[0] + ') ' + clue[1] + '\n'
    elif clue[2] == 'D':
        down_string += clue[0] + ') ' + clue[1] + '\n'

print("Displaying the clues\n-------------")
window.FindElement('across').update(across_string)
window.FindElement('down').update(down_string)

print("Displaying the puzzle\n-------------")
display_puzzle()

while True:
    event, values = window.read()
    if event in (None, "Show Answers"):
        print("Showing answers\n-------------")
        display_puzzle_answers()
    if event in (None, "Clear"):
        print("Clearing the puzzle screen\n-------------")
        clear_puzzle()
    if event in (None, "Exit"):
        print('Exiting\n-------------')
        break
    if event in (None, "Close"):
        print('Exiting\n-------------')
        break
window.close()
