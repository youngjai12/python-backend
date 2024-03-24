from collections import defaultdict
from concurrent.futures.process import ProcessPoolExecutor

import requests
from bs4 import BeautifulSoup
from non_blocking_client import NonBlockingRestClient, RestClientRequest
from time import sleep, time
from aiohttp import ClientSession
import asyncio
from datetime import datetime
from functools import wraps
from dataclasses import dataclass
import pandas as pd


@dataclass
class CrawledInfo:
    req_stock_cd: str
    res_stock_cd: str
    res_price: str


def find_target_child_gubun(soup_obj, target_quarter="2023q3"):
    def _convert_quarter_to_month(YYYYqN):
        splitted = YYYYqN.split("q")
        year = splitted[0]
        month = str(int(splitted[1]) * 3).zfill(2)
        return f"{year}/{month}"

    to_find_quarter = _convert_quarter_to_month(target_quarter)
    for index, th in enumerate(
        soup_obj.select_one(f"#divSonikQ > table > thead > tr").find_all("th"), start=1
    ):
        if th.text.strip() == to_find_quarter:
            return f"child({index})"


def parse(req_text, stock_cd, selector=None):
    #req_text, stock_cd = args_list
    soup_obj_local = BeautifulSoup(req_text, "lxml")
    child_gubun = find_target_child_gubun(soup_obj_local)
    if selector is None:s
        selector = (
            f"#divDaechaQ > table > tbody > tr:nth-child(48) > td:nth-{child_gubun}"
        )
    target_value = None
    elem = soup_obj_local.select_one(selector).text
    if elem is not None:
        target_value = elem.strip()
    given_stock_cd = soup_obj_local.select_one(
        "#compBody > div.section.ul_corpinfo > div.corp_group1 > h2:nth-child(2)"
    ).text
    sleep(1.5)
    return CrawledInfo(
        req_stock_cd=stock_cd, res_stock_cd=given_stock_cd, res_price=target_value
    )


async def async_parse(req_text):
    selector = "#divDaechaQ > table > tbody > tr:nth-child(48) > td:nth-child(5)"
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
        data = await async_parse(
            html,
            selector="#divDaechaQ > table > tbody > tr:nth-child(48) > td:nth-child(5)",
        )
        print(data)

    asyncio.run(execute_by_a_stock())


def process_by_batch(test_stocks_list):
    reqs = nb_client.requests(
        [
            RestClientRequest(
                method="GET", path=nb_client.get_stock_request_url(a_stock)
            )
            for a_stock in test_stocks_list
        ]
    )
    with ProcessPoolExecutor(max_workers=3) as executor:
        parsed_results = list(executor.map(parse, [a.text for a in reqs]))
    return parsed_results


async def crawl_multi_as_async(test_stocks_list, nb_client):
    requests = nb_client.arequests(
        [
            RestClientRequest(
                method="GET", path=nb_client.get_stock_request_url(a_stock)
            )
            for a_stock in test_stocks_list
        ]
    )
    return [a.text for a in await requests]


async def process_by_multi_at_async(test_stocks_list):
    nb_client = NonBlockingRestClient()
    try:
        async_results = await crawl_multi_as_async(test_stocks_list, nb_client)
    finally:
        if nb_client._session is not None:
            await nb_client._session.close()
    args_list = zip(async_results, test_stocks_list)
    with ProcessPoolExecutor(max_workers=3) as executor:
        parsed_results = list(executor.map(parse, args_list))
    return parsed_results


def _multiple_stock_request(nb_client, stocks, chunk_size=5):
    result = []
    for idx in range(0, len(stocks), chunk_size):
        chunked_stocks = stocks[idx: (idx + chunk_size)]
        partial_results = nb_client.requests(
            [RestClientRequest(method="GET", path=nb_client.get_stock_request_url(a_stock))
             for a_stock in chunked_stocks]
        )
        result.extend(partial_results)
        print(f"sleep after {idx + chunk_size} has done")
        sleep(1)

    return result


def craw_multi_and_process_at_one(args):
    chunked_stocks, nb_client = args
    async_results =_multiple_stock_request(nb_client, chunked_stocks)
    result = [parse(e.text, given_stock) for e, given_stock in zip(async_results, chunked_stocks)]
    return result





def calculate_elapsed_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        result = func(*args, **kwargs)
        end_time = datetime.now()
        elapsed_time = end_time - start_time
        print(f"Elapsed time for {func.__name__}: {elapsed_time} seconds")
        return result

    return wrapper

@calculate_elapsed_time
def craw_parse_pair_at_multiprocess(test_stocks, nb_client, processors_cnt=4):
    result = defaultdict(list)
    for idx, stock_cd in enumerate(test_stocks):
        gr_name = idx % processors_cnt
        result[gr_name].append(stock_cd)
    #args_list = zip(list(result.values()), [nb_client] * processors_cnt)
    args_list2 = [(e, nb_client) for e in list(result.values())]
    with ProcessPoolExecutor(max_workers=processors_cnt) as executor:
        parsed_results = list(executor.map(craw_multi_and_process_at_one, args_list2))
    return parsed_results


@calculate_elapsed_time
def wrap_calc(target_stocks, async_func):
    return asyncio.run(async_func(target_stocks))


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

    # target_stocks = list(
    #     pd.read_csv("./auto_trade_hantoo_trade_log.csv", header=None)[0]
    # )

    # process_by_one("005930")
    # results =process_by_multi(target_stocks) # 이러면 return되는 객체가 coroutine object process_by_multi at 0x103ea9340>

    #results_async = wrap_calc(target_stocks, process_by_multi_at_async)
    results = craw_parse_pair_at_multiprocess(target_stocks, nb_client)
    tot_cnt = len(target_stocks)
    print(results)
    res_null_cnt = len([e for e in results if e is None])
    print(f"result null cnt {res_null_cnt} / {tot_cnt}")

    # 1) 종목크롤링 따로, parsing 따로
    # 2) 종목크롤링도 async로 -> parsing도 : 이걸 하나의 async함수로.. 의미가 있나모르겟다..
    #   -> 2처럼하면 미처 다 받아오기도 전에, 넘어가서 그래서 None인가..?
    # 3)
