from asyncio import ensure_future, get_event_loop
from threading import Thread

from aiohttp.web import Application, Response, get, AppRunner, TCPSite


class Webserver:
    def __init__(self):
        Thread(target=self.__run).run()

    @staticmethod
    async def handle(request):
        hook_id = request.match_info.get('hook', None)
        print(hook_id)
        return Response()

    @staticmethod
    def __get_runner():
        app = Application()
        app.add_routes([get("/{hook}", Webserver.handle)])
        return AppRunner(app)

    def __run(self):
        runner = self.__get_runner()

        loop = get_event_loop()
        loop.run_until_complete(runner.setup())

        site = TCPSite(runner, 'localhost', 80)
        ensure_future(site.start())
