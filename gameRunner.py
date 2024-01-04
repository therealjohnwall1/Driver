import pygame
import random

gray = (100, 100, 100)  
green = (76, 208, 56)
red = (200, 0, 0)
white = (255, 255, 255)
yellow = (255, 232, 0)

pygame.init()
class Driver:

    def __init__(self, w = 500, h = 500):
        self.self.screen = pygame.display.set_mode((w, h))
        self.pygame.display.set_caption('Car Game')
        #draw roads and grass
        road_width = 300
        marker_width = 10
        marker_height = 50

        # lane coordinates
        left_lane = 150
        center_lane = 250
        right_lane = 350
        lanes = [left_lane, center_lane, right_lane]

        # road and edge markers
        road = (100, 0, road_width, h)
        left_edge_marker = (95, 0, marker_width, h)
        right_edge_marker = (395, 0, marker_width, h)
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
        for y in range(marker_height * -2, h, marker_height * 2):
            pygame.draw.rect(self.screen, white, (left_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
            pygame.draw.rect(self.screen, white, (center_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
        

        self.reset()

    def reset(self): #innit state of game
        #place vehicle



    def placeCars(self):
        pass

    def step(self):
        pass

    def did_crash(self):
        pass
    def updateUi(self):
        pass

    def move(self):
        pass