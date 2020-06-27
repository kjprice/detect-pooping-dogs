#!/bin/sh

source ~/.bash_profile

ca

nodemon -e py -x 'python python/pull_from_webcam.py'
