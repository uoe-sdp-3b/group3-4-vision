#!/usr/bin/env python2.7
import time
import zmq
import numpy as np


# 1. setup a publisher in zmq
# 2. start pushing computed frames down the wire



def main():
    ctx = zmq.Context()
    socket = ctx.socket(zmq.SUB)
    socket.setsockopt(zmq.SUBSCRIBE, '')
    socket.connect("tcp://localhost:5555")

    print("beginning receiving...")
    while True:
        obj = socket.recv_pyobj()
        print(obj)


if __name__ == "__main__":
    main()
