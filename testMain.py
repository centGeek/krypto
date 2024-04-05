import sys
import numpy as np
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

desX("12345678akljshdflksdahugfsdruygpoiearutg[oasriug[oasdijg;lasdijg;aiuh[qwoerirfuas[dcji[aosdiuf[oasid",
     "12345678abcdefgh12345678")

np.int64()

print(ROL(201326591, 2))

print(zlaczLewyPrawy(134217728, 134217728))
