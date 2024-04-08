#################################################
#                    DESX                       #
#       Autorzy: Maciej Dominiak    247644      #
#                Łukasz Centowski   247638      #
#                                               #
#################################################
import re

import DESX
from DESX import *
import tkinter as tk
from tkinter.filedialog import askopenfilename

keyProperLenth = 48


def show_text_data(event=None):
    text = entryDane.get()
    stringData.set(text)


def show_text_key(event=None):
    key = entryKlucz.get()
    stringKey.set(key)
    if len(key) == keyProperLenth:
        entryKlucz.config(bg="green")
    else:
        entryKlucz.config(bg="white")


def doTheDesXFromEntry(dane, klucz, IsDecoding):
    if len(klucz) == keyProperLenth:
        entryOutput.config(state="normal")
        entryOutput.delete(0, "end")
        entryOutput.insert(0, DESX.desX(dane, klucz, IsDecoding, False))
        entryOutput.config(state="readonly")
    else:
        ctypes.windll.user32.MessageBoxW(0, "Podano złą długość klucza", "Błąd", 0)
        print("Klucz jest niepoprawnej długości!!!")


def doTheDesXFromFile(dane, klucz, IsDecoding):
    if len(klucz) == keyProperLenth:
        entryOutput.config(state="normal")
        entryOutput.delete(0, "end")
        ctypes.windll.user32.MessageBoxW(0, "Wybierz plik na którym chcesz wykonać operacje", "Wybierz", 0)
        sciezka = askopenfilename()
        entryOutput.insert(0, DESX.desX(sciezka, klucz, IsDecoding, True))
        entryOutput.config(state="readonly")
    else:
        ctypes.windll.user32.MessageBoxW(0, "Podano złą długość klucza", "Błąd", 0)
        print("Klucz jest niepoprawnej długości!!!")


def validate(textDoWalidacji):
    return bool(re.match("^[0-9a-fA-F]*$", textDoWalidacji))


root = tk.Tk()
root.title("DESX")

# Zarejestrowanie naszej funkcji walidującej
registerValidate = root.register(validate)

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

entryDane = tk.Entry(frame, width=100, validate="key", validatecommand=(registerValidate, '%P'))
entryDane.bind('<KeyRelease>', show_text_data)  # Wywołaj funkcję show_text_data po zwolnieniu klawisza
entryDane.grid(column=0, row=0)

entryKlucz = tk.Entry(frame, width=100, validate="key", validatecommand=(registerValidate, '%P'))
entryKlucz.bind('<KeyRelease>', show_text_key)  # Wywołaj funkcję show_text_key po zwolnieniu klawisza
entryKlucz.grid(column=2, row=0)

entryOutput = tk.Entry(frame, width=100)
entryOutput.config(state="readonly")
entryOutput.grid(column=1, row=2)

# LABELS

dataLabel = tk.Label(frame, textvariable=stringData)  # Etykieta sprawdzajaca co jest w "kodzie" dla stringData
dataLabel.grid(column=0, row=1)

keyLabel = tk.Label(frame, textvariable=stringKey)  # Etykieta sprawdzajaca co jest w "kodzie" dla stringKey
keyLabel.grid(column=2, row=1)

# CHECKBOX
decode = tk.BooleanVar()
c1 = tk.Checkbutton(frame, text='Decode?', variable=decode, onvalue=1, offvalue=0)
c1.grid(column=1, row=5)
# BUTTONS

desXButton = tk.Button(frame, text="DESX",
                       command=lambda: doTheDesXFromEntry(stringData.get(), stringKey.get(), decode.get()),
                       pady=10,
                       padx=10)  # Przycisk wykonujacy DESX
# but.pack(pady=0, padx=100)
desXButton.grid(column=0, row=5)

desXFromFileButton = tk.Button(frame, text="DESX from file",
                               command=lambda: doTheDesXFromFile(stringData.get(), stringKey.get(), decode.get()),
                               pady=10, padx=10)  # Przycisk odpowiedzialny za wyjscie
desXFromFileButton.grid(column=2, row=5)

quitButton = tk.Button(frame, text="Quit", command=root.destroy, pady=10, padx=10)  # Przycisk odpowiedzialny za wyjscie
# but.pack(pady=0, padx=100)
quitButton.grid(column=1, row=7)

# Rozpocznij pętlę zdarzeń
root.mainloop()
