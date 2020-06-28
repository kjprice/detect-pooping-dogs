#!/bin/sh

source ~/.bash_profile

ca

nodemon -e py -x 'time python python/_scan_for_dogs.py'
