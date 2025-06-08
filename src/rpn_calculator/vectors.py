import math
from typing import Union

Vector = list[float]


def is_vector(obj):
    return isinstance(obj, list)


def vector_add(a: Vector, b: Vector) -> Vector:
    if len(a) != len(b):
        raise ValueError("Сложение векторов разной длины")
    return [x + y for x, y in zip(a, b)]


def vector_sub(a: Vector, b: Vector) -> Vector:
    if len(a) != len(b):
        raise ValueError("Вычитание векторов разной длины")
    return [x - y for x, y in zip(a, b)]


def vector_neg(v: Vector) -> Vector:
    return [-x for x in v]


def vector_abs(v: Vector) -> float:
    return math.sqrt(sum(x * x for x in v))


def vector_dot(a: Vector, b: Vector) -> float:
    if len(a) != len(b):
        raise ValueError("Скалярное произведение векторов разной длины")
    return sum(x * y for x, y in zip(a, b))


def vector_angle(a: Vector, b: Vector) -> float:
    dot = vector_dot(a, b)
    mag_a = vector_abs(a)
    mag_b = vector_abs(b)
    if mag_a == 0 or mag_b == 0:
        raise ValueError("Невозможно вычислить угол с нулевым вектором")
    cos_theta = max(-1.0, min(1.0, dot / (mag_a * mag_b)))
    return math.acos(cos_theta)


def vector_scalar_mul(v: Vector, s: float) -> Vector:
    return [x * s for x in v]


def parse_vector(token: str) -> Union[float, Vector]:
    token = token.strip()
    if token.startswith("[") and token.endswith("]"):
        if len(token) == 2:
            return []
        return [float(x) for x in token[1:-1].split(",")]
    return float(token)
