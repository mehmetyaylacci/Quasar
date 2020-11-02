#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
import csv
import PySimpleGUI as sg
from db_df import db_df

# root = Tk()
# canvas = Canvas(root, width = 1000, height = 530)
# canvas.pack()
# # canvas.
# mainloop()
#
# csv_file = open("thefile.txt", "r")
# reader = csv.DictReader(csv_file)
#
# def get_by_name(name):
#     for row in reader:
#         if row["name"].lower() == name.lower():
#             id_of_bilkenter = row["id"]
#
#     img = PhotoImage(file="photos/" + id_of_bilkenter + ".png")
#     canvas.create_image(10,10, anchor=NW, image=img)
#
# get_by_name(e.get())


def pretty(stuff, name):
    list = stuff.split(" :: ")
    return name + "\n--- ".join(list)


def work():
    db = db_df()
    checker = True
    sg.change_look_and_feel("DarkGrey2")

    Buttons = []

    image_elem = sg.Image(filename='photos/0.png')
    update_text = sg.Text("Classes", size=[50, 30])

    for x in range(1000):
        Buttons.append(sg.Button(str(x), button_color=(
            'black', 'sandy brown'), visible=True))

    my_column = sg.Column([[Buttons[0]]], scrollable=True,
                          size=[400, 600])

    for x in range(999):
        my_column.add_row(Buttons[x + 1])

    layout = [
        [sg.Frame('', [
            [sg.Text("Name"), sg.InputText('', key="name")],
            [sg.Text("Class"), sg.InputText('', key="class")],
            [sg.Button("Search"), sg.Button("Close")],
            [image_elem]
        ]),

            sg.Frame('', [[update_text]]),

            sg.Frame('', [[my_column]])]]

    window = sg.Window("Database", layout)

    # while True:
    #     event, values = window.read()
    #     if event in (None, "Close"):
    #         break
    #     if event in (None, "Search"):
    #         query = values["name"]
    #         bilkenter = db.id_and_ders(query)
    #         print(bilkenter)
    #         try:
    #             new_file = 'photos/' + str(bilkenter["id"]) + '.png'
    #         except:
    #             checker = False
    #
    #         if checker:
    #             image_elem.Update(filename=new_file)
    #             update_text.Update(value=pretty(bilkenter["ders"], bilkenter["name"]))
    #         else:
    #             checker = True
    #
    #     print(f'Event: {event}')
    #     print(str(values))

    while True:
        event, values = window.read()

        if event in (None, "Close"):
            break

        elif event in (None, "Search"):
            for x in range(1000):
                Buttons[x].update(text=str(x), button_color=(
                    'black', 'yellow'), visible=False)

            query = values["name"]
            query2 = values["class"]
            bilkenter = db.id_multiple(query, query2)

            list_bilkenter = list(bilkenter)

            print(list_bilkenter)

            if len(list_bilkenter) != 1:
                for x in range(len(list_bilkenter)):
                    Buttons[x].update(text=list_bilkenter[x]['name'], button_color=(
                        'black', 'sandy brown'), visible=True)

            elif len(list_bilkenter) == 1:
                bilkenter = db.id_and_ders(query)
                print(bilkenter)
                try:
                    new_file = 'photos/' + str(bilkenter["id"]) + '.png'
                except:
                    checker = False

                if checker:
                    image_elem.Update(filename=new_file)
                    update_text.Update(value=pretty(
                        bilkenter["ders"], bilkenter["name"]))
                else:
                    checker = True

        else:
            bilkenter = db.id_and_ders(list_bilkenter[int(event)]["name"])
            print(bilkenter)
            try:
                new_file = 'photos/' + str(bilkenter["id"]) + '.png'
            except:
                checker = False

            if checker:
                image_elem.Update(filename=new_file)
                update_text.Update(value=pretty(
                    bilkenter["ders"], bilkenter["name"]))
            else:
                checker = True

            print(f'Event: {event}')
            print(str(values))

    window.close()


work()
