import codecs
import struct
import sys
import numpy as np
import tkinter as tk

from DESX import *

import bitarray as bit


# b = bytearray("polinezja", "utf-8")
#
# a = bit.bitarray()
#
# op = np.packbits(1)
#
# a.frombytes(b)
#
# tab = np.array(np.uint8)
#
# # for i in range(len(199999)):
# #     tab.
#
# a = 1 << 4
#
# # print(a.nbytes)
#
# print(a.__sizeof__())
#
# print(sys.getsizeof(a))
#
# print(tab.__sizeof__())
#
# val = np.int64(1)
# print(val.__sizeof__())
# print(sys.getsizeof(val))
#
# val
#
# print(val.itemsize)
#
# val = val << 3
#
# print(val)
#
# tekst = "4Wy����"
#
# print(tekst)
#
# utf8_int_array = [int.from_bytes(znak.encode('utf-8')) for znak in tekst]
# klucz = np.int64(utf8_int_array[0])
# for i in range(len(utf8_int_array) - 1):
#     klucz = klucz * 256
#     klucz += utf8_int_array[i + 1]
#
# print(klucz)
#
# a = 1
# print(a)
# a = a << 1
# print(a)
# ciag = "Polecam jesc duzo masla albo czegos innego"
#
# print(blokiInt64(ciag))
#
# liczba = 0b0001001100110100010101110111100110011011101111001101111111110001
# print(bin(permutation1(liczba)))

# print(kluczNa3("1234567890123456abcdefghijklomnprstuwyxyz1234567"))


# def bloki_na_utf8(bloki):
#     utf8_text = b""
#     for blok in bloki:
#         utf8_text += struct.pack('>Q', blok)
#     return utf8_text.decode('utf-8')
#
#
# # Przykładowe bloki 64-bitowe jako numpy array
# bloki = np.array([0x48656c6c6f20776f, 0x726c6421],
#                  dtype=np.int64)  # Hexadecymalne reprezentacje bloków "Hello wo" i "rld!"
#
# # Zamiana bloków na tekst UTF-8
# tekst = bloki_na_utf8(bloki)
#
# print(tekst)  # Wynik: "Hello world!"
# wynik = desX("82F86742448B0D99", "111111111234567811111111", 0, False)
# print(wynik)
from tkinter.filedialog import askopenfilename
# tk.Tk().withdraw() # part of the import if you are not using other tkinter functions



# fn = askopenfilename()
# print("user chose", fn)


wynik = desX("szyfr.txt", "111111111234567811111111", 1, True)
print(wynik)


# np.int64()
#
# print(ROL(201326591, 2))
#
# print(zlaczLewyPrawyKlucze(134217728, 134217728))
#
# print(getFromSBox(1, 1, 0))


# def hex_to_int64(hex_text):  # Text w hexie zamieniony na int64
#     int64_value = np.int64(int.from_bytes(bytes.fromhex(hex_text), byteorder='big', signed=True))
#     return int64_value
#
#
# print(hex_to_int64("F9D2E08FB85A6C9C"))


# hex_values = wynik
# byte_values = bytes.fromhex(hex_values)
# result_string = byte_values.decode('utf-8')
# print(result_string)
# byte_values = result_string.encode('utf-8')
# hex_values = byte_values.hex()
# print(hex_values)