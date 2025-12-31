
import random

import pygame
import sys
from pygame.locals import*



S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['.....',
      '0000.',
      '.....',
      '.....',
      '.....'],
    ['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]







tetris_shapes = [S, Z, I, O, J, L, T]

#colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

information={'screen_x':700, 'screen_y':800, 'horizontal_block': 10, 'vertical_block': 20 , 'block_size': 30,'block_speed':500,'board_x':300,'board_y':600} #board will be a rectangle from (100,300) to (400,900)

top_left_x=150#(information['screen_x']-information['board_x'])//2 #top left of the board

top_left_y=100#information['screen_y']-information['board_y']




class Piece(object):
    def __init__(self,column,row,shape):#block object
        self.column=column#int
        self.row=row#ine
        self.shape=shape#list of possible rotation of the shape
        self.color=colors[tetris_shapes.index(shape)]#image file
        self.rotation=0


def create_grid(pos={}): #create a two dimentional list that contains information about each block
    grid=[[ None for x in range(information['horizontal_block'])]for y in range(information['vertical_block'])]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in pos:
                grid[i][j]=pos[(j,i)]
    return grid

def get_shape(): 

    return Piece(5,0,random.choice(tetris_shapes))

def draw_grid(surface,col,row): #draw the grid of the board
    for i in range(row):
        pygame.draw.line(surface,(128,128,128),(top_left_x,top_left_y+i*information['block_size']),(top_left_x+information['board_x'],top_left_y+i*information['block_size']))
    for i in range(col):
        pygame.draw.line(surface,(128,128,128),(top_left_x+i*information['block_size'],top_left_y),(top_left_x+i*information['block_size'],top_left_y+information['board_y']))

def validity(shape,grid): #True if is a valid pos

    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == None] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_form(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1 or not( pos[0] <= information['horizontal_block']-1 and pos[0]>=0):
                return False
    return True


def convert_shape_form(shape):
    positions=[]
    shape_format=shape.shape[shape.rotation%len(shape.shape)]

    for i, line in enumerate(shape_format):
        for j,column in enumerate(line):
            if column=='0':
                positions.append((shape.column+j-2,shape.row+i-4))
    
    return positions

def lost(positions):#check if the game is lost
    for i in positions:#input a formatted shape
        if i[1]<0:
            return True

    return False

def clear_rows(grid, locked):
    
    rows=[]#(row index, shift)
    shift=0
    total=0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if None not in row:
            shift+=1
            total+=1
            for j in range(len(row)):
                try:
                    del locked[(j,i)]
                except:
                    continue
        else:
            rows.append((i,shift))

    for y in rows:
        for x in range(information['horizontal_block']):
            if (x,y[0]) in locked:
                locked[(x,sum(y))]=locked.pop((x,y[0]))
    return total
'''
    for key in sorted(list(locked), key=lambda x: x[1],reverse=True):
        if key[1] in rows:
            x,y=key
            y+=rows[rows.index(key[1])][1]
            locked[(x,y)]
    return total
           

    for i in adj_row:
        shift_rows+=i
        temp=ind.pop(0)
        for key in sorted(list(locked), key=lambda x: x[1],reverse=True):
            x, y = key
            if y < temp:
                newKey = (x, y + shift_rows)
                locked[newKey] = locked.pop(key)
    return sum(adj_row)
'''

def score_count(row,level):
    if level>19:
        level=19
    if row == 1:
        return 40*(level)
    elif row == 2:
        return 100*(level)
    elif row == 3:
        return 300*(level)
    elif row == 4:
        return 1200*(level)
    else:
        return 0


def draw_window(surface, grid, score=0, last_score = 0, level = 0):
    surface.fill((150, 150, 150))
    pygame.font.init()
    # font = pygame.font.SysFont('comicsans', 60)
    # label = font.render('Tetris', 1, (255, 255, 255))

    # surface.blit(label, (top_left_x + information['board_x'] / 2 - (label.get_width() / 2), top_left_y//2-30))

    # current score

    sx = top_left_x + information['board_x'] 
    sy = top_left_y + information['board_y'] /2 - 100

    font = pygame.font.SysFont('comicsans', 30)

    label=font.render('Level: '+str(level), 1 ,(255, 255, 255))
    surface.blit(label, (sx+30, sy-100))
    pygame.draw.rect(surface, (100,100,100), (sx+15, sy-110, 200,70),3)

    # last score

    label = font.render('High Score:',1,(255,255,255))
    surface.blit(label,(sx+30, sy-10))


    label = font.render(str(last_score), 1, (255,255,255))
    surface.blit(label, (sx+50 , sy + 40))
    pygame.draw.rect(surface, (100,100,100), (sx+15, sy-20, 200,110),3)


    label = font.render('Score: ' , 1, (255,255,255))
    surface.blit(label, (sx+30 , sy + 110))



    label = font.render(str(score), 1, (255,255,255))
    surface.blit(label, (sx+50, sy+150))
    pygame.draw.rect(surface, (100,100,100), (sx+15, sy+100, 200, 110),3)
    



    #pygame.draw.rect(surface , (128,128,128), (sx+15, sy+15, 200,110),3)


    sx = top_left_x - 200
    sy = top_left_y + 200


    pygame.draw.rect(surface, (0, 0, 0), (top_left_x+5, top_left_y+5, information['board_x']-10, information['board_y']-10))


    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] is None:
                pygame.draw.rect(surface, (0,0,0), (top_left_x + j*information['block_size'], top_left_y + i*information['block_size'], information['block_size'], information['block_size']), 0)
            else:
                surface.blit(grid[i][j],(top_left_x + j*information['block_size'], top_left_y + i*information['block_size']))
            #pygame.draw.rect(surface, grid[i][j], (top_left_x + j*information['block_size'], top_left_y + i*information['block_size'], information['block_size'], information['block_size']), 0)

    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, information['board_x'], information['board_y']), 5)

    draw_grid(surface, information['horizontal_block'], information['vertical_block'])

