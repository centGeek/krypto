import random


def Miller_Rabin_Test(liczba, dokladnosc):
    """
    Fukncja wykonująca test Millera Rabina
    :param liczba: liczba ktora chcemy sprawdzic czy jest pierwsza
    :param dokladnosc: tu podajemy liczbe rund
    :return: True jezeli podejzewamy iz liczba jest pierwsza, Falase jezeli nie jest pierwsza
    """
    blad = pow((1 / 4), dokladnosc)
    if liczba == 2 or liczba == 3:
        return True
    if (liczba % 2 == 0) | (liczba <= 2):
        return False
    s = 0
    d = liczba - 1
    while d % 2:
        s += 1
        d = d / 2
    for i in range(dokladnosc):         #Ile razy przeprowadzamy test Rabina-Millera
        a = random.randint(2, liczba - 2)   #Wybieramy losową podstawę z przedziału
        x = pow(a, d, liczba)
        if x == 1 or x == liczba - 1:       #To jest szybkie sprawdzenie czy nie spełniamy juz warunku
            continue
        j = 1
        while (j < s) & (x is not (liczba - 1)):
            x = pow(x, 2, liczba)
            if x == 1:
                return False
            j += 1
        if x is not (liczba - 1):
            return False
    return True
