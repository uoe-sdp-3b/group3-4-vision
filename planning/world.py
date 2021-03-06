#!/usr/bin/env python2.7
import zmq
from threading import Thread
import logging

log = logging.getLogger(__name__)


class WorldApi():
    """
    Wrapper around world with some threading magic to make things interesting
    """

    def __init__(self, target="tcp://localhost:5555", debug=False):
        if debug:
            log.setLevel(logging.DEBUG)
        self.world = None
        self.target = target
        self.thread_close = False
        self.thread_ready = False
        self.client_thread = Thread(target=self.client)
        self.client_thread.start()

    def close(self):
        """
        Cleans up WorldApi
        """
        log.debug("Closing Thread")
        self.thread_close = True

    def client(self):
        log.info("Client Thread ready")
        ctx = zmq.Context()
        socket = ctx.socket(zmq.SUB)
        socket.setsockopt(zmq.SUBSCRIBE, '')
        socket.setsockopt(zmq.RCVTIMEO, 100)
        socket.connect(self.target)

        while not self.thread_close:
            obj = None
            try:
                obj = socket.recv_pyobj()
            except zmq.Again:
                log.warn("Thread not receiving anything")

            if obj is not None:
                self.thread_ready = True
                self.world = obj

        socket.close()
        log.debug("Thread Closed")

    def ready(self):
        """
        whether the world api is ready yet
        """
        return self.thread_ready
