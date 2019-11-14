# Test suite for main.py
#
# This file admittedly has a few bugs (writing tests for async
# functions is not really my strong suit), but it shows the
# underlining thoughts and design decisions.
#
# 2019 andreas.helfenstein@hotmail.ch

import asyncio
import aiohttp
import pytest
from bottle import Bottle, request, Response

import main

app = Bottle()


@app.route('/')
def home():
    html = Response("<html><body>Hello world</body></html>")
    return html


def test_strip_html_tags():
    test_cases = [["<i>test text</i>", "test text"],
                  ["text<script>alert();</script>", "text"]]
    for input_, output in test_cases:
        assert main.strip_html_tags(input_) == output


def test_get_writer():
    writer = main.get_writer()
    assert hasattr(writer, "send")


@pytest.mark.asyncio
async def test_get_content():
    app.run(host="0.0.0.0", port=3000)
    url_correct = "http://127.0.0.1:3000"
    url_404 = "http://127.0.0.1:3000/notfound.html"
    url_none = None
    loop = asyncio.get_event_loop()
    async with aiohttp.ClientSession(loop=loop) as client:
        res = await main.get_content(client, url_correct)
        assert res == "Hello world"
        with pytest.raises(ValueError):
            await main.get_content(client, url_404)
        with pytest.raises(TypeError):
            await main.get_content(client, url_none)
    loop.stop()
    loop.close()
    app.close()
