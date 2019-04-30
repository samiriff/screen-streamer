import asyncio
import websockets
import matplotlib.pyplot as plt
import numpy as np
import time
import argparse

# Default values
host = 'ws://localhost:8765'  # Modify this with a public URL if running remotely
run_once = True               # Change to False to keep capturing images periodically
time_period = 2               # Indicates the number of seconds between consecutive captures. Modify for your use case.

async def get_image():
    while True:
        async with websockets.connect(host) as websocket:
            height, width = 500, 500
            request = str(height) + 'x' + str(width)
            await websocket.send(request)
            print('>', request)
            payload = await websocket.recv()
            print('<', len(payload))
            img = np.frombuffer(payload, dtype=np.uint8).reshape(height, width, 3)
            performOperation(img)

        if run_once:
            print("Run Once = ", run_once)
            break

        time.sleep(time_period)

def performOperation(img):
    # TODO: Add your custom logic here for processing each image
    # Eg., model.predict

    print("Image shape = ", img.shape)
    plt.imshow(img)
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sample Screen Streaming Client')
    parser.add_argument(
        '--host', action='store', dest='host', default=host,
        help='Host to connect to via Websocket protocol'
    )
    parser.add_argument(
        '--run-once', action='store', dest='run_once', default=run_once,
        help='Request for screenshot only once and then exit'
    )
    parser.add_argument(
        '--time-period', action='store', dest='time_period', default=time_period,
        help='Host to connect to via Websocket protocol'
    )
    results = parser.parse_args()

    host = results.host
    run_once = results.run_once
    time_period = results.time_period

    asyncio.get_event_loop().run_until_complete(get_image())