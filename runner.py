from game import *
from model import Nmodel
import torch
import torch.nn as nn
from collections import deque
import numpy as np
MAX_MEM = 100_000
BATCH = 1000
HIGH_SCORE = 0

#agent
class Runner:
    def __init__(self):
        self.model = Nmodel(6,64,32,5)
        LR = 0.01
        self.gamma = 0.1
        self.optim = torch.optim.Adam(self.model.parameters(), lr=LR)
        self.criterion = nn.MSELoss()
        self.num_games = 0
        self.memory = deque(maxlen=MAX_MEM)
        #change later

    def train(self):
        game = Driver()
        runner = Runner()
        max_score = 0
        while True:
            old_state = runner.get_state(game)
            final_move = runner.move(old_state)
            game.updateUi()
            reward, game_over, score = game.step(final_move)
            new_state = runner.get_state(game)

            runner.short_mem(old_state,final_move,reward,new_state,game_over)

            runner.mem_append(old_state, final_move, reward, new_state,game_over)
            
            if game_over:
                game.reset()
                runner.num_games +=1
                runner.long_mem()

                if score > max_score:
                    max_score = score
                    self.model.save()

                print(f"Game {runner.num_games} Score: {score} Record: {max_score}")
                print(f"Epsilon: {40 - runner.num_games}")

    def get_state(self,game):
        #add position of car ahead on board
        #add if danger is left or right
        #[what lane player is in, lane 1, how far npc from car 1 (lane1), lane 2, how far npc from car 2 (lane2), lane 3, how far npc from car 3 (lane3)]
        if game.player.rect.x == LEFT_LANE:
            player_lane = 100
        elif game.player.rect.x == CENTER_LANE:
            player_lane = 200
        else:
            player_lane = 300

        #get closest car on screen
        left_open = True
        center_open = True
        right_open = True
        dist_btwn = -100
        vehicles = game.vehicle_group.sprites()
        if len(vehicles) >0:
            cloest = vehicles[0]
            cloest_x = cloest.rect.x
            if cloest_x == LEFT_LANE:
                left_open = False
            if cloest_x == CENTER_LANE:
                center_open = False
            if cloest_x == RIGHT_LANE:
                right_open = False
            dist_btwn = cloest.rect.y - game.player.rect.y
        
    
        state = np.array([game.speed,player_lane,left_open,center_open,right_open,dist_btwn],dtype = int) #5 len

        return state
        #state will take account
        #speed, lane, distance from car ahead
    

    #training 
    def mem_append(self,state,action,reward,next_state,game_over):
        #add to memory queue of tuples
        self.memory.append((state,action,reward,next_state,game_over))
    
    def short_mem(self,state,action,reward,next_state,done):
        self.train_step(state, action, reward, next_state, done)

    def long_mem(self):
        if len(self.memory) > BATCH:
            sample = random.sample(self.memory, BATCH)
        else:
            sample = self.memory
        states,actions,rewards,next_states,dones = zip(*sample)
        #groups all states,...,dones together from sample
        #appending batches to memory
        self.train_step(states,actions,rewards,next_states,dones)


    #training methods
    def train_step(self, state, action, reward, next_state, done):
        #calculate q values for each possible action in state(bellman equation)
        #choose best one using argmax
        state = torch.tensor(state,dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)


        if len(state.shape) == 1:
            # (1, x)
            state = torch.unsqueeze(state, 0)# adds extra dimension to state(makes it 2d)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

            pred = self.model(state)

            target = pred.clone()
            # print(f"{state}  status")
            # print(f"{target.detach().numpy()}  prediction") 

            #bellman equation
            for index in range(len(done)):
                Q_new = reward[index]
                if not done[index]:
                    Q_new = reward[index] + self.gamma * torch.max(self.model(next_state[index]))
                
                target[index][torch.argmax(action[index]).item()] = Q_new
                #Q value = reward for action in a state

            # 2: Q_new = r + y * max(next_predicted Q value) -> only do this if not done
            # pred.clone()
            # preds[argmax(action)] = Q_new
                
            #backpropagation
            self.optim.zero_grad()
            loss = self.criterion(target, pred)
            loss.backward()

            self.optim.step()

    def move(self,state):
        #exploration vs exploitation
        epsilon =  40 - self.num_games
        #more games less epsilon, less random moves

        final_move = [0,0,0,0,0]
        if random.randint(0,200) < epsilon:
            move = random.randint(0,4)
            final_move[move] = 1
        else:
            #state as tensor
            state0 = torch.tensor(state,dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item() 
            final_move[move] = 1
        return final_move

    
if __name__ == "__main__":
    runner = Runner()
    runner.train()
