import math
from collections import OrderedDict

class TranspositionTable:
    def __init__(self, size=256):
        self.size = size
        self.table = OrderedDict()

    def get(self, key):
        """Retrieve a value from the transposition table and mark it as recently used."""
        if key in self.table:
            self.table.move_to_end(key)
            return self.table[key]
        return None

    def put(self, key, value):
        """Add a key-value pair to the transposition table, evicting the oldest entry if necessary."""
        if key in self.table:
            self.table.move_to_end(key)
        self.table[key] = value
        if len(self.table) > self.size:
            self.table.popitem(last=