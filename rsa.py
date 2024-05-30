import math
import random
import base64
from inverse_modulo import extended_euclidean
from inverse_modulo import inverse_modulo


# check if number is prime
def isPrime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n) + 1)):
        if n % i == 0:
            return False
    return True


# Get p and q randomly, note that p and q are primes so we check before get them
def get_p_and_q():
    # add integer 0 to n into primes list, this make it easily to get the random prime
    primes = [i for i in range(0, 1000000) if isPrime(i)]

    # get p and q properly
    p = random.choice(primes)
    q = random.choice(primes)
    return p, q


# get modulus n = p * q for encryption and decryption
def get_modulus(p, q):
    return p * q


# Calculate notient Φ(n) = (p - 1) * (q - 1)
def phiN(p, q):
    return (p - 1) * (q - 1)


"""
prime_e often starts with e ∈ {3, 5, 17, 257, 65537} which are special primes
These exponents have computational benefits as they are of the form 2k + 1
But for small exponents, especially e = 3, it will be easily for being attacked

number e is less than n (modulus), such that n is relatively prime to (p - 1) * (q - 1)
have no common factor except 1 which is GCD(e, phiN) = 1

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
which is d is the inverse modulo of e mod Φ(n). We reuse the pre-defined function in inverse_modulo.py
"""


# Get decryption key
def get_d(e, phiN):
    return inverse_modulo(e, phiN)


# public key taking e and n (e, n)
def get_public_key(p, q):
    n = get_modulus(p, q)
    phi_n = phiN(p, q)
    e = prime_e(phi_n)
    return (e, n)


def base64_public_key(public_key):
    e, n = public_key
    e_bytes = e.to_bytes((e.bit_length() + 7) // 8, byteorder="big")
    n_bytes = n.to_bytes((n.bit_length() + 7) // 8, byteorder="big")
    key_bytes = e_bytes + n_bytes
    base64_public_key = base64.b64encode(key_bytes).decode("utf-8")
    return base64_public_key


# private key taking d and n (d, n)
def get_private_key(p, q, e):
    phi_n = phiN(p, q)
    d = get_d(e, phi_n)
    return (d, get_modulus(p, q))


def base64_private_key(private_key):
    d, n = private_key
    d_bytes = d.to_bytes((d.bit_length() + 7) // 8, byteorder="big")
    n_bytes = n.to_bytes((n.bit_length() + 7) // 8, byteorder="big")
    key_bytes = d_bytes + n_bytes
    base64_private_key = base64.b64encode(key_bytes).decode("utf-8")
    return base64_private_key


"""
To encrypt a message using RSA, we firstly have e and n for encryption
Next we can get the ciphertext from the plain text by

C = m^e mod n

Firstly, we convert the message character into integer in ASCII values. 
For each character, we encrypt using the given mathematical
"""


# encryption function
def encryption(message, public_key):
    e, n = public_key
    char_message = [ord(character) for character in message]
    encrypted_message_integer = [pow(m, e, n) for m in char_message]

    encrypted_message_bytes = b"".join(
        m.to_bytes((m.bit_length() + 7) // 8, byteorder="big")
        for m in encrypted_message_integer
    )
    encrypted_message = base64.b64encode(encrypted_message_bytes).decode("utf-8")

    return encrypted_message, encrypted_message_integer


"""
To decrypt a message using RSA, we firstly have d and n for decryption
Next we can get the plain text from the given cipher text by

m = C^d mod n
"""


# decryption function
def decryption(encrypted_message_integer, private_key):
    d, n = private_key
    decrypted_char_message = [pow(c, d, n) for c in encrypted_message_integer]
    decrypted_message = "".join([chr(m) for m in decrypted_char_message])
    return decrypted_message


def main():
    p, q = get_p_and_q()
    public_key = get_public_key(p, q)
    private_key = get_private_key(p, q, public_key[0])

    print(base64_public_key(public_key))
    print(base64_private_key(private_key))

    message = "Xin chao"
    print(f"Original message: {message}")

    encrypted_message, encrypted_message_integer = encryption(message, public_key)
    print(f"Encrypted message: {encrypted_message}")

    decrypted_message = decryption(encrypted_message_integer, private_key)
    print(f"Decrypted message: {decrypted_message}")


if __name__ == "__main__":
    main()
