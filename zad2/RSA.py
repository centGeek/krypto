import random
from MillerRabin import *
import numpy as np

from EulerFunc import *
from nwd import *


def RSA(p, q):
    """
    Funkcja do generowania kluczy na podstawie dwóch liczb całkowitych p i q
    :param p:
    :param q:
    :return: d , e , n
    """
    test1 = Miller_Rabin_Test(p, 1000)
    test2 = Miller_Rabin_Test(q, 1000)
    if ((test1 & test2) != True):
        raise ValueError("ILOSC TESTOW BYŁA ZA MAŁA")

    n = p * q
    # while True:
    #     if e < EulerFunc(n):
    #         break
    #     e = random.randint(n // 2, n * 2)
    phi = (p - 1) * (q - 1)  # int(EulerFunc(n))
    e = random.randint(n // 4, phi - 1)

    var1 = (NWD(e, phi) == 1)
    while not var1:
        e = random.randint(4, phi - 1)
        var1 = (NWD(e, phi) == 1)

    # moze tu jest blad
    _, x, _ = moduloInverse(e, phi)
    # d = moduloInverse(e, phi)
    d = x + phi
    return d, e, n


import gmpy2


def RSA_encrypt(d: int, n: int, dane: int):
    """
    :param d: klucz prywatne
    :param n: element klucza publicznego
    :param dane: dane mają być zahaszowane
    :return: zwraca podpis cyfrowy
    """
    moze = gmpy2.powmod(dane, d, n)
    a = int(moze)
    # b = a % n
    # output = pow(dane, d, n)
    # halo = np.power(output, dane, n)
    return a


def RSA_decrypt(podpis, e, n, dane):
    result = gmpy2.powmod(podpis, e, n)
    result2 = pow(podpis, e, n)
    result = int(result)
    if result == dane:
        return True
    return False


def moduloInverse(a, b):
    if b == 0:
        return (a, 1, 0)

    x1, x2, y1, y2 = 0, 1, 1, 0
    while b > 0:
        q, r = divmod(a, b)
        x = x2 - q * x1
        y = y2 - q * y1

        a, b, x2, x1, y2, y1 = b, r, x1, x, y1, y

    gcd, x, y = a, x2, y2
    return (gcd, x, y)
    # nwd, x, y = extendedNWD(e, phi)
    # if nwd != 1:
    #     raise ValueError('No modular inverse')
    # return x % phi


def extendedNWD(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extendedNWD(b % a, a)
        return gcd, y - (b // a) * x, x
