import pygame
import os
import sys
import time
import random
from itertools import permutations, combinations

pygame.init()
farmer_img = pygame.image.load('farmer.jpg')
wolf_img = pygame.image.load('wolf.jpg')
flower_img = pygame.image.load('flower.jpg')
goat_img = pygame.image.load('goat.jpg')
raft_img = pygame.image.load('raft.jpg')
row_img = pygame.image.load('row.jpg')

clock = pygame.time.Clock()

white = (255,255,255)
lightsalmon = (255,160,122)
salmon = (250,128,114)
red = (255,0,0)
green = (34,177,76)
blue = (0,0,255)
black = (0,0,0)

#display params
height=650
width=780

gameDisplay = pygame.display.set_mode((width,height))
pygame.display.set_caption('River Crossing Level 1')


animals_on_right = {'farmer_img': 1, 'wolf_img': 1, 'goat_img': 1,'flower_img': 1}
animals_on_left = {'farmer_img': 0, 'wolf_img': 0, 'goat_img': 0,'flower_img': 0}
    

num_animals = 0
size = 80
gameDisplay.fill(white)

font = pygame.font.SysFont(None, 25)
def text_objects(msg,color):
    surf = font.render(msg,True,color)
    return surf , surf.get_rect()

def message_to_board(msg,color):
    textSurface, textRect = text_objects(msg,color)
    textRect.center = (width/2),50
    pygame.draw.rect(gameDisplay, white, [(width/2)-150,10,350,50])
    gameDisplay.blit(textSurface,textRect)    
    pygame.display.update()
    
def score_to_board(score,color):
    
    textSurface, textRect = text_objects(score,color)
    textRect.center = (width/2)+300,50
    pygame.draw.rect(gameDisplay, white, [(width/2)+250,30,100,50])
    gameDisplay.blit(textSurface,textRect)    
    pygame.display.update()
    
def raft_movement(raft_position,animals_onboard):
                                print("button clicked")
                                Transfer = False
                                if raft_position == "right":
                                        x_lead = 0
                                else:
                                        x_lead = 300
                                        
                                       
                                while not Transfer:
                                    pygame.draw.rect(gameDisplay, white, [width-(320+x_lead),height-300,220,100])
                                    if animals_onboard[0] != 0:
                                        print("========================")
                                        print(width-(290+x_lead))
                                        pygame.draw.rect(gameDisplay, white, [width-(290+x_lead),height-350,100,100])
                                    if animals_onboard[1] != 0:
                                        pygame.draw.rect(gameDisplay, white, [width-(210+x_lead),height-350,100,100])    
                                    if raft_position == "right":
                                        x_lead += 10
                                    else:
                                        x_lead -= 10
                                    
                                    render_image(raft_img,320+x_lead,300,220,100)
                                    if animals_onboard[0] != 0:
                                        print("========================")
                                        print(width-(290+x_lead))
                                        render_image(animals_onboard[0],290+x_lead,350,80,80)
                                        
                                    if animals_onboard[1] != 0:
                                        render_image(animals_onboard[1],210+x_lead,350,80,80)
                                        
                                    
                                    pygame.display.update()
                                    if x_lead == 300 and raft_position == "right":
                                        break;
                                    if x_lead == 0 and raft_position == "left":
                                        break;
                                    clock.tick(18)
                                if raft_position == "right":    
                                    raft_position="left"
                                else:
                                    raft_position="right"
                                return raft_position
                                

def check_if_animal_present(raft_position,img_name):
    if  raft_position == "right" and animals_on_right[img_name] == 1:
        animals_on_right[img_name] = 0
        return 1
    elif raft_position == "left" and animals_on_left[img_name] == 1:
        animals_on_left[img_name] = 0
        return 1
    return 0

def render_image(image_name,x,y,w,h): 
    charRect = pygame.Rect((0,0),(w,h))
    image_name = pygame.transform.scale(image_name, charRect.size)
    image_name = image_name.convert()
    gameDisplay.blit(image_name, (width-x, height-y))