def top_score(current=None):
    
    try:
        f=open('scores.txt', 'r', encoding='utf-8')
    except Exception:
        top=0
    else:
        top=f.read()
        f.close()

    if current is None:
        return top
    
    if int(top)<current:
        f=open('scores.txt','w',encoding='utf-8')
        f.write(str(current))
        f.close()
def pause(text,surface):

    grey=pygame.transform.scale(pygame.image.load('grey.png').convert_alpha(),(information['screen_x'],information['screen_y']))
    grey.set_alpha(200)
    

    surface.blit(grey,(0,0))

    font = pygame.font.SysFont('comicsans', 50)
    label = font.render(text, 1, (255, 255, 255))

    surface.blit(label, (information['screen_x'] / 2 - (label.get_width() / 2), information['screen_y']/2-100))
    pygame.display.update()
    run=True
    while run:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            if event.type==KEYDOWN:
                run=False    


def main():
    global information, colors
    pygame.init()


    surface=pygame.display.set_mode((information['screen_x'],information['screen_y']))
    pygame.display.set_caption("Tetris_By_Harry")

    lightblue=pygame.image.load('lightblue.png').convert()
    darkblue=pygame.image.load('darkblue.png').convert()
    red=pygame.image.load('red.png').convert()
    yellow= pygame.image.load('yellow.png').convert()
    orange=pygame.image.load('orange.png').convert()
    green=pygame.image.load('green.png').convert()
    purple=pygame.image.load('purple.png').convert()


    colors=[green, red, lightblue, yellow, darkblue,orange, purple]

    for i in range(len(colors)):
        colors[i]=pygame.transform.scale(colors[i],(information['block_size'],information['block_size']))
    
    pause('Press Any Key To Start',surface)

    while True:
        locked_pos={} #fixed blocks, dictionary, (R,G,B)
        next_piece=False 
        current_block=get_shape()
        next_block=get_shape()
        
        clock=pygame.time.Clock()
        score=0
        fall_time=0
        pygame.key.set_repeat(200)
        level=1
        cleared=0

        while True:
            grid=create_grid(locked_pos)

            fall_time+=clock.get_rawtime()
            clock.tick()

            if fall_time > information['block_speed']:

                fall_time = 0
                current_block.row += 1
                if not(validity(current_block, grid)) and current_block.row > 0:
                    current_block.row -= 1
                    next_piece = True
                    pygame.time.delay(200)
                else:
                    score+=1


                        
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == KEYDOWN:
                    
                    if event.key==K_DOWN: 
                        information['block_speed']=100
                    
                    elif event.key == K_RIGHT:
                        current_block.column+=1
                        if not validity(current_block,grid) or next_piece:
                            current_block.column-=1
                    
                    elif event.key == K_LEFT:
                        current_block.column-=1
                        if not validity(current_block,grid) or next_piece:
                            current_block.column+=1

                    elif event.key == K_UP:
                        current_block.rotation+=1
                        if not validity(current_block,grid):
                            current_block.rotation-=1
                
                    elif event.key == K_SPACE:
                        while True:
                            current_block.row+=1
                            if not validity(current_block, grid):
                                current_block.row-=1
                                break
                            else:
                                score +=2
                        next_piece=True
                    elif event.key== K_ESCAPE:
                        pause('Press Any Key To Continue',surface)



                
                if event.type == KEYUP:
                    if event.key==K_DOWN:
                        information['block_speed']=(0.8-((level-1)*0.007))*1000
                
            shape_pos = convert_shape_form(current_block)

            for i in range(len(shape_pos)):
                if shape_pos[i][1]>-1:
                    grid[shape_pos[i][1]][shape_pos[i][0]]=current_block.color
            
            if next_piece:
                for pos in shape_pos:
                    locked_pos[(pos[0],pos[1])]=current_block.color
                current_block=next_block
                next_block=get_shape()

                next_piece=False
                temp_rows=clear_rows(grid,locked_pos)
                score += score_count(temp_rows, level)
                cleared+=temp_rows

                if cleared>10:
                    cleared-=10
                    level+=1
                if lost(locked_pos):
                    pause('Game Over',surface)
                    break

            draw_window(surface, grid, score,last_score=top_score(), level=level)
            pygame.display.update()
            top_score(score)
            
                



main()