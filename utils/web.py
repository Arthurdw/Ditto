# Copyright Arthurdw 2021-present
# Full MIT License can be found in `LICENSE` at the project root.

from asyncio import ensure_future, get_event_loop
from json import loads, JSONDecodeError
from os import getenv
from threading import Thread
from typing import Dict
from uuid import UUID

from aiohttp.web import Application, Response, post, AppRunner, TCPSite, Request
from pincer.utils.types import Coro


class Webserver:
    callbacks: Dict[str, Coro] = {}

    def __init__(self):
        Thread(target=self.__run).run()

        self.base_url = getenv("BASE_URL")

    @staticmethod
    async def handle(request: Request) -> Response:
        try:
            await Webserver.callbacks["webhook"](UUID(request.match_info["id"]), loads(await request.content.read()))
        except JSONDecodeError:
            return Response(status=400, body="No valid JSON body has been passed!")
        except ValueError:
            return Response(status=400, body="Invalid webhook id supplied!")
        except IndexError:
            return Response(status=404, body="Webhook not found!")
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
