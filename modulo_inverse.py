# Returns the gcd of a and b, and x, y such that ax + by = gcd(a, b)
def extended_euclidean(a, b):
    # Base Case
    if a == 0:
        return b, 0, 1

    gcd, x1, y1 = extended_euclidean(b % a, a)

    # Update x and y using results of recursive
    x = y1 - (b // a) * x1
    y = x1

    return gcd, x, y


def modulo_inverse(a, m):
    # calculate a * b (mod m)
    gcd, x, y = extended_euclidean(a, m)

    # if gcd(a, m) = 1, there is a x modular inverse of a modulo m
    if gcd != 1:
        raise ValueError(f"Inverse doesn't exist for {a} modulo {m}")
    else:
        return x % m


print(modulo_inverse(4, 1000000))