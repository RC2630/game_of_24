from __future__ import annotations
from typing import Any

class RationalNumber:

    def __init__(self, numerator: int, denominator: int = 1) -> None:
        assert denominator != 0
        self.numerator: int = numerator
        self.denominator: int = denominator

    def __add__(self, other: RationalNumber) -> RationalNumber:
        if self.denominator == other.denominator:
            return RationalNumber(self.numerator + other.numerator, self.denominator)
        return RationalNumber(
            self.numerator * other.denominator + self.denominator * other.numerator,
            self.denominator * other.denominator
        )

    def __sub__(self, other: RationalNumber) -> RationalNumber:
        if self.denominator == other.denominator:
            return RationalNumber(self.numerator - other.numerator, self.denominator)
        return RationalNumber(
            self.numerator * other.denominator - self.denominator * other.numerator,
            self.denominator * other.denominator
        )

    def __mul__(self, other: RationalNumber) -> RationalNumber:
        return RationalNumber(
            self.numerator * other.numerator,
            self.denominator * other.denominator
        )

    def __truediv__(self, other: RationalNumber) -> RationalNumber:
        if other.numerator == 0:
            raise ZeroDivisionError()
        return RationalNumber(
            self.numerator * other.denominator,
            self.denominator * other.numerator
        )
    
    def compute(self) -> float:
        return self.numerator / self.denominator
    
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, RationalNumber):
            return False
        return self.numerator * other.denominator == self.denominator * other.numerator
    
    def approx_equal(self, other: int | float, tol: float = 1e-9) -> bool:
        return abs(self.compute() - other) < tol
    
    def __str__(self) -> str:
        if self.denominator == 1:
            return f"{self.numerator}"
        else:
            return f"{self.numerator} / {self.denominator}"
        
    def __repr__(self) -> str:
        return f"RationalNumber({self.numerator}, {self.denominator})"