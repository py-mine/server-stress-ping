from time import time
import asyncio
import struct

host, port = input('Host: ').split(':')
port = int(port)

cons = 100

response_times = []

handshake_payload = b'\x10\x00\x04\nxenonmc.mlJ\xbd\x01'
request_payload = b'\x01\x00'
pingpong_payload = b"\t\x01.K\xdb\xf7\xc9\x84';"

async def ping():
    try:
        r, w = await asyncio.open_connection(host, port)

        w.write(handshake_payload)
        await w.drain()

        await asyncio.sleep(.1)

        w.write(request_payload)
        await w.drain()

        await asyncio.sleep(.1)

        start = time()
        w.write(pingpong_payload)
        await w.drain()

        await r.read(8)

        return time() - start
    except ConnectionResetError:
        return -1

async def main():
    tasks = []

    for _ in range(cons):
        tasks.append(asyncio.create_task(ping()))

    await asyncio.wait(tasks)

    times = [t for t in [t.result() for t in tasks] if t != -1]

    avg = round((sum(times) / len(times)) * 1000, 2)
    max_ = round(max(times) * 1000, 2)

    print(f'Average: {avg}ms | Max: {max_}ms | Dropped: {len(tasks)-len(times)}')

asyncio.run(main())
