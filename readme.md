# Assignment

## Introduction

This is a submission to CGI's recruitment assignment. It's main focus is on simplicity. Before pushing it into production, it is advisable to replace the file writer with a database writer, for example using `asyncpg` or `aiomysql`drivers for even more asyncio fun.

2019 [Andreas Helfenstein](andreas.helfenstein@hotmail.ch)

## Installation

Requires at least Python 3.7

```sh
pip install -r requirements.txt
```

To test, run

```sh
python main.py
```

## Usage

### Function `main(urllist, max_coros=10)`

Match the content of a list of urls with corresponding regular
expressions and write the result into a file (output.csv).

**Arguments:**

- urllist _(iterable of iterables)_:    Pairs of (url, regexp)
- max_coros _(int, default=10)_:        Maximum number of co-routines to be run simultaneously.

**Returns:**

`None`

**Example:**

```
main([['www.hs.fi', 'Helsinki'],['www.is.fi', '"^Foo.*bar$"']])
```

**Remarks:**

This function runs an infinite loop. To interrupt it, use **Ctrl+C**.

The `urllist` parameter does not need to be a list, it can be any iterable, e.g. a generator expression that retrieves data periodically from a database or another external source and pipes it into the function.

