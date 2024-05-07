from MillerRabin import *

licznik = 0
for i in range(1, 7920):
    a, b = Miller_Rabin_Test(i, 100)
    if a:
        print(i, b)
        licznik += 1
print(f"W tym przedziale jest {licznik} pierwszych")