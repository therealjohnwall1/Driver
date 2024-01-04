import pygame
import random
from cars import Vehicle, PlayerVehicle

gray = (100, 100, 100)  
green = (76, 208, 56)
red = (200, 0, 0)
white = (255, 255, 255)
yellow = (255, 232, 0)

pygame.init()

class Driver:
    def __init__(self, w = 500, h = 500):
        self.w = w
        self.h = h
        self.screen = pygame.display.set_mode((w, h))
        pygame.display.set_caption('Car Game')

        self.reset()

    def reset(self): #innit state of game
        self.score = 0
        self.speed = 2
        self.gameover = False
        player_x,player_y = 250,400
        self.player = PlayerVehicle(player_x,player_y)

    def move(self,action):
        if action == [0,0,0,0,1]: #right lane
            self.player.rect.x += 100
        elif action == [0,0,0,1,0]: # left lane
            self.player.rect.x -= 100
        elif action == [0,0,1,0,0]: # stay in lane
            pass
        elif action == [1,0,0,0,0]: # speed up/accel:
            self.speed += 1
        else: # slow down [0,1,0,0,0]
            self.speed -= 1 

    def step(self):
        # user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        #move car based on model output
        # self.move(action)

        #check game status
        reward = 0
        if self.gameover:
            reward = -10
            return reward,self.score
        
        else:
            reward = 10
        
        self.updateUi()

        return reward, self.gameover, self.score
        

    def placeCars(self):
        pass

    def did_crash(self,player,vehicle_group,crash_rect):
        if pygame.sprite.spritecollide(player, vehicle_group, True):
            self.gameover = True
            crash_rect.center = [player.rect.center[0], player.rect.top]
            
        
        
    def updateUi(self):
        road_width = 300
        marker_width = 10
        marker_height = 50

        # lane coordinates
        left_lane = 150
        center_lane = 250
        right_lane = 350
        lanes = [left_lane, center_lane, right_lane]

        # road and edge markers
        road = (100, 0, road_width, self.h)
        left_edge_marker = (95, 0, marker_width, self.h)
        right_edge_marker = (395, 0, marker_width, self.h)
        # for animating movement of the lane markers
        lane_marker_move_y = 0

        self.screen.fill(green)
        # draw the road
        pygame.draw.rect(self.screen, gray, road)
        
        # draw the edge markers
        pygame.draw.rect(self.screen, yellow, left_edge_marker)
        pygame.draw.rect(self.screen, yellow, right_edge_marker)
        speed = 2
        # draw the lane markers
        lane_marker_move_y += speed * 2
        if lane_marker_move_y >= marker_height * 2:
            lane_marker_move_y = 0
        for y in range(marker_height * -2, self.h, marker_height * 2):
            pygame.draw.rect(self.screen, white, (left_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
            pygame.draw.rect(self.screen, white, (center_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
        
        pygame.display.flip()        

    def move(self):
        pass