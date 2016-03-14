#!/usr/bin/env python

from agate.aggregations.base import Aggregation
from agate.data_types import Boolean


class Any(Aggregation):
    """
    Returns :code:`True` if any value in a column passes a truth test. The
    truth test may be omitted when testing :class:`.Boolean` data.

    :param test:
        A function that takes a value and returns `True` or `False`.
    """
    def __init__(self, column_name, test=None):
        self._column_name = column_name
        self._test = test

    def get_aggregate_data_type(self, table):
        return Boolean()

    def validate(self, table):
        column = table.columns[self._column_name]

        if not isinstance(column.data_type, Boolean) and not self._test:
            raise ValueError('You must supply a test function for columns containing non-Boolean data.')

    def run(self, table):
        column = table.columns[self._column_name]
        data = column.values()

        if isinstance(column.data_type, Boolean):
            return any(data)

        return any(self._test(d) for d in data)