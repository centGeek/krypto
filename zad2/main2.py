import ctypes
import random
import re
import tkinter as tk
from tkinter.filedialog import askopenfilename
from MillerRabin import *
from tkinter.filedialog import askopenfilename
import sys

from zad2 import HashFunc
from zad2.RSA import RSA, RSA_decrypt, RSA_encrypt

keyProperLenth = 15


def read_file_with_data():
    ctypes.windll.user32.MessageBoxW(0, "Wybierz plik z danymi", "Wybierz", 0)
    sciezka = askopenfilename()
    try:
        with open(sciezka, 'rb') as file:
            binary_data = file.read()
            hex_string = binary_data.hex()
            stringData.set(hex_string)
    except FileNotFoundError:
        print("Plik nie został znaleziony.")
    except Exception as e:
        print("Wystąpił błąd podczas odczytu pliku:", e)


def read_keys_from_file():
    try:
        with open("./kluczeDoRSA.txt", "r") as file:
            lines = file.readlines()

            if len(lines) < 3:
                print("Plik musi mieć co najmniej 3 linie.")
                return
            line1 = lines[0].strip()  # Usunięcie znaków nowej linii z końca
            line2 = lines[1].strip()
            line3 = lines[2].strip()

            stringKeyD.set(line1)
            stringKeyE.set(line2)
            stringKeyn.set(line3)
    except FileNotFoundError:
        print("Plik nie został znaleziony.")
    except Exception as e:
        print("Wystąpił błąd podczas odczytu pliku:", e)


def save_keys_to_file():
    try:
        with open("./kluczeDoRSA.txt", "w") as file:
            file.write(stringKeyD.get() + '\n')
            file.write(stringKeyE.get() + '\n')
            file.write(stringKeyn.get() + '\n')
    except Exception as e:
        print("Wystapił bład podczas zapisu do pliku", e)


def save_Signature_to_file():
    try:
        with open("./PodpisCyfrowyRSA.txt", "w") as file:
            file.write(stringSignature.get())
    except Exception as e:
        print("Wystapił bład podczas zapisu do pliku", e)


def read_Signature_from_file():
    try:
        with open("./PodpisCyfrowyRSA.txt", "r") as file:
            line = file.readlines()
            line1 = line[0].strip()  # Usunięcie znaków nowej linii z końca jakby takowy sie pojawił
            stringSignature.set(line1)
    except FileNotFoundError:
        print("Plik nie został znaleziony.")
    except Exception as e:
        print("Wystąpił błąd podczas odczytu pliku:", e)


def generate_keys(dokladnosc):
    p = random.getrandbits(1024)
    q = random.getrandbits(1024)
    while not (Miller_Rabin_Test(p, int(dokladnosc))):
        p = random.getrandbits(1024)
    while not (Miller_Rabin_Test(q, int(dokladnosc))):
        q = random.getrandbits(1024)

    d, e, n = RSA(p, q)

    dokl = pow(1 / 4, int(dokladnosc))
    print(p, q, dokl)
    print(d, e, n)
    d = hex(d)[2:]
    e = hex(e)[2:]
    n = hex(n)[2:]
    stringKeyD.set(d)
    stringKeyE.set(e)
    stringKeyn.set(n)


def show_text_key_n(event=None):
    text = entryKeyn.get()
    stringKeyn.set(text)


def show_text_key_d(event=None):
    key = entryKeyD.get()
    stringKeyD.set(key)


def show_text_key_q(event=None):
    key = entryKeyE.get()
    stringKeyE.set(key)


def show_text_data(event=None):
    data = entryData.get()
    stringData.set(data)


def show_text_signature(event=None):
    signature = entrySignature.get()
    stringSignature.set(signature)


def validate(textDoWalidacji):
    return bool(re.match("^[0-9a-fA-F]*$", textDoWalidacji))


