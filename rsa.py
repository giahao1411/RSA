import time
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


def measure_time(message, public_key, private_key):
    start_enc = time.perf_counter()
    _, encrypted_message_integer = encryption(message, public_key)
    end_enc = time.perf_counter()

    start_dec = time.perf_counter()
    _ = decryption(encrypted_message_integer, private_key)
    end_dec = time.perf_counter()

    enc_time = end_enc - start_enc
    dec_time = end_dec - start_dec

    return enc_time, dec_time


def write_data_to_file(filename, data):
    with open(filename, "a") as file:
        length, enc_time, dec_time = data
        file.write(f"{length}|{enc_time:.6f}|{dec_time:.6f}\n")


def write_information(filename, data):
    with open(filename, "a") as file:
        public_key, private_key, original_msg, encrpyted_msg, decrypted_msg = data
        file.write(
            f"---PUBLIC KEY---\n{public_key}\n"
            f"\n---PRIVATE KEY---\n{private_key}\n"
            f"\n---ORIGINAL MESSAGE---\n{original_msg}\n"
            f"\n---ENCRYPTED MESSAGE---\n{encrpyted_msg}\n"
            f"\n---DECRYPTED MESSAGE---\n{decrypted_msg}\n"
            "\n-----------------------------------------------\n\n"
        )


def main():
    bit_length = 2048
    p, q = get_p_and_q(bit_length)
    public_key = get_public_key(p, q)
    private_key = get_private_key(p, q, public_key[0])

    # Original message
    message = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. Nam quam nunc, blandit vel, luctus pulvinar, hendrerit id, lorem. Maecenas nec odio et ante tincidunt tempus. Donec vitae sapien ut libero venenatis faucibus. Nullam quis ante. Etiam sit amet orci eget eros faucibus tincidunt. Duis leo. Sed fringilla mauris sit amet nibh. Donec sodales sagittis magna. Sed consequat, leo eget bibendum sodales, augue velit cursus nunc, quis gravida magna mi a libero. Fusce vulputate eleifend sapien. Vestibulum purus quam, scelerisque ut, mollis sed, nonummy id, metus. Nullam accumsan lorem in dui. Cras ultricies mi eu turpis hendrerit fringilla. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; In ac dui quis mi consectetuer lacinia. Nam pretium turpis et arcu. Duis arcu tortor, suscipit eget, imperdiet nec, imperdiet iaculis, ipsum. Sed aliquam ultrices mauris. Integer ante arcu, accumsan a, consectetuer eget, posuere ut, mauris. Praesent adipiscing. Phasellus ullamcorper ipsum rutrum nunc. Nunc nonummy metus. Vestibulum volutpat pretium libero. Cras id dui. Aenean ut eros et nisl sagittis vestibulum. Nullam nulla eros, ultricies sit amet, nonummy id, imperdiet feugiat, pede. Sed lectus. Donec mollis hendrerit risus. Phasellus nec sem in justo pellentesque facilisis. Etiam imperdiet imperdiet orci. Nunc nec neque. Phasellus leo dolor, tempus non, auctor et, hendrerit quis, nisi. Curabitur ligula sapien, tincidunt non, euismod vitae, posuere imperdiet, leo. Maecenas malesuada. Praesent congue erat at massa. Sed cursus turpis vitae tortor. Donec posuere vulputate arcu. Phasellus accumsan cursus velit. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Sed aliquam, nisi quis porttitor congue, elit erat euismod orci, ac placerat dolor lectus quis orci. Phasellus consectetuer vestibulum elit. Aenean tellus metus, bibendum sed, posuere ac, mattis non, nunc. Vestibulum fringilla pede sit amet augue. In turpis. Pellentesque posuere. Praesent turpis. Aenean posuere, tortor sed cursus feugiat, nunc augue blandit nunc, eu sollicitudin urna dolor sagittis lacus. Donec elit libero, sodales nec, volutpat a, suscipit non, turpis. Nullam sagittis. Suspendisse pulvinar, augue ac venenatis condimentum, sem libero volutpat nibh, nec pellentesque velit pede quis nunc. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Fusce id purus. Ut varius tincidunt libero. Phasellus dolor. Maecenas vestibulum mollis diam. Pellentesque ut neque. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. In dui magna, posuere eget, vestibulum et, tempor auctor, justo. In ac felis quis tortor malesuada pretium. Pellentesque auctor neque nec urna. Proin sapien ipsum, porta a, auctor quis, euismod ut, mi. Aenean viverra rhoncus pede. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Ut non enim eleifend felis pretium feugiat. Vivamus quis mi. Phasellus a est. Phasellus magna. In hac habitasse platea dictumst. Curabitur at lacus ac velit ornare lobortis. Curabitur a felis in nunc fringilla tristique. Morbi mattis ullamcorper velit. Phasellus gravida semper nisi. Nullam vel sem. Pellentesque libero tortor, tincidunt et, tincidunt eget, semper nec, quam. Sed hendrerit. Morbi ac felis. Nunc egestas, augue at pellentesque laoreet, felis eros vehicula leo, at malesuada velit leo quis pede. Donec interdum, metus et hendrerit aliquet, dolor diam sagittis ligula, eget egestas libero turpis vel mi. Nunc nulla. Fusce risus nisl, viverra et, tempor et, pretium in, sapien. Donec venenatis vulputate lorem. Morbi nec metus. Phasellus blandit leo ut odio. Maecenas ullamcorper, dui et placerat feugiat, eros pede varius nisi, condimentum viverra felis nunc et lorem. Sed magna purus, fermentum eu, tincidunt eu, varius ut, felis. In auctor lobortis lacus. Quisque libero metus, condimentum nec, tempor a, commodo mollis, magna. Vestibulum ullamcorper mauris at ligul"

    # Encrypted message
    encrypted_message, encrypted_message_integer = encryption(message, public_key)

    # Decrypted message
    decrypted_message = decryption(encrypted_message_integer, private_key)

    # Calculate time of encrypt and decrypt
    enc_time, dec_time = measure_time(message, public_key, private_key)

    # Data setting for write to files
    message_data = [
        base64_key(public_key),
        base64_key(private_key),
        message,
        encrypted_message,
        decrypted_message,
    ]
    data = [len(message), enc_time, dec_time]

    # Perform write to files
    write_information("keys_and_messages.txt", message_data)
    write_data_to_file("result_data.txt", data)


if __name__ == "__main__":
    main()
