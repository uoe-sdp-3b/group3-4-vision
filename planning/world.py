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
                log.debug(obj)
                self.world = World(obj)

        socket.close()
        log.debug("Thread Closed")

    def ready(self):
        """
        whether the world api is ready yet
        """
        return self.thread_ready

    def get_allied_green(self):
        return self.world.allied_green

    def get_allied_pink(self):
        return self.world.allied_pink

    def get_opponent_green(self):
        return self.world.green_opponent

    def get_opponent_pink(self):
        return self.world.pink_opponent


class World():
    """
    Simple wrapper object to ease handling
    """
    def __init__(self, d):
        try:
            self.allied_green = d['ally']['green']
            self.allied_pink = d['ally']['pink']
            self.pink_opponent = d['enemy']['pink']
            self.green_opponent = d['enemy']['green']
        except KeyError as e:
            log.error("Error accessing key " + e.message)
