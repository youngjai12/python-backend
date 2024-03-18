from concurrent.futures.process import ProcessPoolExecutor

import requests
from bs4 import BeautifulSoup
from non_blocking_client import NonBlockingRestClient, RestClientRequest
from time import sleep
from aiohttp import ClientSession
import asyncio

def parse(req_text, selector=None):
    soup_obj_local = BeautifulSoup(req_text, "lxml")
    if selector is None:
        selector = '#divDaechaQ > table > tbody > tr:nth-child(48) > td:nth-child(5)'
    elem = soup_obj_local.select_one(selector).text
    if elem is None:
        return None
    sleep(1.5)
    rst = elem.strip()
    if not rst:
        return None
    return rst


async def async_parse(req_text):
    selector = '#divDaechaQ > table > tbody > tr:nth-child(48) > td:nth-child(5)'
    soup_obj_local = BeautifulSoup(req_text, "lxml")
    elem = soup_obj_local.select_one(selector).text
    if elem is None:
        return None
    sleep(1.5)
    rst = elem.strip()
    if not rst:
        return None
    return rst

# non-blocking 하게끔 async하게 호출한것임.
async def single_fetch(stock_cd):
    target_url_local = NonBlockingRestClient.get_stock_request_url(stock=stock_cd)
    async with ClientSession() as session:
        async with session.get(target_url_local) as response:
            return await response.text()




def process_by_one(a_stock):
    async def execute_by_a_stock():
        html = await single_fetch(a_stock)
        data = await async_parse(html, selector='#divDaechaQ > table > tbody > tr:nth-child(48) > td:nth-child(5)')
        print(data)

    asyncio.run(execute_by_a_stock())

async def fetch_multi_as_async(test_stocks_list):
    requests = nb_client.arequests(
        [RestClientRequest(method="GET", path=nb_client.get_stock_request_url(a_stock))
         for a_stock in test_stocks_list]
    )
    return [a.text for a in await requests]


def process_by_batch(test_stocks_list):
    reqs = nb_client.requests(
        [RestClientRequest(method="GET", path=nb_client.get_stock_request_url(a_stock))
         for a_stock in test_stocks_list]
    )
    with ProcessPoolExecutor(max_workers=3) as executor:
        parsed_results = list(executor.map(parse, [a.text for a in reqs]))
    return parsed_results



async def process_by_multi_at_async(test_stocks_list):
    async_results = await fetch_multi_as_async(test_stocks_list)

    with ProcessPoolExecutor(max_workers=3) as executor:
        parsed_results = list(executor.map(parse, async_results))
    return parsed_results

if __name__ == "__main__":
    nb_client = NonBlockingRestClient()
    target_url = NonBlockingRestClient.get_stock_request_url(stock="005930")
    single_result = requests.get(url=target_url)
    # print(single_result.text)

    # soup_obj = BeautifulSoup(single_result.text, "lxml")
    # parsed_result = parse(soup_obj, selector=f'#divDaechaQ > table > tbody > tr:nth-child(48) > td:nth-child(5)')
    # print(parsed_result)
    target_stocks = ['005930', '064090', '068760', '079190', '093240', '109080', '144510', '194480', '197140', '214420',
                      '224110', '235980', '297090', '298020', '001440', '014190', '041020', '075130', '084870',
                      '085810', '196300', '213420', '900110', '008600', '013360', '014830', '025550', '039020',
                      '069410', '069730', '138490', '238200', '290720', '298000', '298050', '900300', '004690',
                      '013000', '017390', '020400']

    #process_by_one("005930")
    #results =process_by_multi(target_stocks) # 이러면 return되는 객체가 coroutine object process_by_multi at 0x103ea9340>


    results_async = asyncio.run(process_by_multi_at_async(target_stocks))


    results = process_by_batch(target_stocks)
    print(results)
