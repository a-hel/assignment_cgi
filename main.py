# Assignment
#
# 2019 andreas.helfenstein@hotmail.ch

import signal
import sys
import asyncio
import aiohttp
import re
import time
from datetime import datetime
from bs4 import BeautifulSoup


def shutdown(loop, client):
    """Close asyncio loop and http client on keyboard interrupt."""
    loop.create_task(client.close())
    loop.stop()
    sys.exit(0)


def strip_html_tags(raw_text):
    """Remove content from <script> and <style> tags and remove
    all other tags.
    """
    soup = BeautifulSoup(raw_text, "html.parser")
    for tag in [soup.script, soup.style]:
        if tag is not None:
            tag.decompose()
    text = soup.get_text()
    return text


async def get_content(client, url):
    """Get content from url using async http client."""
    if not isinstance(url, str):
        raise TypeError('"%s" is not a valid URL' % url)
    async with client.get(url) as response:
        if not response.status == 200:
            raise ValueError('HTTP response %s' % response.status)
        raw_content = await response.text()
        text_content = strip_html_tags(raw_content)
        return text_content


async def match_regex(client, url, regex, writer):
    """Match content of url with regex, format result and send
    it to writer."""
    error = None
    first_match = None
    match_beginning, match_end = None, None
    start = time.time()
    timestamp = datetime.now()
    try:
        content = await get_content(client, url)
        first_match = re.search(regex, content)
    except aiohttp.client_exceptions.InvalidURL as e:
        error = '"%s" is not a valid URL' % url
    except (ValueError, TypeError) as e:
        error = e
    stop = time.time()
    elapsed = stop - start
    if first_match is not None:
        match_beginning, match_end = first_match.span()
    data = [
        timestamp.strftime('%d/%m/%Y %H:%M:%S.%f'), url, match_beginning,
        match_end, elapsed, error
    ]
    writer.send(data)


def get_writer():
    """Create a file writer.

    For the sake of this exercise, this is just a simple file writer, In
    production, it can easily be replaced with a database writer or similar.
    For the same reason, the name of the output file is hard-coded into the
    function.
    """
    fname = "output.csv"
    headers = [
        'timestamp', 'url', 'match_beginning', 'match_end', 'elapsed_time',
        'error'
    ]
    with open(fname, 'w') as f:
        f.write(', '.join(headers))
        f.write('\n')
        while True:
            data = yield
            f.write(', '.join([str(d) for d in data]))
            f.write('\n')


async def run_loop(urllist, max_coros, client):
    """Schedule and run co-routines for each url in urllist."""
    sem = asyncio.Semaphore(max_coros)
    writer = get_writer()
    writer.send(None)
    async with sem:
        for url, regex in urllist:
            asyncio.gather(match_regex(client, url, regex, writer))


def main(urllist, max_coros=10):
    """
    Match the content of a list of urls with corresponding regular
    expressions and write the result into a file.

    Arguments:

    urllist (iterable of iterables):    Pairs of (url, regexp)
    max_coros (int, default=10):        Maximum number of co-routines
                                        to be run simultaneously.

    Returns:
    None

    Example:

    main([['www.hs.fi', 'Helsinki'],['www.is.fi', '"^Foo.*bar$"']])

    Remarks:

    This function runs an infinite loop. To interrupt it, use Ctrl+C.

    The urllist parameter does not need to be a list, it can also be
    e.g. a generator expression that retrieves data periodically from
    e.g. a database and pipes it into the function.
    """
    loop = asyncio.get_event_loop()
    client = aiohttp.ClientSession(loop=loop)
    loop.add_signal_handler(
        signal.SIGINT, lambda: asyncio.create_task(shutdown(loop, client)))
    loop.create_task(run_loop(urllist, max_coros, client))
    loop.run_forever()


if __name__ == '__main__':
    urllist = [['https://www.hs.fi',
                'Helsinki'], ['https://www.is.fi', 'koti'],
               ['www.unknown_url.xy', 'example'], [56, 'example'],
               [None, 'example'], ['http://www.cgi.fi/error_code', 'example']]
    main(urllist)