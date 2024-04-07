import ctypes
import os.path
import struct

import numpy as np

blockSize = 8  # Kazdy blok danych jest reprezentowany jako 64 bitowy

sBox = \
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,  # S1
      0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
      4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
      15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],

     [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,  # S2
      3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
      0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
      13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],

     [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,  # S3
      13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
      13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
      1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],

     [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,  # S4
      13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
      10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
      3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],

     [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,  # S5
      14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
      4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
      11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],

     [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,  # S6
      10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
      9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
      4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],

     [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,  # S7
      13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
      1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
      6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],

     [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,  # S8
      1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
      7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
      2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]


def desX(dane, klucz, strona, czyPlik):
    """
    :param dane:
    :param klucz:
    :param strona: 0 - szyfrowanie, 1 - odszyfrowywanie
    :param czyPlik: 0 - dane tekstowe w HEX, 1 - sciezka pliku w zmiennej "dane"
    :return:
    """
    if (len(klucz) != 24):  # sprawdzamy czy ten podany klucz jest poprawnej dlugosci
        print(len(klucz))
        ctypes.windll.user32.MessageBoxW(0, "Podano złą długość klucza,\nmusi miec 24 znaki!", "Błąd", 0)
        return

    blokiDanych = []
    # Pierwsze co to dzielimy dane na bloki kazdy bedzie juz od razu reprezentowany jako int64
    if not czyPlik:
        blokiDanych = blokiInt64(dane)
    else:
        blokiDanych = read_file_in_64_bit_blocks(dane)
    # Podobnie klucze zostaja podzielone oraz zamineione na odpowiednie typy
    klucze = kluczNa3(klucz)
    for i in range(len(klucze)):
        klucze[i] = kluczNaInt64(klucze[i])

    if (strona):
        klucze.reverse()
    #####################################
    #               XOR1                #
    #####################################

    # for i in range(len(blokiDanych)):
    #     blokiDanych[i] = xor(blokiDanych[i], klucze[0])

    #####################################
    #            DES KLUCZE             #
    #####################################

    # Rozpoczynamy od operacji na kluczu (z tablicy wybieramy ten pod indeksem 1, bo ten jest dla DES-a)

    L, R = podkluczeLewyPrawy(permutationPC1(klucze[1]))

    # Tablica mówiąca o tym o ile obracamy poprzedni klucz dla danego podklucza
    RolNum = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

    LeweKlucze = []
    PraweKlucze = []

    LeweKlucze.append(ROL(L, RolNum[0]))
    PraweKlucze.append(ROL(R, RolNum[0]))

    for i in range(15):
        LeweKlucze.append(ROL(LeweKlucze[i], RolNum[i + 1]))
        PraweKlucze.append(ROL(PraweKlucze[i], RolNum[i + 1]))
    # Po otrzymaniu Lewych i Prawych części podkluczy musimy je teraz ze sobą połączyć

    kluczeDlaDES = []
    for i in range(16):  # mamy 16 kluczy lewych i prawych
        kluczeDlaDES.append(zlaczLewyPrawyKlucze(LeweKlucze[i], PraweKlucze[i]))
        kluczeDlaDES[i] = permutationPC2(kluczeDlaDES[i])  # Po permutacji klucze maja 48 bit-y

    # Otrzymujemy dzieki tym funkcja pełen zestaw kluczy do obróbki danych

    if (strona):
        kluczeDlaDES.reverse()

    #####################################
    #       DES - CZĘŚĆ WŁAŚCIWA        #
    #####################################

    blokiWyjsciowe = []

    # Wykonyjemy pętle osobno dla każdego bloku
    for u in range(len(blokiDanych)):

        blokiDanych[u] = permutationIP(blokiDanych[u])

        # Tu beda przechowywane bloki z poprzednich rund
        L, R = daneLewePrawe(blokiDanych[u])
        LeweDane = [L]
        PraweDane = [R]

        # Po podzieleniu naszych danych na lewą i prawą część czas na 16 rund
        for i in range(16):

            # Rozszerzamy nasze dane a nastepnie XOR-ujemy je z kluczem dla rundy
            rozszerzoneDane = tablicaERozszerzenie(PraweDane[i])
            rozszerzoneDane = rozszerzoneDane ^ kluczeDlaDES[i]

            # Teraz musimy odczytać wartości z S-Boxów na podstawie 6-bitowych bloków(jest ich 8) z rozszerzonych danych
            # rccccr - tak wyglądają nasze bity
            # bierzmy i wybieramy tylko r oraz tylko c i otrzymujemy
            # rr - 2 bity (pierwszy i ostatni) - określają rząd w S-boxie
            # cccc - 4 bity (środkowe) - określają kolumnę w S-boxie

            result = 0
            for j in range(8):
                c = 0
                r = getXPosFromYBits(rozszerzoneDane, (j * 6) + 1, 48)
                r = r << 1
                r += getXPosFromYBits(rozszerzoneDane, (j * 6) + 6, 48)
                for k in range(4):
                    c += getXPosFromYBits(rozszerzoneDane, ((j * 6) + k + 2), 48)
                    c = c << 1
                c = c >> 1
                result += np.int64(getFromSBox(c, r, j))
                if (j == 7):
                    break
                result = result << 4
            # Wynik wszystkich S-boxów jest permutowany (bez zmiany wielkości, pozostjae 32-bity)
            result = permutationPBox(result)

            # XOR-owanie rezulatatu z lewą stroną
            result = LeweDane[i] ^ result

            # Dodanie danych do
            LeweDane.append(PraweDane[i])
            PraweDane.append(result)
        # Po zakonczeniu wszystkich 16 rund DES, odczytujemy wartosci
        zlaczone = zlaczPrawyLewyDane(LeweDane[16], PraweDane[16])
        # Znów dokonujemy permutacji na
        blokiWyjsciowe.append(permutationIP_1(zlaczone))

    #################################
    #           XOR - 2             #
    #################################

    # for i in range(len(blokiWyjsciowe)):
    #     blokiWyjsciowe[i] = xor(blokiWyjsciowe[i], klucze[2])

    if not czyPlik:
        output = bloki_na_hex(blokiWyjsciowe)
    else:
        nazwa_wyjscia = "szyfrogram.txt"
        if (strona):
            nazwa_wyjscia = "odszyfrowane.txt"
        zapisz_bloki_do_pliku(nazwa_wyjscia, blokiWyjsciowe)
        if (strona):
            wyszysc_nulle(nazwa_wyjscia)
        output = f"udało sie, zapisano wynik do {nazwa_wyjscia}"

    return output


