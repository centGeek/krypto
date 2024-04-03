#################################################
#                    DESX                       #
#       Autorzy: Maciej Dominiak    247644      #
#                Łukasz Centowski   247638      #
#                                               #
#################################################
import DESX
from DESX import *
import tkinter as tk


keyProperLenth = 3


def show_text_data(event=None):
    text = entryDane.get()
    stringData.set(text)


def show_text_key(event=None):
    key = entryKlucz.get()
    stringKey.set(key)
    if len(key)== keyProperLenth:
        entryKlucz.config(bg="green")
    else:
        entryKlucz.config(bg="white")


def doTheDesX(dane, klucz):
    if len(klucz) == keyProperLenth:
        entryOutput.config(state="normal")
        entryOutput.delete(0, "end")
        entryOutput.insert(0, DESX.xorFromString(dane, klucz))
        entryOutput.config(state="readonly")
    else:
        print("Klucz jest niepoprawnej długości!!!")


root = tk.Tk()
root.title("DESX")

frame = tk.Frame(root, padx=10, pady=10)

frame.grid()

# STRINGS

stringKey = tk.StringVar()  # Zwykła zmienna którą czyta (obserwuje) keyLabel
stringKey.set("")

stringData = tk.StringVar()  # Zwykła zmienna którą czyta (obserwuje) dataLabel
stringData.set("")

stringOutput = tk.StringVar()  # Zwykła zmienna którą czyta (obserwuje) outputLabel
stringOutput.set("")

# ENTRYS

entryDane = tk.Entry(frame)
entryDane.bind('<KeyRelease>', show_text_data)  # Wywołaj funkcję show_text_data po zwolnieniu klawisza
entryDane.grid(column=0, row=0)

entryKlucz = tk.Entry(frame, width=100)
entryKlucz.bind('<KeyRelease>', show_text_key)  # Wywołaj funkcję show_text_key po zwolnieniu klawisza
entryKlucz.grid(column=2, row=0)

entryOutput = tk.Entry(frame)
entryOutput.config(state="readonly")
entryOutput.grid(column=1, row=2)

# LABELS

dataLabel = tk.Label(frame, textvariable=stringData)  # Etykieta sprawdzajaca co jest w "kodzie" dla stringData
dataLabel.grid(column=0, row=1)

keyLabel = tk.Label(frame, textvariable=stringKey)  # Etykieta sprawdzajaca co jest w "kodzie" dla stringKey
keyLabel.grid(column=2, row=1)

# BUTTONS

desXButton = tk.Button(frame, text="DESX", command=lambda: doTheDesX(stringData.get(), stringKey.get()), pady=10,
                       padx=10)  # Przycisk wykonujacy DESX
# but.pack(pady=0, padx=100)
desXButton.grid(column=0, row=5)

quitButton = tk.Button(frame, text="Quit", command=root.destroy, pady=10, padx=10)  # Przycisk odpowiedzialny za wyjscie
# but.pack(pady=0, padx=100)
quitButton.grid(column=5, row=5)

# Rozpocznij pętlę zdarzeń
root.mainloop()