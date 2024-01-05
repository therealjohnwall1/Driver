from theGame import Driver
from model import *


class Agent:
    def __init__(self):
        # self.model = Model()
        pass
    def train(self):
        game = Driver()
        while True:
            reward, gameOver, score = game.step()
            if gameOver:
                game.reset()

    def getState(self):
        #state will take account
        #speed, lane, distance from car ahead
        pass


    
if __name__ == "__main__":
    agent = Agent()
    agent.train()
