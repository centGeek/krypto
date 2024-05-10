import math


def NWD(a, b):
    """
    Funkcja do liczenia największego wspólnego dzielnika
    :param a:
    :param b:
    :return:
    """

    return math.gcd(a,b)
    #print(a,b)
    # if b == 0:
    #     return a
    # return NWD(b, a % b)
