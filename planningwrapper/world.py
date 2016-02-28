#!/usr/bin/env python2.7
import zmq
from threading import Thread


class WorldApi():
    """
    Wrapper around world with some threading magic to make things interesting
    """

    def __init__(self, target="tcp://localhost:5555"):
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
        self.thread_close = True

    def client(self):
        print("Thread ready")
        ctx = zmq.Context()
        socket = ctx.socket(zmq.SUB)
        socket.setsockopt(zmq.SUBSCRIBE, '')
        socket.connect(self.target)

        while not self.thread_close:
            obj = socket.recv_pyobj()
            if obj is not None:
                self.thread_ready = True
                self.world = World(obj)

        socket.close()

    # TODO: look into making this more generic
    # ugly blocking hax
    def get_allied_green(self):
        while not self.thread_ready:
            pass
        return self.world.allied_green

    def get_allied_pink(self):
        while not self.thread_ready:
            pass
        return self.world.allied_pink

    def get_opponent_green(self):
        while not self.thread_ready:
            pass
        return self.world.green_opponent

    def get_opponent_pink(self):
        while not self.thread_ready:
            pass
        return self.world.pink_opponent

    def get_ball(self):
        while not self.thread_ready:
            pass
        return self.world.ball

    def get_time(self):
        while not self.thread_ready:
            pass
        return self.world.time


class World():
    """
    Simple wrapper object to ease handling
    """
    def __init__(self, d):
        try:
            self.time = d["time"]
            self.ball = d["ball_center"]
            self.allied_green = d["green_ally"]
            self.allied_pink = d["pink_ally"]
            self.pink_opponent = d["pink_opponent"]
            self.green_opponent = d["green_opponent"]
        except KeyError as e:
            print("Error accessing key " + e.message)
