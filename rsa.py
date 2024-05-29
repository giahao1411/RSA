import math
import random
from inverse_modulo import extended_euclidean
from inverse_modulo import inverse_modulo


# check if number is prime
def isPrime(n):
    for i in range(2, int(math.sqrt(n) + 1)):
        if n % i == 0:
            return False
    return True


# Get p and q randomly, note that p and q are primes so we check before get them
def get_p_and_q():
    # add integer 0 to n into primes list, this make it easily to get the random prime
    primes = [i for i in range(0, 1000) if isPrime(i)]

    # get p and q properly
    p = random.choice(primes)
    q = random.choice(primes)
    return p, q


# get modulus n = p * q for encryption and decryption
def get_modulus(p, q):
    return p * q


# Calculate Φ(n) = (p - 1) * (q - 1)
def phiN(p, q):
    return (p - 1) * (q - 1)


"""
prime_e often starts with e ∈ {3, 5, 17, 257, 65537} which are special primes
These exponents have computational benefits as they are of the form 2k + 1
But for small exponents, especially e = 3, it will be easily for being attacked

number e is less than n (modulus), such that n is relatively prime to (p - 1) * (q - 1)
have no common factor except 1 (GCD(e, phiN) = 1)

e is defined by 1 < e < Φ(n)
"""


# Get encryption key e
def prime_e(phiN):
    for i in range(2, phiN):
        gcd, x, y = extended_euclidean(i, phiN)
        if gcd == 1:
            return i
    return -1


"""
we have e * d = k * Φ(n) + 1 which is e * d mod Φ(n) = 1
can be noted that d ≡ e^(-1) mod Φ(n)
which is d is the inverse modulo of e mod Φ(n). We reuse the pre-defined function in Question_8.py
"""


# Get decryption key
def get_d(e, phiN):
    return inverse_modulo(e, phiN)


# TODO: implementation for getting public_key() and private_key()
def public_key():
    return


def private_key():
    return


print(get_p_and_q())
p, q = get_p_and_q()
print(get_modulus(p, q))
print(phiN(p, q))
print(prime_e(phiN(p, q)))
