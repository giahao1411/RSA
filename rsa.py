import base64
import sympy as sp
from modulo_inverse import extended_euclidean, modulo_inverse


# Generate primes randomly using sympy randprime
def generate_rand_prime(bit_length):
    return sp.randprime(2 ** (bit_length - 1), 2**bit_length)


# Get p and q randomly, note that p and q are primes so we check before get them
def get_p_and_q(bit_length):
    # Get random primes for p and q in given bit length
    p = generate_rand_prime(bit_length)
    q = generate_rand_prime(bit_length)

    return p, q


# get modulus n = p * q for encryption and decryption
def get_modulus(p, q):
    return p * q


# Calculate notient Φ(n) = (p - 1) * (q - 1)
def phiN(p, q):
    return (p - 1) * (q - 1)


"""
exponent_e often starts with e ∈ {3, 5, 17, 257, 65537} which are special primes
These exponents have computational benefits as they are of the form 2k + 1
But for small exponents, especially e = 3, it will be easily for being attacked

number e is less than n (modulus), such that n is relatively prime to (p - 1) * (q - 1)
have no common factor except 1 which is GCD(e, phiN) = 1

e is defined by 1 < e < Φ(n)

The most common exponent e = 65537 for encryption for the higher security 
"""


# Get encryption key e
def get_exponent_e(phiN):
    # Using a common set of prime numbers for efficiency
    common_primes = [3, 5, 17, 257, 65537]
    for e in common_primes:
        if extended_euclidean(e, phiN)[0] == 1:
            return e

    # Back to custome search if common primes are not suitable
    for e in range(2, phiN):
        if extended_euclidean(e, phiN)[0] == 1:
            return e
    return -1


"""
we have e * d = k * Φ(n) + 1 which is e * d mod Φ(n) = 1
can be noted that d ≡ e^(-1) mod Φ(n)
which is d is the inverse modulo of e mod Φ(n). We reuse the pre-defined function in inverse_modulo.py
"""


# Get decryption key
def get_d(e, phiN):
    return modulo_inverse(e, phiN)


# public key taking e and n (e, n)
def get_public_key(p, q):
    n = get_modulus(p, q)
    phi_n = phiN(p, q)
    e = get_exponent_e(phi_n)

    # Most common exponent e
    # e = 65537
    return (e, n)


# private key taking d and n (d, n)
def get_private_key(p, q, e):
    phi_n = phiN(p, q)
    d = get_d(e, phi_n)
    return (d, get_modulus(p, q))


# Convert keys to base64
def base64_key(key):
    a, b = key
    a_bytes = a.to_bytes((a.bit_length() + 7) // 8, byteorder="big")
    b_bytes = b.to_bytes((b.bit_length() + 7) // 8, byteorder="big")
    key_bytes = a_bytes + b_bytes
    return base64.b64encode(key_bytes).decode("utf-8")


"""
To encrypt a message using RSA, we firstly have e and n for encryption
Next we can get the cipher text from the plain text by

C = m^e mod n

Firstly, we convert the message character into integer in ASCII values. 
For each character, we encrypt using the given mathematical definition
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
    bit_length = 2048
    p, q = get_p_and_q(bit_length)
    public_key = get_public_key(p, q)
    private_key = get_private_key(p, q, public_key[0])

    # public_key, private_key = get_key_pairs(2048)

    print("PUBLIC KEY:\n", base64_key(public_key), "\n")
    print("PRIVATE KEY:\n", base64_key(private_key), "\n")

    message = "Xin chao"
    print(f"Original message:\n {message}\n")

    encrypted_message, encrypted_message_integer = encryption(message, public_key)
    print(f"Encrypted message:\n {encrypted_message}\n")

    decrypted_message = decryption(encrypted_message_integer, private_key)
    print(f"Decrypted message:\n {decrypted_message}\n")


if __name__ == "__main__":
    main()
