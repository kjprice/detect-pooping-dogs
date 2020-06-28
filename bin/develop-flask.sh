#!/bin/sh
# nodemon -e py -x 'python python/server.py'

source ~/.bash_profile

ca

cd python
nodemon -e py,sh -x 'sh flask_server.sh'