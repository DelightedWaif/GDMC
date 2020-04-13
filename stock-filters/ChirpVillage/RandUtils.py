# coding=utf-8
"""
    RandUtils.py
    Randomized Utils
        Used for generating random numbers
    Author: Chirp Nets
    © 2020
"""


def lehmer_prng(seed):
    """
    Implementation of the lehmer random number generator
    :params seed: the seed to generate number with
    :returns: the generated integer from the seed using lehmer
    """
    tmp = seed * 0x4a39b70d
    m1 = ((tmp >> 32) ^ tmp)
    tmp = m1 * 0x12fad5c9
    m2 = ((tmp >> 32) ^ tmp)
    return m2


def lehmer_2(x, y):
    """
    Use Lehmer Random number generator to generate random number from 2 seeds
    :params x: seed one
    :params y: seed two
    :returns: random number generated from seeds
    """
    return lehmer_prng(lehmer_prng(x) ^ y)


def rand_range(x, y, max, min):
    """
    Generate random number within a range
    :params x: seed one
    :params y: seed two
    :params max: max range
    :params min:  min range
    :returns: Generated random number within the range
    """
    return lehmer_2(x, y) % (max - min) + 1 + min


# DEMO Code
if __name__ == "__main__":
    test_x, test_y = 4, 8
    print("Test 1: " + str(lehmer_2(test_x, test_y)))
    test_x, test_y = 4, 4
    print("Test 2: " + str(lehmer_2(test_x, test_y)))
    test_x, test_y = 4, 8
    print("Test 3: " + str(lehmer_2(test_x, test_y)))

    seed = 2523870351887443968
    i, j = 45, 63
    print("Test 4: " + str(float(((lehmer_2(lehmer_2(seed, i), j)) % 100)) / 100))
    i, j = 43, 1
    print("Test 5: " + str(float(((lehmer_2(lehmer_2(seed, i), j)) % 100)) / 100))
    i, j = 45, 63
    print("Test 6: " + str(float(((lehmer_2(lehmer_2(seed, i), j)) % 100)) / 100))

    x, z = 34, 45
    print("Test 7: " + str(float(rand_range(x, z, 230, 170))/100))
    x, z = 24, 173
    print("Test 7: " + str(float(rand_range(x, z, 230, 170))/100))
