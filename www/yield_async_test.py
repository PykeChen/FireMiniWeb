import asyncio, threading
import random

__author_ = "cpy"


def gen():
    """
    模拟yield的使用
    其实receive=yield value包含了3个步骤：
    1、向函数外抛出（返回）value
    2、暂停(pause)，等待next()或send()恢复
    3、赋值receive=MockGetValue() 。 这个MockGetValue()是假想函数，用来接收send()发送进来的值
    :return:
    """
    value = 0
    while True:
        receive = yield value
        if receive == 'e':
            break
        value = 'got:%s' % receive


g = gen()
print(g)

# test1: 无线循环，没有结束
# for i in g:
#     print('next %s' % i)

## test2:循环一定次数，next调用的时候才会执行，第一次返回0,后面返回next got:None，说明迭代内部是通过send(None)来迭代的
for i in range(8):
    print('next %s' % next(g))

## test3: yield第一次得到0,通过send发送数据且继续执行，依次得到hello, 12345,迭代结束
## 这里要特别注意：在启动生成器函数时只能send(None),如果试图输入其它的值都会得到错误提示信息:can't send non-None value to a just-started generator
# print(g.send(8999))
print(g.send(None))
print(g.send('hello'))
print(g.send(123456))
try:
    print(g.send('e'))
except StopIteration as e:
    print('iterator end %s' % e)


# ===================================
#  模拟的是yield from 和yield的区别:
#      1.yield就是将range这个可迭代对象直接返回了。而yield from 解析了range(iterable对象)，将其中每一个Item返回了.
#      yield from iterable本质上等于for item in iterable: yield item的缩写版
# ===================================
def g1():
    yield range(5)


def g2():
    yield from range(5)


it1 = g1()
it2 = g2()
for x in it1:
    print(x)

for x in it2:
    print(x)


def fab(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        # print b
        a, b = b, a + b
        n = n + 1


def f_wrapper(fun_iterable):
    print('start')
    for item in fun_iterable:
        yield item
    print('end')


def f_wrapper2(fun_iterable):
    print('startWrapper2')
    yield from fun_iterable
    print('endWrapper2')


wrap = f_wrapper2(fab(5))
for i in wrap:
    print(i, end=' ')


# ===================================
#  模拟的是asyncio.coroutine和yield from
#  1.asyncio是一个基于事件循环的实现异步I/O的模块
#  2.之前都是我们手工切换协程，现在当声明函数为协程后(coroutine)，我们通过事件循环来调度协程。
#  3.使用yield from asyncio.sleep 两个协程使用的都是同一个线程，通过yield from可以将协程asyncio.sleep的控制权交给事件循环会将控制权交给事件循环，然后挂起当协程，
#    至于何时唤醒asyncio.sleep,接着向后执行代码
#  4.使用time.sleep则就就变成了串行执行了，不存在切换.
# ===================================

@asyncio.coroutine
def smart_fib(n):
    index = 0
    a = 0
    b = 1
    while index < n:
        sleep_secs = random.uniform(0, 0.5)
        yield from asyncio.sleep(sleep_secs)  # 通常yield from后都是接的耗时操作
        # time.sleep(sleep_secs)
        print('Smart one think {} secs to get {}, threadId {}'.format(sleep_secs, b, threading.current_thread().ident))
        a, b = b, a + b
        index += 1


@asyncio.coroutine
def stupid_fib(n):
    index = 0
    a = 0
    b = 1
    while index < n:
        sleep_secs = random.uniform(0, 0.2)
        yield from asyncio.sleep(sleep_secs)  # 通常yield from后都是接的耗时操作
        # time.sleep(sleep_secs)
        print('Stupid one think {} secs to get {}, threadId {}'.format(sleep_secs, b, threading.current_thread().ident))
        a, b = b, a + b
        index += 1


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    tasks = [
        smart_fib(10),
        stupid_fib(10),
    ]
    # awaitableTask = asyncio.wait(tasks)
    # print(type(awaitableTask))
    # loop.run_until_complete(awaitableTask)
    # print('All fib finished.')
    # loop.close()


# ===================================
#  模拟的是async和await-python3.5引入
#
# ===================================
async def mygen(alist):
    """
       :param alist:
       :return: <class 'coroutine'>
    """
    while len(alist) > 0:
        c = random.randint(0, len(alist) - 1)
        print(alist.pop(c))


async def mygen2(alist):
    """
    :param alist:
    :return:<class 'async_generator'>
    """
    while len(alist) > 0:
        c = random.randint(0, len(alist) - 1)
        yield alist.pop(c)


async def mygen3(alist):
    while len(alist) > 0:
        c = random.randint(0, len(alist) - 1)
        print(alist.pop(c), f'threadId {threading.current_thread().ident}')
        await asyncio.sleep(1)


a = ['aa', 'dd', 'xx']
c = mygen(a)
d = mygen2(a)
e = mygen3(a)
print(type(c))
print(type(d))
print(type(e))
strlist = ["ss", "dd", "gg"]
intlist = [1, 2, 5, 6]
c1 = mygen3(strlist)
c2 = mygen3(intlist)
print(c1)
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    tasks = [
        c1,
        c2
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    print('All fib finished.')
    loop.close()
