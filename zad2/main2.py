import random
import re
import tkinter as tk
from tkinter.filedialog import askopenfilename
from MillerRabin import *


#keyProperLenth = 15

def show_text_data(event=None):
    text = entryDane.get()
    stringData.set(text)


def show_text_key_public(event=None):
    key = entryKluczPubliczny.get()
    stringKeyPublic.set(key)
    if len(key) == keyProperLenth:
        entryKluczPubliczny.config(bg="green")
    else:
        entryKluczPubliczny.config(bg="white")


def show_text_key_private(event=None):
    key = entryKeyPrivate.get()
    stringKeyPrivate.set(key)
    if len(key) == keyProperLenth:
        entryKeyPrivate.config(bg="green")
    else:
        entryKeyPrivate.config(bg="white")


def validate(textDoWalidacji):
    return bool(re.match("^[0-9a-fA-F]*$", textDoWalidacji))


root = tk.Tk()
root.title("Podpis cyfrowy RSA")

# Zarejestrowanie naszej funkcji walidującej
registerValidate = root.register(validate)

frame = tk.Frame(root, padx=20, pady=20)

frame.grid()

# STRINGS
stringDescriptionData = tk.StringVar()
stringDescriptionData.set("Dane")

stringDescriptionKey = tk.StringVar()
stringDescriptionKey.set("Klucz")

stringKeyPublicDescription = tk.StringVar()
stringKeyPublicDescription.set("Klucz Publiczny")

stringKeyPrivateDescription = tk.StringVar()
stringKeyPrivateDescription.set("Klucz Prywatny")

stringKeyPublic = tk.StringVar()  # Zwykła zmienna którą czyta (obserwuje) keyLabel
stringKeyPublic.set("")

stringKeyPrivate = tk.StringVar()
stringKeyPrivate.set("")

stringData = tk.StringVar()  # Zwykła zmienna którą czyta (obserwuje) dataLabel
stringData.set("")

stringOutput = tk.StringVar()  # Zwykła zmienna którą czyta (obserwuje) outputLabel
stringOutput.set("")

# ENTRYS

entryKluczPubliczny = tk.Entry(frame, width=100, validate="key", validatecommand=(registerValidate, '%P'))
entryKluczPubliczny.bind('<KeyRelease>', show_text_key_public)  # Wywołaj funkcję show_text_key po zwolnieniu klawisza
entryKluczPubliczny.grid(column=1, row=0)

entryKeyPrivate = tk.Entry(frame, width=100, validate="key", validatecommand=(registerValidate, '%P'))
entryKeyPrivate.bind('<KeyRelease>', show_text_key_private)
entryKeyPrivate.grid(column=1, row=1)

entryDane = tk.Entry(frame, width=100, validate="key", validatecommand=(registerValidate, '%P'))
entryDane.bind('<KeyRelease>', show_text_data)  # Wywołaj funkcję show_text_data po zwolnieniu klawisza
entryDane.grid(column=1, row=2)

entryOutput = tk.Entry(frame, width=100)
entryOutput.config(state="readonly")
entryOutput.grid(column=1, row=3)

# LABELS
labelDescriptionPublicKey = tk.Label(frame, textvariable=stringKeyPublicDescription)
labelDescriptionPublicKey.grid(column=0, row=0)

labelDescriptionPrivateKey = tk.Label(frame, textvariable=stringKeyPrivateDescription)
labelDescriptionPrivateKey.grid(column=0, row=1)

# Etykieta sprawdzajaca co jest w "kodzie" dla stringData
dataLabel = tk.Label(frame, textvariable=stringData)
dataLabel.grid(column=2, row=2)

# Etykieta sprawdzajaca co jest w "kodzie" dla stringData
labelDescriptionData = tk.Label(frame, textvariable=stringDescriptionData)
labelDescriptionData.grid(column=0, row=2)

labelKeyPublic = tk.Label(frame,
                          textvariable=stringKeyPublic)  # Etykieta sprawdzajaca co jest w "kodzie" dla stringKeyPublic
labelKeyPublic.grid(column=2, row=0)

labelKeyPrivate = tk.Label(frame, textvariable=stringKeyPrivate)
labelKeyPrivate.grid(column=2, row=1)
# labelKeyDescritpion = tk.Label(frame, textvariable=stringDescriptionKey)
# labelKeyDescritpion.grid(column=0, row=3)

# Buttons
quitButton = tk.Button(frame, text="Quit", command=root.destroy, pady=10, padx=10)  # Przycisk odpowiedzialny za wyjscie
# but.pack(pady=0, padx=100)
quitButton.grid(column=1, row=15)

# Rozpocznij pętlę zdarzeń
root.mainloop()
