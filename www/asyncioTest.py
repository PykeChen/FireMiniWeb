import asyncio, threading, time


@asyncio.coroutine
def hello():
    print('Hello world! (%s)' % threading.currentThread())
    yield from asyncio.sleep(1)
    print('Hello again! (%s)' % threading.currentThread())


# loop = asyncio.get_event_loop()
# tasks = [hello(), hello()]
# loop.run_until_complete(asyncio.wait(tasks))
# loop.close()


@asyncio.coroutine
def wget(host):
    print('wget %s... (%s)' % (host, threading.current_thread()))
    connect = asyncio.open_connection(host, 80)
    reader, writer = yield from connect
    header = 'GET / HTTP/1.0\r\nHost: %s\r\n\r\n' % host
    # header = 'GET / HTTP/1.0\r\n'
    writer.write(header.encode('utf-8'))
    yield from writer.drain()
    while True:
        line = yield from reader.readline()
        if line == b'\r\n':
            break
        print('%s header > %s (%s)' % (host, line.decode('utf-8').rstrip(), threading.current_thread()))
    # Ignore the body, close the socket
    writer.close()

# typea = asyncio.sleep(1)
# print(type(typea))
print('time = ', time.time(), len('11100100100100000111000110100110111110011101'))
loop = asyncio.get_event_loop()
tasks = [wget(host) for host in ['www.sina.com.cn', 'www.sohu.com', 'www.163.com']]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
