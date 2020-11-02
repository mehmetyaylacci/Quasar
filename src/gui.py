import PySimpleGUI as sg
import random
BOX_SIZE = 80

sg.change_look_and_feel("BlackWhite")

layout = [
    [sg.Frame('',[
        [sg.Graph((1280, 720), (0, 720), (1280, 0), key='graph',
            change_submits=True, drag_submits=False)],
        [sg.Button('Clear'), sg.Button('Exit')]])
    ]
]

sg.Input(justification='center',size=(100,1))

window = sg.Window('XOxygen Puzzle Solver', layout, finalize=True)

g = window['graph']

# font for letters
font_letter = ("Courier New", 18)

for row in range(5):
    for col in range(5):
        if random.randint(0, 100) > 10:
             g.draw_rectangle((col * BOX_SIZE + 5, row * BOX_SIZE + 3), (col * BOX_SIZE +
                                        BOX_SIZE + 5, row * BOX_SIZE + BOX_SIZE + 3), line_color='black', fill_color='white')
        else:
            g.draw_rectangle((col * BOX_SIZE + 5, row * BOX_SIZE + 3), (col * BOX_SIZE + BOX_SIZE +
                                                                        5, row * BOX_SIZE + BOX_SIZE + 3), line_color='black', fill_color='black')
        g.draw_text('{}'.format(row * 5 + col + 1),
                    (col * BOX_SIZE + 10, row * BOX_SIZE + 8))

        g.draw_text('{}'.format('A'),
                    (col * BOX_SIZE + 30, row * BOX_SIZE + 30), font=font_letter)

while True:
    event, values = window.read()

    if event in (None, "Close"):
        break
    if event in (None, "Clear"):
        for row in range(5):
            for col in range(5):
                g.draw_rectangle((col * BOX_SIZE + 5, row * BOX_SIZE + 3), (col * BOX_SIZE +
                                        BOX_SIZE + 5, row * BOX_SIZE + BOX_SIZE + 3), line_color='black', fill_color='white')

window.close()
