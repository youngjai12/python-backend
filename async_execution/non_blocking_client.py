from asyncio import AbstractEventLoop
from http import HTTPStatus
from typing import List, Any
import asyncio
from aiohttp import ClientSession, TCPConnector, ClientTimeout, ClientResponse
from attr import define
from requests.adapters import HTTPAdapter, Retry

@define(kw_only=True)
class RestClientRequest:
    method: str
    path: str
    headers = None
    params = None
    form_data = None
    json_data = None


@define(kw_only=True)
class RestClientResponse:
    status_code: int = None
    reason: str = None
    data: Any = None
    text: str = None


class NonBlockingRestClient:
    def __init__(
        self, pool_size: int = 10, connect_timeout: int = 5, read_timeout: int = 20
    ) -> None:
        self.pool_size = pool_size
        self.connect_timeout = connect_timeout
        self.read_timeout = read_timeout
        self._session: ClientSession = None
        self._loop: AbstractEventLoop = None
        self.url = "https://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp?pGB=1&gicode=A{}&cID=&MenuYn=Y&ReportGB=&NewMenuID=103&stkGb=701"

    def get_stock_request_url(self, stock):
        return self.url.format(stock)

    async def get_session(self) -> ClientSession:
        should_renew_session = self._session is None

        if self._loop != (cur_loop := asyncio.get_running_loop()):
            self._loop = cur_loop
            should_renew_session = True

        if should_renew_session:
            if self._session is not None:
                await self._session.close()

            self._session = ClientSession(
                connector=TCPConnector(limit=self.pool_size),
                timeout=ClientTimeout(
                    sock_connect=self.connect_timeout,  # Maximal number of seconds for connecting to a peer for a new connection
                    sock_read=self.read_timeout,  # Maximal number of seconds for reading a portion of data from a peer.
                ),
            )

        assert self._session is not None

        return self._session

    def requests(self, requests: List[RestClientRequest]) -> List[RestClientResponse]:
        async def call_arequests_and_close_session() -> List[RestClientResponse]:
            """
            asyncio.run()을 호출하면 loop가 종료되기 때문에 명시적으로 session과 loop를 초기화 해준다.
            """
            try:
                return await self.arequests(requests)
            finally:
                assert self._session is not None

                await self._session.close()
                self._session = None
                self._loop = None

        return asyncio.run(call_arequests_and_close_session())

    async def arequests(
        self, requests: List[RestClientRequest]
    ) -> List[RestClientResponse]:
        tasks = []
        for req in requests:
            tasks.append(asyncio.create_task(self.arequest(req)))
        ttmp = await asyncio.gather(*tasks)

        return [
            RestClientResponse(
                status_code=resp.status, reason=resp.reason, text=html_text
            )
            for resp, html_text in ttmp
        ]

    async def arequest(self, request: RestClientRequest):
        async with (await self.get_session()).request(
            method=request.method,
            url=request.path,
            params=request.params,
            data=request.form_data,
            json=request.json_data,
            headers=request.headers,
        ) as r:
            return r, await r.text()

    def set_connection_properties(self) -> None:
        server_error_codes = [
            HTTPStatus.INTERNAL_SERVER_ERROR,
            HTTPStatus.NOT_IMPLEMENTED,
            HTTPStatus.BAD_GATEWAY,
            HTTPStatus.SERVICE_UNAVAILABLE,
            HTTPStatus.GATEWAY_TIMEOUT,
        ]
        retry = Retry(total=5, status_forcelist=server_error_codes)
        self._session.mount("http://", HTTPAdapter(max_retries=retry))



if __name__ == "__main__":
    nb_client = NonBlockingRestClient()
    chunked_stocks = ['064090', '068760', '079190', '093240']
    partial_results = nb_client.requests(
        [RestClientRequest(method="GET", path=nb_client.get_stock_request_url(a_stock))
         for a_stock in chunked_stocks]
    )
