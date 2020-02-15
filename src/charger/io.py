import csv
import functools
import gzip
from contextlib import closing
from pathlib import Path
from typing import Dict, Iterator, List, Union


class unix_tab(csv.excel):
    """The :py:class:`csv.Dialect` to read TSV."""

    delimiter = "\t"
    lineterminator = "\n"


csv.register_dialect("unix_tab", unix_tab)


def read_tsv(
    path: Path, dialect="unix_tab", as_dict=False, columns=None, **kwargs
) -> Union[Iterator[List[str]], Iterator[Dict[str, str]]]:
    """Read a plain-text or gzip compressed TSV table.

    When `as_dict` is False, return each row as a list using :py:func:`csv.reader`.

    When `as_dict` is `True`, return each row as a `dict` mapping from the column name to the corresponding value
    using :py:class:`csv.DictReader`. `columns` will be used as the column names. If `columns` is omitted, the first
    row will be treated as the column names.
    """
    if path.suffix == ".gz":
        file_obj = gzip.open(path, "rt")
    else:
        file_obj = open(path, "rt")
    with closing(file_obj) as f:
        if as_dict:
            yield from csv.DictReader(f, dialect=dialect, fieldnames=columns, **kwargs)
        else:
            yield from csv.reader(f, dialect=dialect, **kwargs)


read_csv = functools.partial(read_tsv, dialect="excel")
read_csv.__doc__ = """
    Read a plain-text or gzip compressed CSV table.

    See :py:func:`read_tsv` for its usage.
    """
