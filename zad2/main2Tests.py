from MillerRabin import *
from nwd import *
from EulerFunc import *
from eulerlib import *
from HashFunc import *
from RSA import *

licznik = 0
for i in range(1, 7920):
    a = Miller_Rabin_Test(i, 100)
    if a:
        print(i)
        licznik += 1

print(f"W tym przedziale jest {licznik} pierwszych")
print(NWD(100, 56))

a = numtheory.Divisors()
good = 0
# Testowanie funkcji Eulera
for i in range(1, 101):
    if EulerFunc(i) == a.phi(i):
        print(i, EulerFunc(i))
        good += 1
print(f"Dobrze wyszło {good}")
p = 97
q = 89
n = p * q
e = EulerFunc(n)
e2 = (p - 1) * (q - 1)
print(f"niemożliwe że to tak jest {p} * {q} = {n} i potem że ten FI(n) = {e} czyli {e2}")

# hashowa1 = "1258adf24d5de44f"
# hashowa2 = 1321997746824930383
# print(f"Skrót z str: {hashFunc(hashowa1)}")
# print(f"Skrót z int: {hashFunc(hashowa2)}")


dana = "99"
dana = hashFunc(dana)

d, e, n = RSA(
    0xb72bde08993d62c3d9d90a7d65832b371c31401cde416fff1cc3e822e2b32b2bb9c69062e1dd08fccdf113c3bac48b82d78e420cee878c0e40db6540b39bddafc3f16cf132e40b0047b2c6d64bf5400f0ec10f1670d87245b21064061f7f4efe991570171f0f6faca7811904181eeb6314725c7f66e18d67def42d330e7d34a1,
    0xb6d692bb2948f89b2fd9b0a9ddd9867259e5f58944ff505e159498775d09a4a2f81420c9643b59d453b89994ae5ac11fa313bd670cfcd6e00bc55ae9fc420581a53337158098058ccf349037cd25f1d084cd44b8b7536ec990c381a8a36c36c551a0a16bd227c60cf1ef4ff3e230d428bb3edd8ed3e20a623a71db1a04c29e91)


podpis = RSA_encrypt(d, n, dana)
print(RSA_decrypt(podpis, e, n, dana))

# Test na działanie odworotności modulo
# print(moduloInverse(65537, 784357036801))
