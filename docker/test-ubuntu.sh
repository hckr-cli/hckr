#!/bin/bash
IMAGE='hckr-ubuntu'


docker build -t $IMAGE .

docker run -it $IMAGE


# we can run 'make checks' inside this ubuntu image to test everything
