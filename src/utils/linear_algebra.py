from typing import Iterable, overload
from math import sqrt


class Vec3:
    x: float
    y: float
    z: float

    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return f"Vec3({self.x}, {self.y}, {self.z})"

    def __add__(self, other: Vec3 | float) -> Vec3:
        if isinstance(other, Vec3):
            return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
        return Vec3(self.x + other, self.y + other, self.z + other)

    def __radd__(self, other: float) -> Vec3:
        return self + other

    def __iadd__(self, other: Vec3 | float) -> Vec3:
        if isinstance(other, Vec3):
            self.x += other.x
            self.y += other.y
            self.z += other.z
        else:
            self.x += other
            self.y += other
            self.z += other
        return self

    def __sub__(self, other: Vec3 | float) -> Vec3:
        if isinstance(other, Vec3):
            return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)
        return Vec3(self.x - other, self.y - other, self.z - other)

    def __rsub__(self, other: float) -> Vec3:
        return Vec3(other - self.x, other - self.y, other - self.z)

    def __isub__(self, other: Vec3 | float) -> Vec3:
        if isinstance(other, Vec3):
            self.x -= other.x
            self.y -= other.y
            self.z -= other.z
        else:
            self.x -= other
            self.y -= other
            self.z -= other
        return self

    def __neg__(self) -> Vec3:
        return Vec3(-self.x, -self.y, -self.z)

    @overload
    def __mul__(self, other: Vec3) -> float: ...

    @overload
    def __mul__(self, other: float) -> Vec3: ...

    def __mul__(self, other: Vec3 | float) -> float | Vec3:
        if isinstance(other, Vec3):
            return self.x * other.x + self.y * other.y + self.z * other.z
        return Vec3(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other: float) -> Vec3:
        return self * other

    def __truediv__(self, other: float) -> Vec3:
        return Vec3(self.x / other, self.y / other, self.z / other)

    def __itruediv__(self, other: float) -> Vec3:
        self.x /= other
        self.y /= other
        self.z /= other
        return self

    def dot(self, other: Vec3) -> float:
        return self * other

    def __matmul__(self, other: Vec3) -> float:
        return self * other

    def cross(self, other: Vec3) -> Vec3:
        return Vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def length(self) -> float:
        return sqrt(self * self)  # agora mypy entende que é float

    def normalize(self) -> Vec3:
        l = self.length()
        if l == 0:
            raise ValueError("Cannot normalize zero vector")
        return self / l


def sum_vec3(vectors: Iterable[Vec3]) -> Vec3:
    result = Vec3(0.0, 0.0, 0.0)
    for v in vectors:
        result += v
    return result


HAT_I = Vec3(1.0, 0.0, 0.0)
HAT_J = Vec3(0.0, 1.0, 0.0)
HAT_K = Vec3(0.0, 0.0, 1.0)
