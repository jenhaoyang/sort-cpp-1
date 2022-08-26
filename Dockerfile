FROM nvcr.io/nvidia/cuda:11.4.3-cudnn8-devel-ubuntu20.04

RUN apt-get update -y && \
    apt-get install -y \
    unzip \
    gpg \
    wget \
    g++

# install cmake https://apt.kitware.com/
RUN wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | gpg --dearmor - | tee /usr/share/keyrings/kitware-archive-keyring.gpg >/dev/null
RUN echo 'deb [signed-by=/usr/share/keyrings/kitware-archive-keyring.gpg] https://apt.kitware.com/ubuntu/ focal main' | tee /etc/apt/sources.list.d/kitware.list >/dev/null
RUN apt-get update
RUN rm /usr/share/keyrings/kitware-archive-keyring.gpg
RUN apt-get install -y kitware-archive-keyring cmake

# Download and unpack sources
RUN wget -O opencv.zip https://github.com/opencv/opencv/archive/4.x.zip
RUN wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.x.zip
RUN unzip opencv.zip
RUN unzip opencv_contrib.zip
ARG DEBIAN_FRONTEND=noninteractive
RUN apt install -y ffmpeg
# Create build directory and switch into it
RUN mkdir -p build && cd build
# Configure
RUN cmake -DOPENCV_EXTRA_MODULES_PATH=../opencv_contrib-4.x/modules ../opencv-4.x
# Build
RUN cmake --build . -j 8

RUN apt-get install -y \
    libboost-all-dev
RUN apt-get install -y \
    libeigen3-dev 
WORKDIR /workspace

