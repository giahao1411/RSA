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


# d = inverse_modulo(7, 51480)
# print(d * 7 % 51480)
# a = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC/BuycBr+ADK5aiaXtYGjFZMz2pDYc54t4fbfnpY5O/1uOFP3dUjcWxAEiNE0XTwbXPP0CU+UDu1JxNktkQVS+g+SJRVfDegCZZrAR66CqrGzLUJNJ68zT9vwYn6uwvJbxZgiaPiOB8hNZQzsyzDeUXotMRSwxFeeiAmahXVDZHQIDAQAB"
# b = "MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBAL8G7JwGv4AMrlqJpe1gaMVkzPakNhzni3h9t+eljk7/W44U/d1SNxbEASI0TRdPBtc8/QJT5QO7UnE2S2RBVL6D5IlFV8N6AJlmsBHroKqsbMtQk0nrzNP2/Bifq7C8lvFmCJo+I4HyE1lDOzLMN5Rei0xFLDEV56ICZqFdUNkdAgMBAAECgYEAmz35U+N4BYxItXNf0UWkX6bHmzlgcKULh2RD7JFy0Whc817D4PVLp8iqUy3F6Mdke88onpenahz1puPE6TjesH18p7L/rG3/MsfBX89a1jgw2mmI+kRERK4PZXlAv/TJKTCZQHavnViiaVmnl9kNo6DzminTN8uGvhoKdfIcrVECQQDo6MQVkrSaMbRHt69+pZJaizov1LDAXNLCTSjDZhm9GHEwyZBZscCO7AheSL2wT8DtntOlXrjIS3GImnqohAPXAkEA0fcwTHpT453m/bBEqOCwhV+8zIQ1ZdDmwhzWZsmhlZvZnycngFnlL40NgV5tB+I6Ty9dPSoTbZc4mtNmTfbsKwJBAMakl3Bq0jvcfozYPgY/AqbUrgjTVviJcnujQUv+DZ+4c/mPP90v/DIpXy3Czn3MV5iSaKJXOjQiHC/MySZmibsCQAVUwWUvtfGRkMvgLd4b1l+Mjr6inLh5FWLYWJlDhVbHHj9sPxSDM86BRlaCj0Ij/FcGXNewuc2OiWFk/LP+EQECQGpkM1yYzKH2X7RBiiBfp5ETS7GeCTn7HB04vsV0X5svkBz4Awga0pnCtgxKtqtvf5ZlBXulj4qxybIs90rbcnU="
# c = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC/BuycBr+ADK5aiaXtYGjFZMz2pDYc54t4fbfnpY5O/1uOFP3dUjcWxAEiNE0XTwbXPP0CU+UDu1JxNktkQVS+g+SJRVfDegCZZrAR66CqrGzLUJNJ68zT9vwYn6uwvJbxZgiaPiOB8hNZQzsyzDeUXotMRSwxFeeiAmahXVDZHQIDAQAB"
# print(a, "\n")
# print(b, "\n")
# print(c, "\n")
