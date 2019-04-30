
# Screen Streamer

Capture a portion of your screen at periodic intervals and stream each frame as Numpy arrays (via Websockets) which can be consumed by remote environments. One sample use case would be to stream frames of a video playing on your laptop screen to a remote environment such as  Google Colaboratory, where you can train a neural network using Tensorflow with a GPU. 

```
  _________                                      _________ __                                              
 /   _____/ ___________   ____   ____   ____    /   _____//  |________   ____ _____    _____   ___________ 
 \_____  \_/ ___\_  __ \_/ __ \_/ __ \ /    \   \_____  \\   __\_  __ \_/ __ \\__  \  /     \_/ __ \_  __ \
 /        \  \___|  | \/\  ___/\  ___/|   |  \  /        \|  |  |  | \/\  ___/ / __ \|  Y Y  \  ___/|  | \/
/_______  /\___  >__|    \___  >\___  >___|  / /_______  /|__|  |__|    \___  >____  /__|_|  /\___  >__|   
        \/     \/            \/     \/     \/          \/                   \/     \/      \/     \/
```

[//]: # (Image References)

[image1]: ./images/pygame_window.png "Pygame Window"
[image2]: ./images/pygame_window_selection.png "Pygame Window Selection"
[image3]: ./images/ngrok.png "ngrok"

## Basic Usage

### Start Screen Streaming Server
- Run `python screen_streaming_server.py`
- You will have 2 seconds to ensure that the windows on your screen are what you would like to capture.
- A new pygame window pops up in which a screenshot of your screen is displayed.
	![Pygame Window][image1]
- You will now have to draw a bounding box around your area of interest. To begin, click on a point in this screenshot to indicate the top-left corner of your bounding box. You will now see a gray overlay on the image.
- Move your mouse cursor to adjust the width and height of the rectangle, and once you are satisfied, click once again to indicate the bottom-right point of your bounding box.
	![Pygame Window Selection][image2]
- Minimize the pygame window.
- You should now see a "Starting Server" message along with bounding box coordinates in your console.

### Expose Public URL
- The server will be accessible at `localhost:8765` via a websocket, so, in order to access this websocket remotely, you will have to expose a public URL using ngrok.
- Visit [https://ngrok.com/](https://ngrok.com/) to download and install ngrok
- After installation, run `ngrok http 8765` from a new command prompt and note the first part of the forward URL in the screen that shows up.
	![ngrok][image3]

### Run Screen Streaming Client remotely
- In your remote system, run `python screen_streaming_client.py --host ws://ee90dd44.ngrok.io --run_once=False --time-period=2`
- An image plot containing a screenshot from your designated bounding box should appear, and the dimensions of the image should be printed in the logs.
- Closing the window should reopen a new image plot after a time period of 2 seconds, as specified in your command above.
- To run this client only once, just change the `run_once` flag to True while starting the client.
- Add your custom business logic to the `performOperation` method in `screen_streaming_client.py`

### Run Screen Streaming Client in Google Colaboratory
- Open [https://colab.research.google.com](https://colab.research.google.com/)
- Navigate to `File > Open Notebook` and select the GITHUB tab
- Enter the following URL - [https://github.com/samiriff/screen-streamer/blob/master/google_colab_sample.ipynb](https://github.com/samiriff/screen-streamer/blob/master/google_colab_sample.ipynb) in the text field to open and run this notebook.
- Follow the instructions in the notebook to perform custom operations on the image retrieved from your local web socket.

## Contributors
- Samir Sheriff
