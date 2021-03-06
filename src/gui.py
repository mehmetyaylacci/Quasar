# @authors: 
# Burak Turksever
# Mehmet Yaylaci
# Eralp Kumbasar

import PySimpleGUI as sg
import random
from bs4_scraper import Scraper_bs as sc_bs
import time
from datetime import datetime
import threading
from naturl import NLP 
# constants
PUZZLE_BOX = 50

# fonts
font_letter = ("Arial Black", 20)
font_number = ("Arial", 10)
font_clues = ('Times New Roman', 14)

# themes and colors
sg.change_look_and_feel("Default1")

#layout of the puzzle designed according to the NYTimes puzzle template,
#using PySimpleGUI
layout = [
    [sg.Frame('', [
        [
            sg.Graph(canvas_size=(PUZZLE_BOX * 5 + 20, PUZZLE_BOX * 5 + 20), graph_bottom_left=(0, PUZZLE_BOX * 5 + 20), graph_top_right=(PUZZLE_BOX * 5 + 20, 0),
                     key='graph', change_submits=True, drag_submits=False, background_color="white"),
            sg.Column([
                [
                    sg.Text('', key='across', size=(30, 10),
                            font=font_clues, background_color="white"),
                    sg.Text('', key='down', size=(30, 10), font=font_clues, background_color="white")]], element_justification="c", pad=(50, 50), background_color="white"),

            sg.Graph(canvas_size=(PUZZLE_BOX * 5 + 20, PUZZLE_BOX * 5 + 20), graph_bottom_left=(0, PUZZLE_BOX * 5 + 20), graph_top_right=(PUZZLE_BOX * 5 + 20, 0),
                     key='graph-true', change_submits=True, drag_submits=False, background_color="white")],
        [
            sg.Text('', size=(20, 2), pad=((100, 0), (0, 0)), key='time', background_color="white")]],  element_justification="left", background_color="white")
    ]
]

# sg.Input(justification = 'center', size=(100, 1))

window = sg.Window('XOXYGEN Puzzle Solver', layout, finalize=True, size=(1400, 400), background_color="white")

g = window['graph']
g2 = window['graph-true']


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


'''
Displays the puzzle grid, including the black slots in their places, also putting
the numbers to associate the places of the words with the given clues
'''
def display_puzzle(g):
    print("Displaying the puzzle grid...\n-------------")
    counter = 0
    for x in range(5):
        for y in range(5):
            if blacks[counter] == 1:
                g.draw_rectangle((y * PUZZLE_BOX + 3, x * PUZZLE_BOX + 3),
                                 (y * PUZZLE_BOX + PUZZLE_BOX + 3,
                                  x * PUZZLE_BOX + PUZZLE_BOX + 3),
                line_color='black', fill_color='black')
            else:
                g.draw_rectangle((y * PUZZLE_BOX + 3, x * PUZZLE_BOX + 3),
                                 (y * PUZZLE_BOX + PUZZLE_BOX +
                                  3, x * PUZZLE_BOX + PUZZLE_BOX + 3),
                line_color='black', fill_color='white')
            if numbers[counter] != -1:
                g.draw_text('{}'.format(numbers[counter]), (y * PUZZLE_BOX + 10 + 3,
                                                            x * PUZZLE_BOX + 10 + 3),
                font=font_number)
            counter += 1


# Function to display the answers from the official solution of the puzzle,
# downloaded directly from NYTimes website
def display_puzzle_answers(g):
    counter = 0
    for x in range(5):
        for y in range(5):
            if letters[counter] != '-1':
                g.draw_text('{}'.format(letters[counter]), (y * PUZZLE_BOX + (PUZZLE_BOX/2) + 3,
                                                            x * PUZZLE_BOX + (PUZZLE_BOX/2) + 3),
                font=font_letter)
            counter += 1

#function to display the answers of the scraped
#puzzle found using nlp, for comparison with the official solution to
#test the success of the nlp algorithm
def display_puzzle_answers_nlp(solving, g):
    print("Putting the answers in their proper places...\n-------------")
    counter = 0
    letters = []
    black_ct = 0
    ct = 0
    ans = ""
    for i in solving:
        ans += str(i[1])
    print(ans)
    for i in range(len(blacks)):
        if blacks[black_ct] == 1:
            letters.append('-1')
        else:
            letters.append(ans[ct].upper())
            ct += 1
        black_ct += 1
    print(letters)
    
    for x in range(5):
        for y in range(5):
            if letters[counter] != '-1':
                g.draw_text('{}'.format(letters[counter]), (y * PUZZLE_BOX + (PUZZLE_BOX/2) + 3,
                                                            x * PUZZLE_BOX + (PUZZLE_BOX/2) + 3),
                font=font_letter)
            counter += 1


# Function to return current date and time in string format
def time_func():
    current_date_time = str(datetime.now().strftime('%D %H:%M'))
    return "XOXYGEN " + current_date_time


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

nlp_obj = NLP()
solving = nlp_obj.initiate_guessing()

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
display_puzzle(g2)
print("Displaying the puzzle answers as solved by the system\n-------------")
display_puzzle_answers_nlp(solving, g2)

print("Displaying the real puzzle\n-------------")
display_puzzle(g)
print("Displaying the puzzle answers as given by the site\n-------------")
display_puzzle_answers(g)

while True:
    event, values = window.read()
    # if event in (None, "Show Answers"):
    #     print("Showing answers\n-------------")
    #     display_puzzle_answers()
    # if event in (None, "Clear"):
    #     print("Clearing the puzzle screen\n-------------")
    #     clear_puzzle(g)
    if event in (None, "Exit"):
        print('Exiting\n-------------')
        break
    if event in (None, "Close"):
        print('Exiting\n-------------')
        break
    


window.close()
