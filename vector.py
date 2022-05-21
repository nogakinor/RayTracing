from numpy import linalg as LNG
import numpy as np
import math


# Declare a vector using np.zeros(3)

def vector_len(v: np.ndarray):
    ret_val = 0
    for i in range(3):
        ret_val += (v.item(i) ** 2)
    return math.sqrt(ret_val)


def normalized(v: np.ndarray):
    norma = LNG.norm(v)
    ret_val = divide(v, norma)
    return ret_val


def divide(v, scalar):
    return np.divide(v, scalar)


def multiply(v, scalar):
    return np.multiply(v, scalar)


def minus(v: np.ndarray, other: np.ndarray):
    return np.subtract(v, other)


def add(v, other):
    return np.add(v, other)


def dot_product(v, other):
    if isinstance(other, np.ndarray) == False:
        other = np.array(other)

    other = other.reshape(3)
    v = v.reshape(3)
    return np.dot(v, other)


def cross_product(v, other):
    return np.cross(v, other)


def negative(v):
    return np.negative(v)


def projected(v, other):
    return multiply(normalized(other), dot_product(v, other) / vector_len(other))


def projected_left(v, other):
    return minus(v, projected(v, other))


def reflect(v, other: np.ndarray):
    v1 = normalized(other)
    return minus(v, multiply(v, 2 * dot_product(v, v1)))


def some_perpendicular(v):
    return normalized(cross_product(v, np.add(v, 7)))