def xor(dane, klucz):
    # klucz_b = kluczNaInt64(klucz)
    dane_b = dane
    danePoXor = dane_b.__xor__(klucz)

    print("Dane ", dane, " dane_b ", danePoXor)
    return danePoXor


def blokiInt64(dane):
    bloczki = dzielCiagZnakowNa16(dane)
    interArray = np.empty((len(bloczki),), dtype=np.int64)
    for x in range(len(bloczki)):
        interArray[x] = hex_to_int64(bloczki[x])
    return interArray


def dzielCiagZnakowNa16(tekst):
    output = []
    for i in range(0, len(tekst), 16):
        chunk = tekst[i:i + 16]
        # Uzupełnienie fragmentu zerami, jeśli jest krótszy niż 16 znaków
        chunk += '0' * (16 - len(chunk))
        output.append(chunk)
    return output


def hex_to_int64(hex_text):  # Tekst w hexie zamieniony na int64
    int64_value = np.int64(int.from_bytes(bytes.fromhex(hex_text), byteorder='big', signed=True))
    return int64_value


def kluczNaInt64(klucz):  # Funkcja zwraca klucz w int64(który ma być podany jako UTF-8))
    utf8_int_array = [int.from_bytes(znak.encode('utf-8')) for znak in klucz]
    klucz = np.int64()  # utf8_int_array[0]
    for i in range(len(utf8_int_array) - 1):
        klucz += utf8_int_array[i]
        klucz = klucz * 256
    return klucz


