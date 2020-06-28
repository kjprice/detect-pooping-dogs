To start, simply run `./python/scan_for_dogs.py`

To do this in Visual studio, follow these steps (found [here](https://stackoverflow.com/questions/52705643/abort-trap-6-when-attempting-opencv-video-capture-on-macos-mojave)):
1. type cmd+shift+p
2. type "shell command: Install code in PATH"
3. Close vscode
4. Use "sudo code" to open vscode
5. It will give warning not to run as a root user
6. Ignore the warning and run the file , you will not get the "Abort trap: 6" error anymore.

### Notes

To use specific pretrained networks: https://keras.io/api/applications/

I had to crop the images (to be square) and resize the images (to be 224/224) to work with ResNet50

## Create SSL Certificate

I followed the instructions [here](https://www.freecodecamp.org/news/how-to-get-https-working-on-your-local-development-environment-in-5-minutes-7af615770eec/). I used the password "test".

## Start Front End Server

To develop the front end (currently there is no production setup):

```
cd frontend
npm start
```

Use ngrok to get https access (note that we have a proxy for the backend on port 5000)

```
ngrok http 3000
```

## Start Back End Server

This is ran using flask, you can just run `./bin/develop-flask.sh`

# TODO
 - On Front end make it so that there are only 3 web requests at any given time - throttle requests when there are too many requests
 - Setup a UI to see the images (and their predictions)
 - Split python scripts into multiple cores - one script is the flask server and saves the raw images - the other scripts pull from the raw image folder and makes predictions
