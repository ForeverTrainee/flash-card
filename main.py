import tkinter
import pandas
import random
import time

BACKGROUND_COLOR_GREEN = "#B1DDC6"
BACKGROUND_COLOR_WHITE = '#FFFFFF'
BACKGROUND_COLOR_BLACK = '#000000'
current_card = {}
# ------------------------------------- CSV -------------------------------------

try:
    data_df = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data_df = pandas.read_csv("data/french_words.csv")
    data_dict = data_df.to_dict(orient="records")  # <- read more about to_dict attributes

else:
    data_dict = data_df.to_dict(orient="records")  # <- read more about to_dict attributes


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(data_dict)
    canvas.itemconfig(card_title, text="French", fill=BACKGROUND_COLOR_BLACK)
    canvas.itemconfig(card_word, text=current_card["French"], fill=BACKGROUND_COLOR_BLACK)
    canvas.itemconfig(card_background, image=card_front)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="English", fill=BACKGROUND_COLOR_WHITE)
    canvas.itemconfig(card_word, text=current_card["English"], fill=BACKGROUND_COLOR_WHITE)
    canvas.itemconfig(card_background, image=card_back)


def known_word():
    data_dict.remove(current_card)
    next_card()
    data_df = pandas.DataFrame(data_dict)
    data_df.to_csv("data/words_to_learn.csv", index=False)


# -------------------------------------UI -------------------------------------

# Main window
window = tkinter.Tk()
window.title("Flash Cards")
window.config(height=400, width=400, pady=50, padx=50, bg=BACKGROUND_COLOR_GREEN)
flip_timer = window.after(3000, func=flip_card)

# Canvas
canvas = tkinter.Canvas(width=800, height=526)
card_front = tkinter.PhotoImage(file="images/card_front.png")
card_back = tkinter.PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front)
canvas.config(bg=BACKGROUND_COLOR_GREEN, highlightthickness=0)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

# Correct button

right_image = tkinter.PhotoImage(file="images/right.png")
known_button = tkinter.Button(image=right_image, highlightthickness=0, command=known_word)
known_button.grid(column=1, row=1)

# Wrong button

wrong_image = tkinter.PhotoImage(file="images/wrong.png")
unknown_button = tkinter.Button(image=wrong_image, highlightthickness=0, command=next_card)
unknown_button.grid(column=0, row=1)

window.mainloop()
