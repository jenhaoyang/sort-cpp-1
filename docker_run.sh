DOCKER_NAME=sort

# XSOCK=/tmp/.X11-unix
# XAUTH=/home/$USER/.Xauthority

# xhost +

docker run \
    -it --rm \
    -e XAUTHORITY=${XAUTH} \
    -e DISPLAY=${DISPLAY} \
    -e QT_X11_NO_MITSHM=1 \
    --privileged \
    -v /dev/bus/usb:/dev/bus/usb \
    -v /dev/video0:/dev/video0 \
    -v $PWD:/workspace \
    --name sort-cpp \
    $DOCKER_NAME /bin/bash
