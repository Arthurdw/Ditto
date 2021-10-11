from pincer import command


class Test:
    @command(guild=728278830770290759)
    async def test(self):
        return "Working"


setup = Test
