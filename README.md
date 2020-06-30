# Find The Doggy

This project was created after a doggy kept pooping in our yard. This is an attempt to find the doggy so that maybe its owner will clean up after it at least.

To get this running, you need to run three different processes: Front End, Server, and Daemon. Instructions for each can be found below.

## Start Front End Server
To develop the front end (currently there is no production setup):

```
cd frontend
npm install
npm start
```

You have to have an https connection (or use localhost) in order to get the UI to run (because we are using `getUserMedia`). Because I need this to work on my phone, I decided to just run this locally but have ngrok serve my local port.

Use ngrok to get https access pointing to your front end server:

```
ngrok http 3000
```

* Note that we have a proxy for the backend on port 5000

## Start Back End Server
This is ran using flask, you can just run `./bin/develop-flask.sh`.

This starts a server that you can hit on the endpoint (using POST) `http://localhost:5000/newImage` to send each image (which the front end server will do).

The backend server simply saves each image frame.

## Start Daemon
There is a daemon that should continuously run to look for new images. These daemon pulls new images (from the `temp-images` folder) and then runs the prediction algorithm against each new image to see if there is a dog in the image. Note that each image, once pulled, will be deleted from `temp-images` folder.

The daemon can be started by running `./bin/run-daemon.py`.

## The Machine Learning Model and architecture

We are using the VGG16 machine learning model. Everything is housed inside the [_scan_for_dogs.py](python/_scan_for_dogs.py) file. You can test this single files functionality by running this file by itself (ie `python ./python/_scan_for_dogs.py`).

The `scan_for_dogs` function actually does all of the hard work and will save any possible dog images based on the probability that a dog is in fact in the image:

- 10% confidence will go into the `data/dog-images-maybe/` folder
- 25% confidence will go into the `data/dog-images-probably/` folder
- 50% confidence will go into the `data/dog-images-definitely/` folder

### Notes

To use specific pretrained networks: https://keras.io/api/applications/

I had to crop the images (to be square) and resize the images (to be 224/224) to work with ResNet50

You may get errors using visual studio code. If so, it might be helpful to follow these steps (found [here](https://stackoverflow.com/questions/52705643/abort-trap-6-when-attempting-opencv-video-capture-on-macos-mojave)):


```
1. type cmd+shift+p
2. type "shell command: Install code in PATH"
3. Close vscode
4. Use "sudo code" to open vscode
5. It will give warning not to run as a root user
6. Ignore the warning and run the file , you will not get the "Abort trap: 6" error anymore.
```
