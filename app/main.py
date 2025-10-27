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
        if not self.min_amount <= value <= self.max_amount:
            raise ValueError
        setattr(instance, self.protected_name, value)

    def validate(self, value: int) -> bool:
        return (isinstance(value, int)
                and self.min_amount <= value <= self.max_amount)


class Visitor:
    def __init__(
            self,
            name: str,
            age: int,
            height: int,
            weight: int
    ) -> None:
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight


class SlideLimitationValidator(ABC):
    def __init__(self) -> None:
        pass

    def validate(self, visitor: Visitor) -> bool:
        raise NotImplementedError


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__()
        self.age_range = IntegerRange(4, 14)
        self.height_range = IntegerRange(80, 120)
        self.weight_range = IntegerRange(20, 50)

    def validate(self, visitor: Visitor) -> bool:
        return (
            self.age_range.validate(visitor.age)
            and self.height_range.validate(visitor.height)
            and self.weight_range.validate(visitor.weight)
        )


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__()
        self.age_range = IntegerRange(14, 60)
        self.height_range = IntegerRange(120, 220)
        self.weight_range = IntegerRange(50, 120)

    def validate(self, visitor: Visitor) -> bool:
        return (
            self.age_range.validate(visitor.age)
            and self.height_range.validate(visitor.height)
            and self.weight_range.validate(visitor.weight)
        )


class Slide:
    def __init__(self, name: str, limitation_class: type) -> None:
        self.name = name
        self.limitation = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        return self.limitation.validate(visitor)
