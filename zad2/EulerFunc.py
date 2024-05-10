from nwd import *
from sympy import totient


# Niestety jestesmy zmuszeni skorzystac z tego gdyz nasze rozwiazania sa bardzo powolne
def EulerFunc(n):
    phi = totient(n)
    return phi

    # result = n
    # p = 2
    # while p * p <= n:
    #     if n % p == 0:
    #         while n % p == 0:
    #             n //= p
    #         result -= result // p
    #     p += 1
    # if n > 1:
    #     result -= result // n
    # return result

    # result = 1
    # for i in range(2, n):
    #     if (NWD(i, n) == 1):
    #         result += 1
    # return result
