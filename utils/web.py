# Copyright Arthurdw 2021-present
# Full MIT License can be found in `LICENSE` at the project root.

from asyncio import ensure_future, get_event_loop
from json import loads
from threading import Thread
from typing import Dict

from aiohttp.web import Application, Response, post, AppRunner, TCPSite, Request
from pincer.utils.types import Coro


class Webserver:
    callbacks: Dict[str, Coro] = {}

    def __init__(self):
        Thread(target=self.__run).run()

    @staticmethod
    async def handle(request: Request) -> Response:
        try:
            await Webserver.callbacks["webhook"](request.match_info["id"], loads(await request.content.read()))
        except Exception as e:
            # TODO: proper response
            raise e
        return Response(body="Ok")

    @staticmethod
    def __get_runner():
        app = Application()
        app.add_routes([post("/webhook/{id}", Webserver.handle)])
        return AppRunner(app)

    def __run(self):
        runner = self.__get_runner()

        loop = get_event_loop()
        loop.run_until_complete(runner.setup())

        site = TCPSite(runner, 'localhost', 80)
        ensure_future(site.start())
