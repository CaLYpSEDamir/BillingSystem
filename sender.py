import json
import aiohttp
import asyncio
from functools import wraps
from time import time


def timeit(func):
    @wraps(func)
    def _time_it(*args, **kwargs):
        start = int(round(time() * 1000))
        try:
            return func(*args, **kwargs)
        finally:
            end_ = int(round(time() * 1000)) - start
            print(f"Total execution time: {end_ if end_ > 0 else 0} ms")

    return _time_it


async def fetch(session, url, data):
    """Execute an http call async
    Args:
        session: contexte for making the http call
        url: URL to call
    Return:
        responses: A dict like object containing http response
    """
    # data = json.dumps({'amount': 1})
    data = json.dumps(data)
    async with session.post(url, data=data) as response:
        resp = await response.json()
        # print(resp)
        return resp


async def fetch_all(count):
    """ Gather many HTTP call made async
    Args:
        cities: a list of string
    Return:
        responses: A list of dict like object containing http response
    """
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(count):
            # user_id = 1
            # to_user = 2
            # user_id = 2 - (i % 2)
            # to_user = 3 - user_id

            if i % 3 == 0:
                user_id = 1
                to_user = 2

            elif i % 3 == 1:
                user_id = 2
                to_user = 3

            elif i % 3 == 2:
                user_id = 1
                to_user = 3

            data = {'amount': 100, 'to_user': to_user}
            tasks.append(
                fetch(
                    session,
                    # f"http://127.0.0.1:8000/users/{user_id}/add_money/",
                    f"http://127.0.0.1:8000/users/{user_id}/transfer_money/",
                    data,
                )
            )
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        return responses


@timeit
def run(n):
    responses = asyncio.run(fetch_all(n))
    return responses


############################################

async def wait(i):
    if i == 1:
        raise
    await asyncio.sleep(1)
    print('asd')


async def run_errors():
    tasks = [wait(i) for i in range(5)]
    responses = await asyncio.gather(*tasks, return_exceptions=True)
    return responses


def check_errors():
    r = asyncio.run(run_errors())
    print(r)


if __name__ == '__main__':
    run(3)
