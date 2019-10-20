__author__ = 'cpys'

'''
async web application.
'''

import logging;
import sys

logging.basicConfig(level=logging.INFO)

import asyncio, os, json, time
from datetime import datetime

from aiohttp import web


def index(request):
    return web.Response(body=b'<h1>Awesome</h1>', headers={'content-type': 'text/html'})


async def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    logging.info('server started at http://127.0.0.1:9000...')
    return srv

@asyncio.coroutine
def init2(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)
    srv = yield from loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    logging.info('server started at http://127.0.0.1:9000...')
    return srv

# sys.path.append('/Users/cpy/PycharmProjects/FirWepApp/')
print(sys.path)
loop = asyncio.get_event_loop()
loop.run_in_executor(init2(loop))
loop.run_forever()
