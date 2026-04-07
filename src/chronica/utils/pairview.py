from typing import TypeVar, Generic, NamedTuple

T = TypeVar('T')

class PairView(NamedTuple, Generic[T]):
    first: T
    second: T