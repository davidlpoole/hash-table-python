from typing import NamedTuple, Any


class Pair(NamedTuple):
    key: Any
    value: Any


class HashTable:
    def __init__(self, capacity):
        self.capacity = capacity
        self.pairs = capacity * [None]

    def _index(self, key):
        return hash(key) % len(self)

    def __len__(self):
        return len(self.pairs)

    def __setitem__(self, key, value):
        self.pairs[self._index(key)] = Pair(key, value)

    def __delitem__(self, key):
        if key in self:
            self.pairs[self._index(key)] = None
        else:
            raise KeyError(key)

    def __getitem__(self, key):
        pair = self.pairs[self._index(key)]
        if pair is None:
            raise KeyError(key)
        else:
            return pair.value

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __contains__(self, key):
        try:
            self[key]
        except KeyError:
            return False
        else:
            return True
