import random
from tkinter import *
import pandas

timer = None
current_card = None

BACKGROUND_COLOR = "#B1DDC6"
TITLE_FONT = ("Ariel", 40, "bold")
TEXT_FONT = ("Ariel", 60, "bold")
SMALL_TEXT_FONT = ("Ariel", 20, "italic")

TITLE_TEXT = "Definition"
MAIN_TEXT = ("With anchor you specify which point of the widget you are referring to and with the two others you "
             "specify the location of that point. Just for example and to get a better understanding of it,")

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/IT_words.csv")
    to_learn = data.to_dict(orient="records")
    print(to_learn)
else:
    to_learn = data.to_dict(orient="records")
    print(to_learn)
words_to_learn = {}


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="Definition", font=TITLE_FONT, fill="Black")
    canvas.itemconfig(card_word, text=current_card["TERM"], font=TITLE_FONT, fill="Black")
    canvas.itemconfig(card_image, image=photo_front)
    flip_timer = window.after(3000, func=card_flip)


def card_flip():
    canvas.itemconfig(card_image, image=photo_back)
    canvas.itemconfig(card_title, text="Means:", font=TITLE_FONT, fill="White")
    canvas.itemconfig(card_word, text=current_card["MEANING"], font=SMALL_TEXT_FONT, fill="White")


def card_known():
    global current_card, flip_timer
    to_learn.remove(current_card)


    words_to_learn_dict = {object["TERM"]:object["MEANING"] for object in to_learn}
    print(words_to_learn_dict)
    data_to_learn = pandas.DataFrame(words_to_learn_dict,name="MEANING")
    data_to_learn.index.name = "TERM"
    print(data_to_learn)
    data_to_learn.to_csv("data/words_to_learn.csv")


    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="Definition", font=TITLE_FONT, fill="Black")
    canvas.itemconfig(card_word, text=current_card["TERM"], font=TITLE_FONT, fill="Black")
    canvas.itemconfig(card_image, image=photo_front)
    flip_timer = window.after(3000, func=card_flip)


window = Tk()
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

flip_timer = window.after(3000, func=card_flip)

photo_front = PhotoImage(file="images/card_front.png")
photo_back = PhotoImage(file="images/card_back.png")
photo_right = PhotoImage(file="images/right.png")
photo_wrong = PhotoImage(file="images/wrong.png")

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_image = canvas.create_image(400, 263, image=photo_front)
canvas.grid(column=0, row=0, columnspan=2)

card_title = canvas.create_text(400, 120, text=TITLE_TEXT, font=TITLE_FONT, anchor=CENTER, justify=CENTER)
card_word = canvas.create_text(400, 250, text=MAIN_TEXT, font=SMALL_TEXT_FONT, anchor=CENTER, justify=CENTER, width=700)

false_button = Button(width=100, height=100, bg=BACKGROUND_COLOR, image=photo_wrong, command=next_card)
false_button.grid(column=0, row=1)
true_button = Button(width=100, height=100, bg=BACKGROUND_COLOR, image=photo_right, command=card_known)
true_button.grid(column=1, row=1)

# title_label = Label(text=TITLE_TEXT,font=TITLE_FONT,anchor=CENTER,justify=CENTER)
# title_label.place(x=330,y=100)
#
# text_label = Label(text=MAIN_TEXT, font=SMALL_TEXT_FONT,anchor=CENTER,justify=CENTER, wraplength=700)
# text_label.place(x=50,y=200)

next_card()
window.mainloop()
