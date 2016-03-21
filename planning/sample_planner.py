from world import WorldApi
import time


class Planner:

    def __init__(self):
        api = WorldApi()

        try:
            
            while True:
                print "My position: ", api.getMyPosition()
                print "Friend position: ", api.getAllyPosition()
                print "Enemy positions: ", api.getEnemyPositions()
                print api.getMyOrientation()
                print api.getAllyOrientation()
                print api.getEnemyOrientation()
            
        finally:
        # This needs to be run on both a clean or unclean exit. otherwise your threads won't close gracefully
            api.close()


Planner()
