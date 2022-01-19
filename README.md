wsaio is a callback-based WebSocket library for Python.

# Examples
```py
import asyncio

from wsaio import WebSocketClient


class EchoClient(WebSocketClient):
    async def on_text(self, data):
        await self.write(data)

    async def on_binary(self, data):
        await self.write(data, binary=True)


async def main(loop):
    client = EchoClient(loop=loop)

    await client.connect('wss://localhost/helloWorld')


loop = asyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()
```
