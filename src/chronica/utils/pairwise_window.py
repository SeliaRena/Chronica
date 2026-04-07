from typing import Generic, NamedTuple, TypeVar
from dataclasses import dataclass

T = TypeVar('T')

class PairView(NamedTuple, Generic[T]):
    first: T
    second: T

@dataclass
class PairwiseWindow(Generic[T]):
    """
    ### A class that simulates a sliding window of size 2 (pairwise) over a stream of data. \n
    The window holds the most recent two items of type T. \n
    
    <b> The 2 most significant methods are slide_forward() and assign_front(). </b> \n
    
    <i> slide_forward(item) </i> provides a simulation of moving the window forward by one step in a stream of data. \n
    <i> assign_front(item) </i> allows you to assign/overwrite a value to the front of the window without changing the back.
    """
    
    front: T | None = None
    back: T | None = None
    
    # ex. [1, 2] -> slide_forward(3) -> [2, 3]
    def slide_forward(self, item: T | None):
        self.front = self.back
        self.back = item
        
    def assign_front(self, item: T | None):
        self.front = item
        
    def size_non_none(self) -> int:
        return sum(x is not None for x in (self.front, self.back))
    
    def is_empty(self) -> bool:
        return self.front is None and self.back is None
    
    def is_full(self) -> bool:
        return self.front is not None and self.back is not None
    
    def clear(self):
        self.front = None
        self.back = None
    
    @property
    def secured_full_snapshot(self) -> PairView[T] | None:
        """
        ### Standard method to access all elements in the window as a pair (Read Only). \n

        Returns:
            Optional[PairView[T]]: A PairView containing the elements in the window if the window is full, otherwise None.
        """
        if not self.is_full():
            return None
        return PairView(first=self.front, second=self.back)
    
    @property
    def appearance(self) -> PairView[T | None]:
        """
        ### Unsafe method to access all elements in the window as a pair (Read Only). \n
        You may get None values in the PairView if the window is not full.
        This is useful in scenarios where you don't care about the fullness of the window. \n
        <i> ex. You just want to inspect the current state of the window regardless of whether it's full or not. </i>

        Returns:
            PairView[T | None]: A PairView containing the current appearance of the window,
            which may include None values if the window is not full.
        """
        return PairView(first=self.front, second=self.back)