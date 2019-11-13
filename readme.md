# Assignment

## Installation

Requires at least Python 3.7

```sh
pip3 install -f requirements.txt
```

To test, run

```sh
python3 main.py
```

## Usage

### Function `main(urllist, max_coros=10)`

Match the content of a list of urls with corresponding regular
expressions and write the result into a file (output.csv).

####Arguments:####

urllist _(iterable of iterables)_:    Pairs of (url, regexp)
max_coros _(int, default=10)_:        Maximum number of co-routines
                                    to be run simultaneously.

####Returns:####

`None`

####Example:####

```
main([['www.hs.fi', 'Helsinki'],['www.is.fi', '"^Foo.*bar$"']])
```

####Remarks:####

This function runs an infinite loop. To interrupt it, use **Ctrl+C**.

The urllist parameter does not need to be a list, it can also be
e.g. a generator expression that retrieves data periodically from
e.g. a database and pipes it into the function.

