import ctypes
import tkinter

import numpy as np

blockSize = 8  # Kazdy blok danych jest reprezentowany jako 64 bitowy


def desX(dane, klucz):
    if (len(klucz) != 24):              #sprawdzamy czy ten podany klucz jest poprawnej dlugosci
        print(len(klucz))
        ctypes.windll.user32.MessageBoxW(0, "Podano złą długość klucza", "Błąd", 0)
        return

    # Pierwsze co to dzielimy dane na bloki kazdy bedzie juz od razu reprezentowany jako int64
    blokiDanych = blokiInt64(dane)
    # Podobnie klucze zostaja podzielone oraz zamineione na odpowiednie typy
    klucze = kluczNa3(klucz)
    for i in range(len(klucze)):
        klucze[i] = kluczNaInt64(klucze[i])


    output = np.int64()

    #####################################
    #               XOR1                #
    #####################################
    for i in range(len(blokiDanych)):
        blokiDanych[i] = xor(blokiDanych[i], klucze[0])

    #####################################
    #               DES                 #
    #####################################

    # Rozpoczynamy od operacji na kluczu (z tablicy wybieramy ten pod indeksem 1, bo ten jest dla DES-a)

    permutation1(klucze[1])


    sBox = \
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,  # S1
         0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
         4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
         15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13,

         15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,  # S2
         3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
         0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
         13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9,

         10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,  # S3
         13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
         13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
         1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12,

         7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,  # S4
         13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
         10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
         3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14,

         2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,  # S5
         14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
         4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
         11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3,

         12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,  # S6
         10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
         9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
         4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13,

         4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,  # S7
         13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
         1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
         6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12,

         13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,  # S8
         1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
         7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
         2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]

    return output


def xor(dane, klucz):
    # klucz_b = kluczNaInt64(klucz)
    dane_b = dane
    danePoXor = dane_b.__xor__(klucz)

    print("Dane ", dane, " dane_b ", danePoXor)
    return danePoXor


def xorFromString(dane, klucz):
    # dane = bytearray(dane, "utf-8")
    output = xor(dane, klucz)  # odwołanie do XOR-owania
    output = output.decode("utf-8")
    return output


def blokiInt64(dane):
    bloczki = podzielNaBloki(dane)
    interArray = np.empty(len(bloczki), dtype=np.int64)
    for x in range(len(bloczki)):
        inter = np.int64()
        for i in range(8):
            for j in range(8):
                temp = bloczki[x][i] & (128 >> j)
                inter += temp
            inter = inter << 8
        interArray[x] = inter
    return interArray


def podzielNaBloki(dane):  # funkcja zamienia dane na bloki BAJTÓW i dopełnia do 64 bitów (aby blok zawsze tyle miały)
    dane = bytearray(dane, "utf-8")
    blocks = []
    for i in range(0, len(dane), blockSize):
        block = dane[i:i + blockSize]
        if len(block) < blockSize:
            block += b"\x00" * (blockSize - len(block))  # Uzupełnienie zerami(bitowymi) , jeśli blok jest krótszy
        blocks.append(block)
    return blocks


def kluczNaInt64(klucz):  # Funkcja zwraca klucz w int64(który ma być podany jako UTF-8))
    utf8_int_array = [int.from_bytes(znak.encode('utf-8')) for znak in klucz]
    klucz = np.int64()  # utf8_int_array[0]
    for i in range(len(utf8_int_array) - 1):
        klucz += utf8_int_array[i]
        klucz = klucz * 256
    return klucz


def getXPosFrom64Bits(var, x):
    x = int(x)
    mask = 1 << (64 - x)
    var = var & mask
    var = var >> (64 - x)
    return var


def permutation1(klucz):
    permuted = 0
    pc_1 = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
            63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]
    for i in range(len(pc_1)):
        permuted += getXPosFrom64Bits(klucz, np.int64(pc_1[i]))
        permuted = permuted << 1
    permuted = permuted >> 1
    return permuted


def permutation2(klucz):
    permuted = 0
    pc_1 = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47,
            55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]
    for i in range(len(pc_1)):
        permuted += getXPosFrom64Bits(klucz, np.int64(pc_1[i]))
        permuted = permuted << 1
    permuted = permuted >> 1
    return permuted


def kluczNa3(klucz):  # funkcja zwraca liste kluczy
    return [klucz[i:i + blockSize] for i in range(0, len(klucz), blockSize)]
