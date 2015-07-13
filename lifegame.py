#
# (C)  2012  Oleksandr Dunayevskyy <oleksandr.dunayevskyy@gmail.com>
#
# Game of Life
#
# requirements: pygame

import sys
import random
import time
import re
import pygame

# number of cells on the vertical axis
v_field_rows = 0

# number of cells on the horizontal axis
v_field_cols = 0

# size of a cell in pixels
v_item_size  = 15

# delay between simulation steps
c_speed = 0.05


c_field_color       = (192,192,192)
BLACK               = (0, 0, 0, 255)
c_alive_cell_color  = BLACK
c_dead_cell_color   = (255, 255, 255, 255)


v_cells2 = []
v_cells = []
v_step = 1 # start at generation #1



def CreateField(rows,cols):
    global v_cells, v_cells2
    v_cells  = [False]*(rows*cols)
    v_cells2 = [False]*(rows*cols)
    global v_field_rows, v_field_cols, v_item_size
    v_field_rows = rows
    v_field_cols = cols
    v_item_size  = int(round(200 / v_field_rows))


def InitRandomLife():
    CreateField(16, 16)
    global v_cells
    for x in range(v_field_cols):
        for y in range(v_field_rows):
            SetCellState(v_cells, x, y, random.choice([True, False]))

def LoadLifeFile(filename):
    f = open(filename, 'r')
    header = f.readline().rstrip()
    match = re.search('(\d+)x(\d+)', header)
    (w,h) = match.groups()
    (iw,ih) = (int(w), int(h))
    print 'Width=%d  Height=%d' % (iw,ih)
    CreateField(ih,iw)
    match = re.search('\+(\d+)\+(\d+)', header)
    if match:
        offset = match.groups()
    else:
        offset = (0,0)
    for line in f:
        coord_tuples = line.rstrip().split()
        for coord in coord_tuples:
            [x,y] = coord.split(',')
            SetCellState(v_cells, int(x)+int(offset[0]), int(y)+int(offset[1]), True)
           

def GameStep():
    DrawCells()
    DrawStepLabel()
   
    global v_cells
    global v_cells2
    
    Evaluate(v_cells, v_cells2)
    
    # swap lists
    (v_cells, v_cells2) = (v_cells2, v_cells)

    global v_step
    v_step = v_step + 1
    

def GetNeighborCells(x,y):
    return [    (x-1,y-1),
                (x  ,y-1),
                (x+1,y-1),
                (x-1,y  ),
                (x+1,y  ),
                (x-1,y+1),
                (x  ,y+1),
                (x+1,y+1) ]
    
    
def Evaluate(cells_src, cells_dst):
    for x in range(v_field_cols):
        for y in range(v_field_rows):
            current_state = GetCellState(cells_src, x, y)
            neighbors = GetNeighborCells(x,y)
            num_alive_neighbors = 0
            for neighbor in neighbors:
                if True == GetCellState(cells_src, neighbor[0], neighbor[1]):
                    num_alive_neighbors = num_alive_neighbors  + 1
            if current_state == False: # currently dead
                if num_alive_neighbors == 3:
                    current_state = True # lives
            else: # currently alive
                if num_alive_neighbors < 2 or num_alive_neighbors > 3:
                    current_state = False # dies
            SetCellState(cells_dst, x, y, current_state)

# no wrap around
#def GetCellState(cells, x, y):
#    if x < 0:
#        return 1
#    elif x >= v_field_cols:
#        return 1
#    if y < 0:
#        return 1
#    elif y >= v_field_rows:
#        return 1
#    return cells[x + v_field_cols * y]
    
# wrap around
def GetCellState(cells, x, y):
    nx = x
    ny = y
    if x < 0:
        nx = v_field_cols-1
    elif x >= v_field_cols:
        nx = 0
    if y < 0:
        ny = v_field_rows-1
    elif y >= v_field_rows:
        ny = 0
    return cells[nx + v_field_cols * ny]
    
def SetCellState(cells, x, y, value):
    cell_index = x + v_field_cols * y
    cells[cell_index] = value


def DrawCells():
    for x in range(v_field_cols):
        for y in range(v_field_rows):
            cell_index = x + v_field_cols * y
            if GetCellState(v_cells,x,y) == True:
                fill_color = c_alive_cell_color
            else:
                fill_color = c_dead_cell_color
            rect = pygame.Rect(x*v_item_size + x, y*v_item_size + y, v_item_size, v_item_size)
            pygame.draw.rect(window, fill_color, rect)

def DrawStepLabel():
    basicFont = pygame.font.SysFont(None, 25)
    text = basicFont.render('gen: ' +str(v_step), True, BLACK)
    textRect = text.get_rect()
    textRect.left = 0
    textRect.top  = v_item_size*v_field_rows+v_field_rows
    window.blit(text, textRect)




# initialize life
if len(sys.argv) > 1: 
    LoadLifeFile(sys.argv[1])
else:
    InitRandomLife()


pygame.init()
pygame.display.init()
window = pygame.display.set_mode((v_item_size*v_field_cols + v_field_cols, v_item_size*v_field_rows+v_field_rows + 20))

done = False

while not done:
    evtList = pygame.event.get()
    for evt in evtList:
        if evt.type == pygame.QUIT:
            done = True
    window.fill(c_field_color)
    GameStep()
    pygame.display.update()
    time.sleep(c_speed)
pygame.quit()