def getXPosFromYBits(var, x, y):
    """
        var - zmienna z ktrej czytamy

        x - pozycja bitu, licząc od lewej strony NUMEUJĄC OD 1

        y - długość w bitach tego ciagu
    """
    x = np.int64(x)
    var = np.int64(var)
    mask = 1 << (y - x)
    var = var & mask
    var = var >> (y - x)
    return abs(var)


def permutationPC1(klucz):
    permuted = 0
    pc_1 = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
            63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]
    for i in range(len(pc_1)):
        permuted += getXPosFromYBits(klucz, np.int64(pc_1[i]), 64)
        if (i == len(pc_1) - 1):
            break
        permuted = permuted << 1
    # permuted = permuted >> 1
    return permuted


def permutationPC2(klucz):
    permuted = 0
    pc_2 = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47,
            55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]
    for i in range(len(pc_2)):
        permuted += getXPosFromYBits(klucz, np.int64(pc_2[i]), 56)
        if (i == len(pc_2) - 1):
            break
        permuted = permuted << 1
    # permuted = permuted >> 1
    return permuted


def kluczNa3(klucz):  # funkcja zwraca liste kluczy
    return [klucz[i:i + blockSize] for i in range(0, len(klucz), blockSize)]


def podkluczeLewyPrawy(klucz):
    maska = (1 << 28) - 1
    L = (klucz >> 28)
    R = klucz & maska
    return L, R


def zlaczLewyPrawyKlucze(L, P):
    klucz = L
    klucz = klucz << 28
    klucz += P
    return klucz


def ROL(klucz, count):  # funkcja do kręcenia podkluczami (28 bitowymi), realnie przyjmuje tylko 1 i 2 w count
    maska = 0
    bity = 0
    if count == 2:
        maska = (3 << (28 - count))
        bity = klucz & maska
        klucz -= bity
        klucz = klucz << 2
        bity = bity >> 26
        klucz += bity
    else:
        maska = (1 << (28 - count))
        bity = klucz & maska
        klucz -= bity
        klucz = klucz << 1
        bity = bity >> 27
        klucz += bity
    return klucz


def permutationIP(dane):  # To jest permutacja która nic pod wzgledem mocy zabezpieczen nie wnosi
    permuted = 0
    tablicaIP = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6, 64, 56,
                 48, 40, 32, 24, 16, 8, 57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3, 61, 53, 45, 37, 29,
                 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7]
    for i in range(len(tablicaIP)):
        permuted += getXPosFromYBits(dane, np.int64(tablicaIP[i]), 64)
        if (i == len(tablicaIP) - 1):
            break
        permuted = permuted << 1
    # permuted = permuted >> 1
    return permuted


def daneLewePrawe(dane):
    """
    Funkcja zwraca nam dwa bloki danych po 32 bity, dzieląc oryginalne 64 na dwa w polowie
    """
    maska = (1 << 32) - 1
    L = (dane >> 32) & maska
    R = dane & maska
    return L, R


def tablicaERozszerzenie(
        blokDanych):  # Rozszerzamy dane na 48 bitowy blok, tak, aby miały ten sam rozmiar co klucz rundy
    permuted = 0
    tablica_E = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17, 16, 17, 18, 19, 20,
                 21, 20, 21, 22, 23, 24, 25, 24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]
    for i in range(len(tablica_E)):
        permuted += getXPosFromYBits(blokDanych, np.int64(tablica_E[i]), 32)
        if (i == len(tablica_E) - 1):
            break
        permuted = permuted << 1
    # permuted = permuted >> 1
    return permuted


def getFromSBox(c, r, j):
    """
    c - numer kolumny (0-15)

    r - numer wiersza (0-3)

    j - numer S-Boxa (0-7)

    Zwraca wartosc j-tego S boxa w podanym miejscu:
    """
    return sBox[int(j)][((int(r) * 16) + int(c))]