def rsa_sign():
    d = int(stringKeyD.get(), 16)
    n = int(stringKeyn.get(), 16)
    dane = int(stringData.get(), 16)
    dane = HashFunc.hashFunc(dane)
    podpis = RSA_encrypt(d, n, dane)
    podpis = hex(podpis)[2:]
    stringSignature.set(podpis)


def rsa_check_singature():
    e = int(stringKeyE.get(), 16)
    n = int(stringKeyn.get(), 16)
    dane = HashFunc.hashFunc(int(stringData.get(), 16))
    podpis = int(stringSignature.get(), 16)
    result = RSA_decrypt(podpis, e, n, dane)
    if(result):
        stringOutput.set("Podpis jest poprawny")
    else:
        stringOutput.set("Podpis niepoprawny")

root = tk.Tk()
root.title("Podpis cyfrowy RSA")

# Zarejestrowanie naszej funkcji walidującej
registerValidate = root.register(validate)

frame = tk.Frame(root, padx=20, pady=20)

frame.grid()

# STRINGS
stringDescriptionKeyn = tk.StringVar()
stringDescriptionKeyn.set("n")

stringDescriptionKey = tk.StringVar()
stringDescriptionKey.set("Klucz")

stringDescriptionKeyD = tk.StringVar()
stringDescriptionKeyD.set("Klucz D")

stringDescriptionKeyE = tk.StringVar()
stringDescriptionKeyE.set("Klucz E")

stringDescriptionPreciosion = tk.StringVar()
stringDescriptionPreciosion.set("Ilosc \"rund\" testu Millera Rabina")

stringKeyD = tk.StringVar()  # Zwykła zmienna którą czyta (obserwuje) keyLabel
stringKeyD.set("")

stringKeyE = tk.StringVar()
stringKeyE.set("")

stringKeyn = tk.StringVar()  # Zwykła zmienna którą czyta (obserwuje) dataLabel
stringKeyn.set("")

stringData = tk.StringVar()
stringData.set("")

stringSignature = tk.StringVar()
stringSignature.set("")

stringOutput = tk.StringVar()  # Zwykła zmienna którą czyta (obserwuje) outputLabel
stringOutput.set("")

stringDataDescription = tk.StringVar()
stringDataDescription.set("Data")

stringSignatureDescription = tk.StringVar()
stringSignatureDescription.set("Signature")

# ENTRYS

entryKeyD = tk.Entry(frame, width=100, validate="key", validatecommand=(registerValidate, '%P'))
entryKeyD.bind('<KeyRelease>', show_text_key_d)  # Wywołaj funkcję show_text_key po zwolnieniu klawisza
entryKeyD.grid(column=1, row=3)

entryKeyE = tk.Entry(frame, width=100, validate="key", validatecommand=(registerValidate, '%P'))
entryKeyE.bind('<KeyRelease>', show_text_key_q)
entryKeyE.grid(column=1, row=4)

entryKeyn = tk.Entry(frame, width=100, validate="all", validatecommand=(registerValidate, '%P'))
entryKeyn.bind('<KeyRelease>', show_text_key_n)  # Wywołaj funkcję  po zwolnieniu klawisza
entryKeyn.grid(column=1, row=5)

entryData = tk.Entry(frame, width=100, validate="all", validatecommand=(registerValidate, '%P'))
entryData.bind('<KeyRelease>', show_text_data)
entryData.grid(column=1, row=6, padx=5, pady=5, ipady=10)

entrySignature = tk.Entry(frame, width=100, validate="all", validatecommand=(registerValidate, '%P'))
entrySignature.bind('<KeyRelease>', show_text_signature)
entrySignature.grid(column=1, row=7, padx=2, pady=2)

entryOutput = tk.Label(frame, textvariable=stringOutput,width=100)
entryOutput.grid(column=1, row=10)

# LABELS
labelDescriptionDKey = tk.Label(frame, textvariable=stringDescriptionKeyD)
labelDescriptionDKey.grid(column=0, row=3)

labelDescriptionEKey = tk.Label(frame, textvariable=stringDescriptionKeyE)
labelDescriptionEKey.grid(column=0, row=4)

