import pygame
import random
from cars import Vehicle, PlayerVehicle
import random


LEFT_LANE = 150
CENTER_LANE = 250
RIGHT_LANE = 350

gray = (100, 100, 100)  
green = (76, 208, 56)
red = (200, 0, 0)
white = (255, 255, 255)
yellow = (255, 232, 0)

pygame.init()

class Driver:

    def __init__(self, w = 500, h = 500):
        self.w = w
        self.height = h
        self.screen = pygame.display.set_mode((w, h))
        pygame.display.set_caption('Car Game')
        self.player_group = pygame.sprite.Group()
        self.vehicle_group = pygame.sprite.Group()

        self.lanes = [LEFT_LANE, CENTER_LANE, RIGHT_LANE]
        #testing
        self.shift = 0
        self.reset()

    def reset(self): #innit state of game
        self.player_group.empty()
        self.score = 0
        self.speed = 2
        self.gameover = False
        self.player = PlayerVehicle(250, 400)
        self.player_group.add(self.player)
        self.vehicle_group.empty()

#for testing
    def human_move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.rect.x -= 100
        if keys[pygame.K_RIGHT]:
            self.player.rect.x += 100
        if keys[pygame.K_UP]:
            self.speed += 0.25
        if keys[pygame.K_DOWN]:
            self.speed -= 0.25
    
    def model_move(self,action):
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

    def step(self,action):
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
            return reward,self.gameover,self.score
        
        else:
            reward = 10

        
        self.placeCars()
        self.model_move(action)
        self.updateUi()

        return reward, self.gameover, self.score
        

    def placeCars(self):
        image_filenames = ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png']
        if len(self.vehicle_group)<3:
            add_car = True
            for vehicle in self.vehicle_group: #ensure car can fit
                if vehicle.rect.top < vehicle.rect.height * 1.5:
                    add_car = False
            if add_car:
                lane = random.choice(self.lanes)
                # select a random vehicle image
                image = pygame.image.load('images/' + random.choice(image_filenames))
                vehicle = Vehicle(image, lane, self.height / -2)
                self.vehicle_group.add(vehicle)
        # move the vehicles
        for vehicle in self.vehicle_group:
            vehicle.rect.y += self.speed
            if vehicle.rect.top > self.height:
                vehicle.kill()
                self.score += 1

        self.did_crash(self.player,self.vehicle_group)
     

    def did_crash(self,player,vehicle_group):
        #check if touch car or go off road
        if player.rect.center[0] < LEFT_LANE or player.rect.center[0] > RIGHT_LANE:
            self.gameover = True
        crash_rect = pygame.image.load('images/crash.png').get_rect()
        if pygame.sprite.spritecollide(player, vehicle_group, True):
            self.gameover = True
            crash_rect.center = [player.rect.center[0], player.rect.top]
            
        #checking if player hits from the side
        
        return self.gameover
        
    def updateUi(self):
        self.drawRoad() #draw road
        #place player car
        self.player_group.draw(self.screen)
        
        self.human_move() # testing 
        #place vehicles
        self.vehicle_group.draw(self.screen)
        
        #display score on screen
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render('Score: ' + str(self.score), True, white)
        text_rect = text.get_rect()
        text_rect.center = (50, 400)
        self.screen.blit(text, text_rect)
        
        #display speed on screen
        speed_text = font.render('Speed: ' + str(self.speed), True, white)
        speed_rect = speed_text.get_rect()
        speed_rect.center = (50, 420)
        self.screen.blit(speed_text, speed_rect)
        
        pygame.display.flip()        


    def drawRoad(self):
        road_width = 300
        marker_width = 10
        marker_height = 50
        # lane coordinates
        # road and edge markers
        road = (100, 0, road_width, self.height)
        left_edge_marker = (95, 0, marker_width, self.height)
        right_edge_marker = (395, 0, marker_width, self.height)
        # for animating movement of the lane markers
        lane_marker_move_y = 0

        self.screen.fill(green)
        # draw the road
        pygame.draw.rect(self.screen, gray, road)
        
        # draw the edge markers
        pygame.draw.rect(self.screen, yellow, left_edge_marker)
        pygame.draw.rect(self.screen, yellow, right_edge_marker)
        # draw the lane markers

        #has delay
        # self.shift += self.speed*0.5

        # lane_marker_move_y += self.speed * 2
        # if lane_marker_move_y >= marker_height * 2:
        #     lane_marker_move_y = 0
        
        # for y in range(marker_height * -2, self.height + marker_height * 2, marker_height * 2):
        #     pygame.draw.rect(self.screen, white, (LEFT_LANE + 45, y + lane_marker_move_y + self.shift % self.height, marker_width, marker_height))
        #     pygame.draw.rect(self.screen, white, (CENTER_LANE + 45, y + lane_marker_move_y + self.shift % self.height, marker_width, marker_height))

        lane_marker_move_y += self.speed * 2
        if lane_marker_move_y >= marker_height * 2:
            lane_marker_move_y = 0
        for y in range(marker_height * -2, self.height, marker_height * 2):
            pygame.draw.rect(self.screen, white, (LEFT_LANE + 45, y + lane_marker_move_y, marker_width, marker_height))
            pygame.draw.rect(self.screen, white, (CENTER_LANE + 45, y + lane_marker_move_y, marker_width, marker_height))