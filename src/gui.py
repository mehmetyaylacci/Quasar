import PySimpleGUI as sg
import random
from bs4_scraper import Scraper_bs as sc_bs
import time
from datetime import datetime
import threading

# constants
PUZZLE_BOX = 130

# fonts
font_letter = ("Arial Black", 40)
font_number = ("Arial", 20)
font_clues = ('Times New Roman', 16)

# themes and colors
sg.change_look_and_feel("NeutralBlue")

layout = [
    [sg.Frame('', [
        [sg.Graph(canvas_size=(1000, PUZZLE_BOX * 5 + 20), graph_bottom_left=(0, PUZZLE_BOX * 5 + 20), graph_top_right=(1000, 0),
        key='graph', change_submits=True, drag_submits=False), sg.Text('', key='across', size=(30, 10), font=font_clues), 
        sg.Text('', key='down', size=(30, 10), font=font_clues)], [sg.Text('', size=(20, 2), pad=((500, 0), (0, 0)), key='time')],
        [sg.Button('Show Answers'), sg.Button('Clear'), sg.Button('Exit')]], element_justification="left")
    ]
]

sg.Input(justification='center', size=(100, 1))

window = sg.Window('XOxygen Puzzle Solver', layout, finalize=True)

g = window['graph']


#
# -----------------------FUNCTIONS-----------------------
#


# Function to create the web scraper object
def create_scraper():
    scraper_obj = sc_bs()
    clues = scraper_obj.scrape_puzzle()
    blacks = scraper_obj.scrape_puzzle_shape()
    numbers = scraper_obj.scrape_puzzle_numbers()
    letters = scraper_obj.scrape_sols()
    return [clues, blacks, numbers, letters]


# Displays the puzzle grid with the black squares in place, also puts the numbers
def display_puzzle():
    counter = 0
    for x in range(5):
        for y in range(5):
            if blacks[counter] == 1:
                g.draw_rectangle((y * PUZZLE_BOX, x * PUZZLE_BOX),
                (y * PUZZLE_BOX + PUZZLE_BOX, x * PUZZLE_BOX + PUZZLE_BOX),
                line_color='black', fill_color='black')
            else:
                g.draw_rectangle((y * PUZZLE_BOX, x * PUZZLE_BOX),
                (y * PUZZLE_BOX + PUZZLE_BOX, x * PUZZLE_BOX + PUZZLE_BOX),
                line_color='black', fill_color='white')
            if numbers[counter] != -1:
                g.draw_text('{}'.format(numbers[counter]), (y * PUZZLE_BOX + 20,
                x * PUZZLE_BOX + 20),
                font=font_number)
            counter += 1


# Function to display the answers of the puzzle
def display_puzzle_answers():
    counter = 0
    for x in range(5):
        for y in range(5):
            if letters[counter] != '-1':
                g.draw_text('{}'.format(letters[counter]), (y * PUZZLE_BOX + (PUZZLE_BOX/2),
                x * PUZZLE_BOX + (PUZZLE_BOX/2)), 
                font=font_letter)
            counter += 1


# Function to clear the puzzle screen (gets rid of letters inputted)
def clear_puzzle():
    for x in range(5):
        for y in range(5):
            g.draw_rectangle((y * PUZZLE_BOX, x * PUZZLE_BOX), 
            (y * PUZZLE_BOX + PUZZLE_BOX, x * PUZZLE_BOX + PUZZLE_BOX),
                line_color='black', fill_color='white')
    display_puzzle()


# Function to return current date and time in string format
def time_func():
    current_date_time = str(datetime.now().strftime('%D %H:%M'))
    return "XOxygen " + current_date_time


#
# -----------------------END-----------------------
#

print("\n-------------\nNow scraping the NYT webpage for the puzzle\n-------------")
scraped = create_scraper()
print("Scraping done!\n-------------")
clues = scraped[0]
blacks = scraped[1]
numbers = scraped[2]
letters = scraped[3]

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
window.FindElement('time').update(time_func())

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
