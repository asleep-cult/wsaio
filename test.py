import asyncio
import traceback

from wsaio.client import WebSocketClient


class EchoClient(WebSocketClient):
    def __init__(self, *, loop=None):
        super().__init__(loop=loop)
        self.event = asyncio.Event()

    async def on_text(self, data):
        await self.send(data)

    async def on_binary(self, data):
        await self.send(data, binary=True)

    async def on_closed(self, exc):
        self.event.set()


class CasesClient(WebSocketClient):
    def __init__(self, *, loop=None):
        super().__init__(loop=loop)
        self.event = asyncio.Event()

    def on_text(self, data: str) -> None:
        self.cases = int(data)
        self.event.set()


async def main():
    cases = CasesClient()
    await cases.connect('ws://127.0.0.1:9001/getCaseCount')
    await cases.event.wait()

    try:
        for i in range(1, cases.cases):
            try:
                print(f'Running test case {i}')
                client = EchoClient()
                await client.connect(f'ws://127.0.0.1:9001/runCase?case={i}&agent=wsaio')

                try:
                    await asyncio.wait_for(client.event.wait(), timeout=1000)
                except asyncio.TimeoutError:
                    print(f'Test case {i} timed out')
                    await client.close()
                    continue
            except Exception:
                print(f'Exception in tast case {i}')
                traceback.print_exc()
            else:
                print(f'Completed test case {i}')
    finally:
        client = WebSocketClient()
        await client.connect('ws://localhost:9001/updateReports?agent=wsaio')


asyncio.run(main())
