from world import WorldApi
import time


class Planner:

    def __init__(self):
        api = WorldApi()

        try:
            """
             def getMyPosition():
        return self.world[('ally', 'me')]['center']

    def getAllyPosition():
        return self.world[('ally', 'friend')]['center']

    def getEnemyPositions():
        return [self.world[('enemy', 'friend')]['center'], self.world[('enemy', 'me')]['center']]

    def getMyOrientation():
        return self.world[('ally', 'me')]['orientation']

    def getAllyOrientation():
        return self.world[('ally', 'friend')]['orientation']

    def getEnemyOrientation():
        return [self.world[('enemy', 'friend')]['orientation'], self.world[('enemy', 'me')]['orientation']]

            """
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
