#!/bin/bash

# Set the image name
IMAGE_NAME="waterpolo_calendar_backend"

# Build the image
docker build -t $IMAGE_NAME .
