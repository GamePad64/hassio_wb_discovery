from typing import Any


class Tree(dict):
    def __missing__(self, key: Any) -> Any:
        value = self[key] = type(self)()
        return value