def animal_placement(animals_onboard,img_name):
    if num_animals <= 2:
            if animals_onboard[0] == 0:
                    animals_onboard[0]=img_name
            else:
                    animals_onboard[1]=img_name
            print(animals_onboard)
    return animals_onboard       
def raft_can_move(animals_onboard, raft_position):
    if list(animals_on_right.values())[0] == 0 and list(animals_on_left.values())[0] == 0:
      if raft_position == "right": 
        if list(animals_on_right.values())[1] == 1 and list(animals_on_right.values())[2] == 1:
            message_to_board("wolf eats goat if farmer goes away",red)
        elif list(animals_on_right.values())[2] == 1 and list(animals_on_right.values())[3] == 1:
            message_to_board("goat eats flower if farmer goes away",red)
        else:
            return 1

      if raft_position == "left":
        if list(animals_on_left.values())[1] == 1 and list(animals_on_left.values())[2] == 1:
            message_to_board("wolf eats goat if farmer goes away",red)
        elif list(animals_on_left.values())[2] == 1 and list(animals_on_left.values())[3] == 1:
            message_to_board("goat eats flower if farmer goes away",red)
        else:
            return 1
          
    else:
        message_to_board("farmer should steer the raft",red)
        return 0
        

def gameloop():
    num_moves = 0
    animals_onboard=[0,0]
    gameExit = False
    raft_position = "right"
    global num_animals
    while not gameExit:
        for event in pygame.event.get():
            if pygame.mouse.get_pressed()[0] == 1:    
                print(pygame.mouse.get_pos())
                vals= pygame.mouse.get_pos()
                x_val = vals[0]  
                y_val = vals[1]
                if num_animals != 0:
                        if x_val >= width-(width/2+50) and x_val <= width-(width/2+50)+100:
                            
                            if y_val >= height-(height-100) and y_val <= height-(height-100)+50:
                                    message_to_board("",red)
                                    if raft_can_move(animals_onboard,raft_position):
                                        raft_position = raft_movement(raft_position,animals_onboard)
                                        num_moves += 1
                                        score_to_board(str(num_moves),red)
                                        print(raft_position)
                                        if num_animals == 2:
                                            print("2 animals already on board...! :p")
                                        
                else:
                    if x_val >= width-(width/2+50) and x_val <= width-(width/2+50)+100:
                            
                            if y_val >= height-(height-100) and y_val <= height-(height-100)+50:
                                if num_animals == 0:
                                    print("Raft cannot row itself...! :p")
                                    message_to_board("Raft cannot row itself!!!",red)
                                
                                    
                            
               # move animals from right shore on the raft on click event


                if num_animals < 2:
                    if x_val >= width-100 and x_val <= width and raft_position == "right":
                        if y_val >= height-200 and y_val <= height-100:
                          if farmer_img not in animals_onboard: 
                            print("clicked object: farmer")
                            if check_if_animal_present(raft_position,"farmer_img"):
                                draw_on_raft(farmer_img,100,200,raft_position)
                                animals_onboard=animal_placement(animals_onboard,farmer_img)
                            
                                  
                        if y_val >= height-300 and y_val <= height-200:
                          if wolf_img not in animals_onboard:  
                            print("clicked object: wolf")
                            if check_if_animal_present(raft_position,"wolf_img"):
                                draw_on_raft(wolf_img,100,300,raft_position)
                                animals_onboard=animal_placement(animals_onboard,wolf_img)
            
                        if y_val >= height-400 and y_val <= height-300:
                          if goat_img not in animals_onboard:  
                            print("clicked object: goat")
                            if check_if_animal_present(raft_position,"goat_img"):
                                draw_on_raft(goat_img,100,400,raft_position)
                                animals_onboard=animal_placement(animals_onboard,goat_img)
                                  
                                  
                        if y_val >= height-500 and y_val <= height-400:
                          if flower_img not in animals_onboard:  
                            print("clicked object: flower")
                            if check_if_animal_present(raft_position,"flower_img"):
                                draw_on_raft(flower_img,100,500,raft_position)
                                animals_onboard=animal_placement(animals_onboard,flower_img)

                            
                    # move animals from left shore on the raft on click event 
                    if x_val >= 0 and x_val <= 100 and raft_position == "left":
                        if y_val >= height-200 and y_val <= height-100:
                          if farmer_img not in animals_onboard:  
                            print("clicked object: farmer")
                            if check_if_animal_present(raft_position,"farmer_img"):
                                draw_on_raft(farmer_img,780,200,raft_position)
                                animals_onboard=animal_placement(animals_onboard,farmer_img)
                            
                                  
                        if y_val >= height-300 and y_val <= height-200:
                          if wolf_img not in animals_onboard:  
                            print("clicked object: wolf")
                            if check_if_animal_present(raft_position,"wolf_img"):
                                draw_on_raft(wolf_img,780,300,raft_position)
                                animals_onboard=animal_placement(animals_onboard,wolf_img)
            
                        if y_val >= height-400 and y_val <= height-300:
                          if goat_img not in animals_onboard:  
                            print("clicked object: goat")
                            if check_if_animal_present(raft_position,"goat_img"):
                                draw_on_raft(goat_img,780,400,raft_position)
                                animals_onboard=animal_placement(animals_onboard,goat_img)
                                  
                                  
                        if y_val >= height-500 and y_val <= height-400:
                          if flower_img not in animals_onboard:   
                            print("clicked object: flower")
                            if check_if_animal_present(raft_position,"flower_img"):
                                draw_on_raft(flower_img,780,500,raft_position)
                                animals_onboard=animal_placement(animals_onboard,flower_img)        
                else:
                    
                    print ("Raft carries only 2 animals!!!")
                    
                    
                        
                if x_val >= width-290 and x_val <= width-210:
                    if y_val >= height-350 and y_val <= height-270:
                        if animals_onboard[0]==farmer_img:
                            im_name = "farmer_img"
                            x,y=100,200
                        elif  animals_onboard[0]==wolf_img:
                            im_name = "wolf_img"
                            x,y=100,300
                        elif  animals_onboard[0]==goat_img:
                            im_name = "goat_img"
                            x,y=100,400
                        elif  animals_onboard[0]==flower_img:
                            im_name = "flower_img"
                            x,y=100,500    
                        remove_from_raft(animals_onboard[0],x,y,0,raft_position)
                        print("removing 1st animal from the list")
                        animals_onboard[0] = 0
                        print(animals_onboard)
                        animals_on_right[im_name] = 1
                if x_val >= width-210 and x_val <= width-130:
                    if y_val >= height-350 and y_val <= height-270:
                        print(num_animals)
                        if animals_onboard[1]==farmer_img:
                            im_name = "farmer_img"
                            x,y=100,200
                        elif  animals_onboard[1]==wolf_img:
                            im_name = "wolf_img"
                            x,y=100,300
                        elif  animals_onboard[1]==goat_img:
                            im_name = "goat_img"
                            x,y=100,400
                        elif  animals_onboard[1]==flower_img:
                            im_name = "flower_img"
                            x,y=100,500
                        print ("===================")
                        print(x)
                        print(y)
                        remove_from_raft(animals_onboard[1],x,y,1,raft_position)
                        print("removing 2nd animal from the list")
                        animals_onboard[1] = 0
                        print(animals_onboard)
                        animals_on_right[im_name] = 1

                # remove from raft on right side        
                if x_val >= width-590 and x_val <= width-510:
                    if y_val >= height-350 and y_val <= height-270:
                        if animals_onboard[0]==farmer_img:
                            im_name = "farmer_img"
                            x,y=780,200
                        elif  animals_onboard[0]==wolf_img:
                            im_name = "wolf_img"
                            x,y=780,300
                        elif  animals_onboard[0]==goat_img:
                            im_name = "goat_img"
                            x,y=780,400
                        elif  animals_onboard[0]==flower_img:
                            im_name = "flower_img"
                            x,y=780,500    
                        remove_from_raft(animals_onboard[0],x,y,0,raft_position)
                        print("removing 1st animal from the list")
                        animals_onboard[0] = 0
                        print(animals_onboard)
                        
                        animals_on_left[im_name] = 1
                        print (animals_on_left)
                        
                if x_val >= width-510 and x_val <= width-430:
                    if y_val >= height-350 and y_val <= height-270:
                        print(num_animals)
                        if animals_onboard[1]==farmer_img:
                            im_name = "farmer_img"
                            x,y=780,200
                        elif  animals_onboard[1]==wolf_img:
                            im_name = "wolf_img"
                            x,y=780,300
                        elif  animals_onboard[1]==goat_img:
                            im_name = "goat_img"
                            x,y=780,400
                        elif  animals_onboard[1]==flower_img:
                            im_name = "flower_img"
                            x,y=780,500
                        print ("===================")
                        print(x)
                        print(y)
                        remove_from_raft(animals_onboard[1],x,y,1,raft_position)
                        print("removing 2nd animal from the list")
                        animals_onboard[1] = 0
                        print(animals_onboard)

                        animals_on_left[im_name] = 1
                        print (animals_on_left)
                
                        
                    
                    
                    