labelDescriptionData = tk.Label(frame, textvariable=stringDataDescription)
labelDescriptionData.grid(column=0, row=6)

labelDescriptionSignature = tk.Label(frame, textvariable=stringSignatureDescription)
labelDescriptionSignature.grid(column=0, row=7)

# Etykieta sprawdzajaca co jest w "kodzie" dla stringKeyn
labelKeyn = tk.Entry(frame, state="readonly", textvariable=stringKeyn, width=150, borderwidth=1, relief="solid")
labelKeyn.grid(column=2, row=5)

# Etykieta sprawdzajaca co jest w "kodzie" dla stringDescriptionKeyn
labeklDescriptionKeyn = tk.Label(frame, textvariable=stringDescriptionKeyn)
labeklDescriptionKeyn.grid(column=0, row=5)

labelKeyD = tk.Entry(frame, width=150, borderwidth=1, relief="solid", state="readonly",
                     textvariable=stringKeyD)  # Etykieta sprawdzajaca co jest w "kodzie" dla stringKeyPublic
labelKeyD.grid(column=2, row=3)

labelKeyE = tk.Entry(frame, width=150, textvariable=stringKeyE, borderwidth=1, state="readonly",
                     relief="solid")
labelKeyE.grid(column=2, row=4)

labelData = tk.Entry(frame, width=150, textvariable=stringData, borderwidth=1, state="readonly",
                     relief="solid")
labelData.grid(column=2, row=6, padx=5, pady=5, ipady=10)

labelSignature = tk.Entry(frame, width=150, textvariable=stringSignature, borderwidth=1, state="readonly",
                          relief="solid")
labelSignature.grid(column=2, row=7)

labelPrecisionDescription = tk.Label(frame, textvariable=stringDescriptionPreciosion)
labelPrecisionDescription.grid(column=1, row=0, sticky="w")

# Buttons
quitButton = tk.Button(frame, text="Quit", command=root.destroy, pady=10, padx=10)  # Przycisk odpowiedzialny za wyjscie
# but.pack(pady=0, padx=100)
quitButton.grid(column=1, row=15)

generateKeysButton = tk.Button(frame, text="Generate Keys", command=lambda: generate_keys(spinboxPrecision.get()),
                               pady=10, padx=10)
generateKeysButton.grid(column=1, row=0, sticky="")

loadDataFromFileButton = tk.Button(frame, text="Load Data", command=lambda: read_file_with_data(), pady=10, padx=10)
loadDataFromFileButton.grid(column=2, row=2, sticky="")

saveKeysToFileButton = tk.Button(frame, text="Save Keys", command=lambda: save_keys_to_file(), pady=10, padx=10)
saveKeysToFileButton.grid(column=0, row=2, sticky="")

loadKeysFromFileButton = tk.Button(frame, text="Load Keys", command=lambda: read_keys_from_file(), pady=10, padx=10)
loadKeysFromFileButton.grid(column=1, row=2, sticky="")

saveSignatureToFileButton = tk.Button(frame, text="Save Signature", command=lambda: save_Signature_to_file(), pady=10,
                                      padx=10)
saveSignatureToFileButton.grid(column=2, row=8)

loadSignatureFromFileButton = tk.Button(frame, text="Load Signature", command=lambda: read_Signature_from_file(),
                                        pady=10, padx=10)
loadSignatureFromFileButton.grid(column=1, row=8)

signButton = tk.Button(frame, text="Sign", command=lambda: rsa_sign(), pady=10, padx=10)
signButton.grid(column=0, row=8)

checkSignatureButton = tk.Button(frame, text="Check", command=lambda: rsa_check_singature(), pady=10, padx=10)
checkSignatureButton.grid(column=1, row=9)

spinboxPrecision = tk.Spinbox(frame, from_=1, to=100, state="readonly")
spinboxPrecision.grid(column=0, row=0, sticky="e")

# Rozpocznij pętlę zdarzeń
root.mainloop()