def permutationPBox(blokDanych):
    permuted = 0
    p_box = [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10, 2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22,
             11, 4, 25]
    for i in range(len(p_box)):
        permuted += getXPosFromYBits(blokDanych, np.int64(p_box[i]), 32)
        if (i == len(p_box) - 1):
            break
        permuted = permuted << 1
    # permuted = permuted >> 1
    return permuted


def zlaczPrawyLewyDane(L, P):
    """
    Funkcja wykonywana po 16 rundach łączy ze sobą bloki w odwrotnej kolejnosci (RL)
    """
    P = P << 32
    out = P + L
    return out


def permutationIP_1(dane):
    permuted = 0
    tablicaIP_1 = [40, 8, 48, 16, 56, 24, 64, 32,
                   39, 7, 47, 15, 55, 23, 63, 31,
                   38, 6, 46, 14, 54, 22, 62, 30,
                   37, 5, 45, 13, 53, 21, 61, 29,
                   36, 4, 44, 12, 52, 20, 60, 28,
                   35, 3, 43, 11, 51, 19, 59, 27,
                   34, 2, 42, 10, 50, 18, 58, 26,
                   33, 1, 41, 9, 49, 17, 57, 25]
    for i in range(len(tablicaIP_1)):
        permuted += getXPosFromYBits(dane, np.int64(tablicaIP_1[i]), 64)
        if (i == 63):
            break
        permuted = permuted << 1
    return permuted


def bloki_na_hex(bloki):
    tekst_hex = ""
    for blok in bloki:
        for k in range(0, 16, 4):
            temp = 0
            for i in range(4):
                mask = (blok >> (60 - 4 * k - 4 * i)) & 0xF  # Ustalanie maski 4-bitowej
                temp <<= 4  # Przesunięcie o 4 bity w lewo, aby zrobić miejsce na nowy 4-bitowy fragment
                temp |= mask  # Dodanie 4-bitowego fragmentu do temp
            tekst_hex += format(temp, '04X')  # Konwersja temp na tekst i dodanie do wyniku
    return tekst_hex


def read_file_in_64_bit_blocks(file_path):
    rozmiar = os.path.getsize(file_path)  # w bitach
    if (rozmiar % 8) != 0:
        rozmiar = rozmiar // 8
        rozmiar += 1
    else:
        rozmiar = rozmiar // 8
    blocks = np.empty((rozmiar,), dtype=np.int64)
    # blocks = []
    with open(file_path, 'rb') as file:
        i = 0
        while True:
            # Odczytanie 8 bajtów z pliku
            data = file.read(8)
            if not data:
                break  # Zakończ pętlę jeśli nie ma więcej danych

            # Sprawdzenie, czy odczytano dokładnie 8 bajtów
            if len(data) < 8:
                # Wypełnienie brakujących bajtów zerami
                data += b'\x00' * (8 - len(data))

            # Konwersja 8 bajtów na int64
            block = np.frombuffer(data, dtype=np.int64)[0]
            blocks[i] = block
            i += 1
    return blocks


def zapisz_bloki_do_pliku(sciezka, blocks):
    with open(sciezka, 'wb') as file:
        for block in blocks:
            # Konwersja int64 na bajty
            data = np.array(block, dtype=np.int64).tobytes()
            # Zapis bloku (64 bitów) do pliku
            file.write(data)


def wyszysc_nulle(sciezka):
    with open(sciezka, 'r+b') as file:
        # Przesunięcie kursora na koniec pliku
        file.seek(0, 2)
        # 2 oznacza ze offset jest traktowany od konca pliku
        end_position = file.tell()

        # Przesunięcie kursora wstecz, aby znaleźć ostatnie nie-zero bajty
        i = 1
        while True:
            file.seek(-i, 2)
            byte = file.read(1)
            if byte != b'\x00' or file.tell() == 1:
                break
            i += 1

        # Ustawienie długości pliku na ostatni nie-zero bajt
        file.truncate(end_position - i + 1)
