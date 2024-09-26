import httpx
import asyncio
from httpx import TimeoutException, ConnectTimeout, ReadTimeout
from .. import SuccessResponse, InfoResponse, ErrorResponse, BaseError
from .. import API_CONST
from .. import settings

async def fetch_data(url):
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(
                url=url, 
                timeout=settings.CALL_API_TIMEOUT
            )
            requset_code = res.status_code
            requset_result = res.json()
            if requset_code == 200:
                return SuccessResponse(
                    data = requset_result['data']
                )
            elif requset_code == 404:
                return InfoResponse(
                    message='USER NOT EXIST'
                )
            else:
                error = BaseError(
                    error_info=f'Request code:{res.status_code}',
                    track_id=None
                )
                return ErrorResponse(
                    message='NETWORK ERROR',
                    data=error
                )
    except (TimeoutException, ConnectTimeout, ReadTimeout):
        error = BaseError(
            error_info='Request Timeout',
            track_id=None
        )
        return ErrorResponse(
            message='NETWORK ERROR',
            data=error
        )
    except Exception as e:
        error = BaseError(
            error_info=f'Request error:{type(e).__name__}',
            track_id=None
        )
        return ErrorResponse(
            message='NETWORK ERROR',
            data=error
        )

async def get_other_data(
    aid: str,
    server: str,
    use_ac: bool = False,
    ac: str = None
) -> SuccessResponse | InfoResponse | ErrorResponse:
    urls = [
        f'{API_CONST.VORTEX_API_URL.get(server)}/api/accounts/{aid}/ships/pvp/' + (f'?ac={ac}' if use_ac else ''),
        f'{API_CONST.VORTEX_API_URL.get(server)}/api/accounts/{aid}/ships/pvp_solo/' + (f'?ac={ac}' if use_ac else ''),
        f'{API_CONST.VORTEX_API_URL.get(server)}/api/accounts/{aid}/ships/pvp_div2/' + (f'?ac={ac}' if use_ac else ''),
        f'{API_CONST.VORTEX_API_URL.get(server)}/api/accounts/{aid}/ships/pvp_div3/' + (f'?ac={ac}' if use_ac else ''),
        f'{API_CONST.VORTEX_API_URL.get(server)}/api/accounts/{aid}/ships/rank_solo/' + (f'?ac={ac}' if use_ac else '')
    ]
    tasks = []
    responses = []
    async with asyncio.Semaphore(len(urls)):
        for url in urls:
            tasks.append(fetch_data(url))
        responses = await asyncio.gather(*tasks)
        return responses