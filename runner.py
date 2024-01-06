from game import *
from model import Lmodel
import torch
import torch.nn as nn

class Runner:
    def __init__(self):
        self.model = Lmodel()
        LR = 0.001
        self.optim = torch.optim.Adam(self.model.parameters(), lr=LR)
        self.criterion = nn.MSELoss()
        self.game = Driver()

    def train(self):
        while True:
            reward, game_over, score = self.game.step()
            
            if game_over:
                self.game.reset()


    def get_state(self):
        #[what lane player is in, lane 1, how far npc from car 1 (lane1), lane 2, how far npc from car 2 (lane2), lane 3, how far npc from car 3 (lane3)]
        if self.game.player.rect.x == LEFT_LANE:
            lane = 1
        elif self.game.player.rect.x == CENTER_LANE:
            lane = 2
        else:
            lane = 3

        #lane 1 status
        for vehicle in self.game.vehicle_group:
            dist1,dist2,dist3 = -1000,-1000,-1000 #-1000 -> no car in lane
            if vehicle.rect.x == LEFT_LANE:
                dist1 = vehicle.rect.y - self.game.player.rect.y
            if vehicle.rect.x == CENTER_LANE:
                dist2 = vehicle.rect.y - self.game.player.rect.y
            if vehicle.rect.x == RIGHT_LANE:
                dist3 = vehicle.rect.y - self.game.player.rect.y
        
        state = [self.game.speed, lane, dist1, dist2, dist3]

        #state will take account
        #speed, lane, distance from car ahead


#state = [speed, lane, distance from car 1, distance from car 2 , distance from car 3]
    
if __name__ == "__main__":
    runner = Runner()
    runner.train()
