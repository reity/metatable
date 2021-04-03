"""Extensible table data structure.

Table data structure that supports the introduction of user-defined workflow
combinators and the use of these combinators in concise workflow descriptions.
"""

from __future__ import annotations
import doctest
import itertools
import symbolism

class row: # pylint: disable=R0903
    """
    Symbolic representation of a row index.
    """

class drop: # pylint: disable=R0903
    """
    Symbolic representation of a column drop operation.
    """

class column(symbolism.symbol): # pylint: disable=R0903
    """
    Symbolic representation of a column specified (i.e.,
    a numerical index or an attribute name).
    """

class metatable:
    """
    Class for the extensible metatable data structure.
    """
    @staticmethod
    def _eval(r, i, e):
        """
        Evaluation of a symbolic expression that may contain
        references to specific attributes/columns of a row.
        """
        if isinstance(e, column):
            index = e.evaluate()
            return r[index] if index < len(r) else None

        if e is row:
            return i

        if isinstance(e, symbolism.symbol):
            return\
                e.evaluate()\
                if len(e) == 0 else\
                e.instance(*[metatable._eval(r, i, p) for p in e.parameters])

        return e

    @staticmethod
    def _upd(update_filter_index_row):
        """
        Internal method for the work to be completed for each row
        during an invocation of an update on the table.
        """
        ((update, filter_, column_max), (index, row_)) = update_filter_index_row

        # Fill columns that are in the range but that have no expression
        # in the update tasks.
        for col in update:
            while col > len(row_) - 1:
                row_.append(None)

        drops = [] # Columns to drop once updates are evaluated.
        row__ = list(row_)

        # In strict mode, drop columns which do not appear in the update task.
        if column_max is not None:
            row__ = [v for (c, v) in enumerate(row__) if c <= column_max]

        for (col_, upd) in update.items():
            if upd is not drop:
                row__[col_] = metatable._eval(row_, index, upd)
            else:
                drops.append(col_)

        # Apply filter first and then drop columns.
        if filter_ is None or metatable._eval(row__, index, filter_):
            row__ = [v for (c, v) in enumerate(row__) if c not in drops] # Drop columns.
            return [row__]

        # Row was filtered out.
        return []

    def __init__(self, iterable, name=None, header=False):
        """
        Constructor for a table instance that draws data from an iterable.
        """
        self.iterable = iterable
        self.name = name
        self.header = header

    def __iter__(self):
        """
        An instance of a table is an iterable.
        """
        for row_ in self.iterable:
            yield row_

    def map(self, function, iterable, progress): # pylint: disable=R0201
        """
        Internal method for mapping over the data in the table. This method
        can be redefined in derived classes to change how rows are processed
        (e.g., to introduce multiprocessing).
        """
        return (row for rows in progress(map(function, iterable)) for row in rows)

    def update_filter(
            self, update, filter, header=None, strict=False,
            progress=(lambda *a, **ka: a[0])
        ): # pylint: disable=R0913,W0622
        """
        Update-then-filter operations across the entire table, based on
        symbolic expressions for the update and filter task(s).

        >>> t = metatable([['a', 0], ['b', 1], ['c', 2]])
        >>> t.update_filter({0: column(1)}, column(1) > symbolism.symbol(0))
        [[1, 1], [2, 2]]
        >>> list(t)
        [[1, 1], [2, 2]]
        >>> t = metatable([['a'], ['b'], ['c']])
        >>> t.update_filter({3: row}, column(3) < 2)
        [['a', None, None, 0], ['b', None, None, 1]]
        >>> list(t)
        [['a', None, None, 0], ['b', None, None, 1]]
        """
        (rows_in, rows_out) = (iter(self), [])

        # If the update task is a list (representing the operation that yields
        # each column starting from the left-most one), convert it into a dictionary.
        update = dict(enumerate(update)) if isinstance(update, (tuple, list)) else update

        # Determine the column with the highest index in the update task.
        column_max = max(update.keys())

        # Update the header row if it exists and no replacement header is specified.
        if self.header and header is None:
            for row_ in rows_in:
                # Fill columns that are in the range but that have no expression
                # in the update tasks.
                for col in update:
                    while col > len(row_) - 1:
                        row_.append(None)

                # In strict mode, drop columns which do not appear in the update task.
                if strict:
                    row_ = [v for (c, v) in enumerate(row_) if c <= column_max]

                # Drop columns in header as indicated in update specification.
                drops = [col_ for (col_, upd) in update.items() if upd is drop]
                row_ = [v for (c, v) in enumerate(row_) if c not in drops]

                # Add only this header row.
                rows_out.append(row_)
                break
        elif self.header and header is not None: # A replacement header has been specified.
            rows_in = itertools.islice(rows_in, 1, None) # Skip the old header row.
            rows_out.append(header)

        rows_out.extend(self.map(
            metatable._upd,
            zip(
                itertools.repeat((update, filter, column_max if strict else None)),
                enumerate(rows_in)
            ),
            progress
        ))

        self.iterable = rows_out
        return rows_out

    def update(self, update, header=None, strict=False, progress=(lambda *a, **ka: a[0])):
        """
        Update operation across the entire table, based on a
        symbolic expression for the update task(s).

        >>> t = metatable([['a', 0], ['b', 1], ['c', 2]])
        >>> t.update({0: column(1)}) # Replace first-column value with second-column value.
        [[0, 0], [1, 1], [2, 2]]
        >>> list(t)
        [[0, 0], [1, 1], [2, 2]]
        >>> t = metatable([['char', 'num'], ['a', 0], ['b', 1]], header=True)
        >>> t.update({1: column(0)})
        [['char', 'num'], ['a', 'a'], ['b', 'b']]
        >>> t.update({0: drop})
        [['num'], ['a'], ['b']]
        >>> t.update({0: drop})
        [[], [], []]
        >>> t = metatable([['a', 0, True], ['b', 1, True], ['c', 2, False]])
        >>> t.update([column(1), column(0), drop])
        [[0, 'a'], [1, 'b'], [2, 'c']]
        >>> t = metatable([['c', 'n', 'b'], ['a', 0, True], ['b', 1, True]], header=True)
        >>> t.update([column(1), column(0)], strict=True, header=['n', 'c'])
        [['n', 'c'], [0, 'a'], [1, 'b']]
        >>> t.update([column(1)], strict=True)
        [['n'], ['a'], ['b']]
        >>> t.update([column(0)], strict=True, header=['c'])
        [['c'], ['a'], ['b']]
        >>> t.update({2: 'x'})
        [['c', None, None], ['a', None, 'x'], ['b', None, 'x']]
        >>> t = metatable([['a', 0], ['b'], ['c', 2]])
        >>> t.update({2: symbolism.is_(column(1), None)})
        [['a', 0, False], ['b', None, True], ['c', 2, False]]
        """
        return self.update_filter(update, None, header, strict, progress)

if __name__ == "__main__":
    doctest.testmod() # pragma: no cover
