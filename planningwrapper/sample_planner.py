from world import WorldApi
import time


class Planner:

    def __init__(self):
        api = WorldApi()

        try:
            print api.get_allied_green()
            print api.get_allied_pink()
            print api.get_opponent_green()
            print api.get_opponent_pink()
            print api.get_ball()
            print api.get_time()
            while True:
                print(api.get_time())
        finally:
            # This needs to be run on both a clean or unclean exit. otherwise your threads won't close gracefully
            api.close()


Planner()
