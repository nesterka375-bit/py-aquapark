from abc import ABC
from typing import Any


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Any, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: Any, owner: Any) -> Any:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Any, value: Any) -> None:
        if not isinstance(value, int):
            raise TypeError
        if not self.min_amount < value < self.max_amount:
            raise ValueError
        setattr(instance, self.protected_name, value)


class Visitor:
    def __init__(self, name: str, age: int, height: int, weight: int) -> None:
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight


class SlideLimitationValidator(ABC):
    def validate(self, visitor: Visitor) -> bool:
        raise NotImplementedError


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def validate(self, visitor: Visitor) -> bool:
        return (
            4 <= visitor.age <= 14
            and 80 <= visitor.height <= 120
            and 20 <= visitor.weight <= 50
        )


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def validate(self, visitor: Visitor) -> bool:
        return (
            14 <= visitor.age <= 60
            and 120 <= visitor.height <= 220
            and 50 <= visitor.weight <= 120
        )


class Slide:
    def __init__(self, name: str, limitation_class: type) -> None:
        self.name = name
        self.limitation = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        return self.limitation.validate(visitor)
