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

# TODO: Describe how to run the flask server, describe how to run the front end code
# TODO: Maybe use python simple server to serve static local files
# TODO: Maybe crop the images in several different places and run the prediction algorithm on these slices (to give higher res to images)

## Create SSL Certificate

I followed the instructions [here](https://www.freecodecamp.org/news/how-to-get-https-working-on-your-local-development-environment-in-5-minutes-7af615770eec/). I used the password "test".

## Start Front End Server

Install software to serve https:
```
npm install -g git+ssh://git@git.daplie.com:Daplie/serve-https
```

To make the front end code available on port 1820 on your local (and network):

```
cd frontend
npm run build
serve -s build -p 1820
```

To develop the front end:

```
cd frontend
npm start
```

