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
                print "My angle: ", api.getMyOrientation()[1]
                print "Mate angle: ", api.getAllyOrientation()[1]
                #rint "Enemy "api.getEnemyOrientation()
                print "Angles_0-> ", api.getEnemyOrientation()[0][1]
                print "Angles_1-> ", api.getEnemyOrientation()[1][1]

            
        finally:
        # This needs to be run on both a clean or unclean exit. otherwise your threads won't close gracefully
            api.close()


Planner()
