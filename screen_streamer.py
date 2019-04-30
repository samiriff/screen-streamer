from PIL import ImageGrab
import numpy as np
import cv2
import asyncio
import websockets
import base64
from pygame_cropper import Cropper

def get_screenshot():
    img = ImageGrab.grab(bbox=(100,10,400,780)) #bbox specifies specific region (bbox= x,y,width,height)
    img_np = np.array(img)
    frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
    #cv2.imshow("test", frame)
    print(frame.shape)
    #cv2.waitKey(2000)
    #cv2.destroyAllWindows()
    return frame

async def hello(websocket, path):
    name = await websocket.recv()
    print("<", name)

    #img = cv2.imread('../data/notMNIST_small/A/MDEtMDEtMDAudHRm.png')
    img = get_screenshot()
    print(img.shape)
    payload = base64.b64encode(img.tobytes())

    await websocket.send(img.tobytes())
    print('>', payload)

start_server = websockets.serve(hello, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
