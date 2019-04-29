import asyncio
import websockets
import matplotlib.pyplot as plt
import numpy as np

host = 'ws://localhost:8765'

async def get_image():
    async with websockets.connect(host) as websocket:
        height, width = 500, 500
        request = str(height) + 'x' + str(width)
        await websocket.send(request)
        print('>', request)
        payload = await websocket.recv()
        print('<', len(payload))
        img = np.frombuffer(payload, dtype=np.uint8).reshape(height, width, 3)
        print(img.shape)

    plt.imshow(img)
    plt.show()


asyncio.get_event_loop().run_until_complete(get_image())
asyncio.get_event_loop().run_forever()