def remove_from_raft(img_name,x,y,clicked_index,raft_position):
    global num_animals
    if raft_position == "right":
        raft_x1,raft_x2=290,210
    else:
        raft_x1,raft_x2=590,510
        
    if num_animals == 2 or num_animals == 1:
            if clicked_index == 0:
                pygame.draw.rect(gameDisplay, white, [width-raft_x1,height-350,80,80])
                    
            else:
                pygame.draw.rect(gameDisplay, white, [width-raft_x2,height-350,80,80])
            render_image(img_name,x,y,100,100)  
            pygame.display.update()
            num_animals -= 1
    else:
            print ("Raft has no animals on-board!!!")
            #message_to_board("Raft has no animals on-board!!!",red)
    

def draw_on_raft(img_name,x,y,raft_position):
    global num_animals
            
    if raft_position == "right":
        if num_animals == 0:
            raft_x,raft_y=290,350
        elif num_animals == 1:
            raft_x,raft_y=210,350
    
    elif raft_position == "left":
        if num_animals == 0:
            raft_x,raft_y=590,350
        elif num_animals == 1:
            raft_x,raft_y=510,350
            
    render_image(img_name,raft_x,raft_y,80,80)
    pygame.draw.rect(gameDisplay, white, [width-x,height-y,100,100])
    pygame.display.update()
    num_animals += 1   
    
    
