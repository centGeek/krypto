#################################################
#                    DESX                       #
#       Autorzy: Maciej Dominiak    247644      #
#                Łukasz Centowski   247638      #
#                                               #
#################################################
import DESX
from DESX import *
import tkinter as tk


def show_text_data(event=None):
    text = entryDane.get()
    dataString.set(text)


def show_text_key(event=None):
    key = entryKlucz.get()
    keyString.set(key)


def doTheDesX(dane, klucz):
    if (len(dane) == 3):
        keyString.set(DESX.xor(dane, klucz))
    else:
        print("iasidasd")


root = tk.Tk()
root.title("DESX")

frame = tk.Frame(root, padx=10, pady=10)

frame.grid()

keyString = tk.StringVar()  # Zwykła zmienna którą czyta (obserwuje) label
keyString.set("")

dataString = tk.StringVar()  # Zwykła zmienna którą czyta (obserwuje) label
dataString.set("")

entryDane = tk.Entry(frame)
entryDane.bind('<KeyRelease>', show_text_data)  # Wywołaj funkcję show_text_data po zwolnieniu klawisza
entryDane.grid(column=1, row=0)

entryKlucz = tk.Entry(frame)
entryKlucz.bind('<KeyRelease>', show_text_key)  # Wywołaj funkcję show_text_key po zwolnieniu klawisza
entryKlucz.grid(column=2, row=0)

dataLabel = tk.Label(frame, textvariable=dataString)  # Etykieta sprawdzajaca co jest w "kodzie" dla keyData
dataLabel.grid(column=1, row=1)

dataLabel = tk.Label(frame, textvariable=keyString)  # Etykieta sprawdzajaca co jest w "kodzie" dla keyString
dataLabel.grid(column=2, row=1)

desXButton = tk.Button(frame, text="DESX", command=lambda: doTheDesX(dataString.get(), keyString.get()), pady=10,
                       padx=10)  # Przycisk wykonujacy DESX
# but.pack(pady=0, padx=100)
desXButton.grid(column=0, row=5)

quitButton = tk.Button(frame, text="Quit", command=root.destroy, pady=10, padx=10)  # Przycisk odpowiedzialny za wyjscie
# but.pack(pady=0, padx=100)
quitButton.grid(column=5, row=5)

# Rozpocznij pętlę zdarzeń
root.mainloop()
