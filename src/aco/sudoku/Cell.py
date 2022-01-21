class Cell:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.value_set = {1, 2, 3, 4, 5, 6, 7, 8, 9}

    def set_fixed_value(self, value: int) -> None:
        self.value_set = {value}

    def eliminate(self, value: int) -> None:
        self.value_set.remove(value)

    def has_fixed_value(self) -> bool:
        return len(self.value_set) == 1

    def is_failed(self) -> bool:
        return len(self.value_set) == 0

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value) -> None:
        self._x = value

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, value) -> None:
        self._y = value

    @property
    def value_set(self) -> set:
        return self._value_set

    @value_set.setter
    def value_set(self, value: set) -> None:
        self._value_set = value

    def __repr__(self) -> str:
        repr_list = [str(v) for v in self.value_set] if self.value_set else ' '
        return "".join(repr_list)
