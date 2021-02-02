from time import perf_counter as pf
import asyncio
import struct

host = '0.0.0.0'
port = 19133
cons = 20

response_times = []

handshake_payload = b'\x10\x00\x04\nxenonmc.mlJ\xbd\x01'
request_payload = b'\x01\x00'
pingpong_payload = b"\t\x01.K\xdb\xf7\xc9\x84';"

async def ping():
    r, w = await asyncio.open_connection(host, port)

    print('after con')

    w.write(handshake_payload)
    await w.drain()

    await asyncio.sleep(.1); print('handshake')

    w.write(request_payload)
    await w.drain()

    await asyncio.sleep(.1); print('request')

    w.write(pingpong_payload)
    await w.drain()

    await asyncio.sleep(.1); print('pingpong +  wait')

    start = pf()
    await r.read(8)
    return pf() - start

async def main():
    print(await ping())

asyncio.run(main())
