import www.orm as orm
from www.models import User
import asyncio, logging

logging.basicConfig(level=logging.DEBUG)


async def test(loop2):
    logging.info("test start...")
    await orm.create_pool(loop=loop2, user='cpy', password='wawj', db='awesome')
    # logging.info("pool %s", pool)
    u = User(name='Test6', email='test6@139.com', passwd='1234567890', image='about:image')
    await u.save()
    await orm.destory_pool()


loop = asyncio.get_event_loop()
loop.run_until_complete(test(loop))
# loop.run_forever()
loop.close()

# for x in test():
#     # print('xx:::' + str(x))
#     pass