def draw_characters():
    w=100
    h=100
    render_image(farmer_img,100,200,w,h)
    render_image(wolf_img,100,300,w,h)
    render_image(goat_img,100,400,w,h)
    render_image(flower_img,100,500,w,h)
    


draw_characters()
textSurface, textRect = text_objects("#MOVES",red)
textRect.center = (width/2)+300,20
gameDisplay.blit(textSurface,textRect)

textSurface, textRect = text_objects("Game Instructions",blue)
textRect.center = (width/2),520
gameDisplay.blit(textSurface,textRect)
textSurface, textRect = text_objects("1. Only farmer can row the raft",blue)
textRect.center = (width/2),550
gameDisplay.blit(textSurface,textRect)
textSurface, textRect = text_objects("2. Raft can accommodate maximum 2 entities at a time",blue)
textRect.center = (width/2),580
gameDisplay.blit(textSurface,textRect)
textSurface, textRect = text_objects("3. If farmer is not around , goat eats flower",blue)
textRect.center = (width/2),610
gameDisplay.blit(textSurface,textRect)
textSurface, textRect = text_objects("4. If farmer is not around , wolf eats goat",blue)
textRect.center = (width/2),640
gameDisplay.blit(textSurface,textRect)



score_to_board("0",red)
render_image(raft_img,320,300,220,100)
render_image(row_img,width/2+50,height-100,100,50)
pygame.display.update()

gameloop()

    
