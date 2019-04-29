import pygame, sys
import time
from PIL import ImageGrab
import numpy as np
import websockets
import asyncio
import cv2
pygame.init()

class Cropper():

    def __init__(self):
        self._screenshot = None
        self._left, self.right, self._lower, self._upper = None, None, None, None

    @staticmethod
    def capture_screenshot(bbox=(0, 0, 1500, 860), resize_shape=None):
        img = ImageGrab.grab(bbox)  # bbox specifies specific region (bbox= x,y,width,height)
        screenshot = np.array(img)
        if resize_shape:
            screenshot = cv2.resize(screenshot, resize_shape)
        print(screenshot.shape)
        return screenshot

    @staticmethod
    def get_resized_img(image, square_size):
        height, width = image.shape[:-1]
        if (height > width):
            differ = height
        else:
            differ = width
        differ += 4

        mask = np.zeros((differ, differ, 3), dtype="uint8")
        x_pos = int((differ - width) / 2)
        y_pos = int((differ - height) / 2)
        mask[y_pos:y_pos + height, x_pos:x_pos + width, :] = image[0:height, 0:width, :]
        mask = cv2.resize(mask, (square_size, square_size), interpolation=cv2.INTER_AREA)

        return mask

    def get_screenshot(self, bbox=(0, 0, 1500, 860)):
        self._screenshot = Cropper.capture_screenshot(bbox)

    def displayImage(self, screen, px, topleft, prior):
        # ensure that the rect always has positive width, height
        x, y = topleft
        width = pygame.mouse.get_pos()[0] - topleft[0]
        height = pygame.mouse.get_pos()[1] - topleft[1]
        if width < 0:
            x += width
            width = abs(width)
        if height < 0:
            y += height
            height = abs(height)

        # eliminate redundant drawing cycles (when mouse isn't moving)
        current = x, y, width, height
        if not (width and height):
            return current
        if current == prior:
            return current

        # draw transparent box and blit it onto canvas
        screen.blit(px, px.get_rect())
        im = pygame.Surface((width, height))
        im.fill((128, 128, 128))
        pygame.draw.rect(im, (32, 32, 32), im.get_rect(), 1)
        im.set_alpha(128)
        screen.blit(im, (x, y))
        pygame.display.flip()

        # return current box extents
        return (x, y, width, height)

    def setup(self):
        self.get_screenshot(bbox=(0, 0, 1500, 860))
        px = pygame.image.frombuffer(self._screenshot.tostring(), self._screenshot.shape[1::-1], "RGB")
        screen = pygame.display.set_mode( px.get_rect()[2:] )
        screen.blit(px, px.get_rect())
        pygame.display.flip()
        return screen, px

    def mainLoop(self, screen, px):
        topleft = bottomright = prior = None
        n=0
        while n!=1:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    if not topleft:
                        topleft = event.pos
                    else:
                        bottomright = event.pos
                        n=1
            if topleft:
                prior = self.displayImage(screen, px, topleft, prior)
        return ( topleft + bottomright )

    def get_cropped_screenshot(self, upper, lower, left, right):
        cropped_screenshot = self._screenshot[upper:lower, left:right]
        return cropped_screenshot

    def start(self):
        screen, px = self.setup()
        left, upper, right, lower = self.mainLoop(screen, px)

        # ensure output rect always has positive width, height
        if right < left:
            left, right = right, left
        if lower < upper:
            lower, upper = upper, lower

        self._upper, self._lower, self._left, self._right = upper, lower, left, right
        print("Bounding Box = ", (upper, lower, left, right))

        cropped_screenshot = self.get_cropped_screenshot(upper, lower, left, right)
        #plt.imshow(cropped_screenshot)
        #plt.show()

    def get_bounding_box(self):
        return self._upper, self._lower, self._left, self._right


class Server():

    def __init__(self, bbox):
        self._bbox = bbox

    async def capture(self, websocket, path):
        request = await websocket.recv()
        print("<", request)

        if request == 'img_shape':
            width, height = self._bbox[3] - self._bbox[2], self._bbox[1] - self._bbox[0]
            payload = bytes(str(width) + 'x' + str(height), 'UTF-8')
        else:
            upper, lower, left, right = self._bbox
            x, y, width, height = left, upper, right - left, lower - upper
            resize_height, resize_width = [int(i) for i in request.split('x')]
            print("Bbox = ", self._bbox)
            print("Resize = ", resize_height, resize_width)
            img = Cropper.capture_screenshot(bbox=(x, y, width, height), resize_shape=None)
            img = Cropper.get_resized_img(img, resize_height)
            print(img.shape, img.dtype)
            payload = img.tobytes()

        await websocket.send(payload)
        print('>', payload)

    def start(self):
        start_server = websockets.serve(self.capture, 'localhost', 8765)

        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    time.sleep(3)
    cropper = Cropper()
    cropper.start()
    print(cropper.get_bounding_box())

    print("Starting server")
    Server(cropper.get_bounding_box()).start()
