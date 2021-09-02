from itertools import zip_longest

from utils.constants import NOT_SET


class UniqueIterator:
    def __init__(self, iterator):
        self.iterator = iterator
        self.consumed_items = set()

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            try:
                item = next(self.iterator)
            except TypeError as err:
                raise StopIteration

            if item in self.consumed_items:
                continue

            self.consumed_items.add(item)
            return item


def first(filter_function, collection, default=NOT_SET):
    """
    Return the first item from the collection that meets the filter_function.

    It is implemented using an iterator, so it raises StopIteration if nothing is found
    and no default value is specified
    """
    filtered = filter(filter_function, collection)
    if default is NOT_SET:
        return next(filtered)
    return next(filtered, default)


def in_chunks(iterable, n, fillvalue=None):
    """
    Collect data into fixed-length chunks or blocks
    >>> list(in_chunks('ABCDEFG',3,'x'))
    ["ABC", "DEF", "Gxx"]
    """
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)
