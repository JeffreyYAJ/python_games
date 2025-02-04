import random, pygame, sys
from pygame.locals import *
def main():
    global fps_clock, screen
    pygame.init()
    fps_clock = pygame.time.Clock()
    screen = pygame.display.set_mode((640, 480))
    mouse_posx = 0
    mouse_posy = 0
    pygame.display.set_caption('YAJ MemGame')
    game_board = shuffleBoard()
    revealedTiles = generateRevealedTilesData(False)
    first_selection = None
    screen.fill((255,255,255))
    gameStartAnimation(game_board)
    board_final_color = (random.randint(0,100), random.randint(0,100), random.randint(0,100))
    
    while True:
        mouse_clicked = False
        screen.fill(board_final_color)
        logo_photo = pygame.image.load('./logo.png')
        logo_rect = logo_photo.get_rect()
        #logo_rect.topleft()
        screen.blit(logo_photo,logo_rect)
        drawGamingBoard(game_board, revealedTiles)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mouse_posx, mouse_posy = event.pos
            elif event.type == MOUSEBUTTONUP:
                mouse_posx, mouse_posy = event.pos
                mouse_clicked = True
                #hint click 
            elif event.type == pygame.K_LCTRL:
                boxes= []
                for x in range(10):
                    for y in range(7):
                        if revealedTiles[x][y]== False:
                            boxes.append( (x, y) )
                tiles_to_reveal= gameHintTiles(8, boxes)
                for tiles in tiles_to_reveal:    
                    revealTile(game_board, tiles)
                    coverTile(game_board, tiles)
        bb, ee = findTilesAtCoordinates(mouse_posx, mouse_posy)
        if bb != None and ee != None:
            if not revealedTiles[bb][ee]:
                highlightTiles(bb, ee)
            if not revealedTiles[bb][ee] and mouse_clicked:
                revealTile(game_board, [(bb, ee)])
                revealedTiles[bb][ee] = True
                if first_selection== None:
                    first_selection= (bb, ee)
                else:
                    q, fff = getTilesCharacteristics(game_board, first_selection[0], first_selection[1])
                    r, ggg = getTilesCharacteristics(game_board, bb, ee)
                    if q != r or fff != ggg:
                        pygame.time.wait(1000)
                        coverTile(game_board, [(first_selection[0], first_selection[1]), (bb, ee)])
                        revealedTiles[first_selection[0]][first_selection[1]] = False
                        revealedTiles[bb][ee] = False
                    elif gameWinned(revealedTiles):
                        gameCompletedAnimation(game_board)
                        pygame.time.wait(2000)
                        i = shuffleBoard()
                        revealedTiles = generateRevealedTilesData(False)
                        drawGamingBoard(game_board, revealedTiles)
                        pygame.display.update()
                        pygame.time.wait(1000)
                        gameStartAnimation(game_board)
                    first_selection= None
        pygame.display.update()
        fps_clock.tick(30)

def generateRevealedTilesData(value):
    revealedTiles = []
    for i in range(10):
        revealedTiles.append([value] * 7)
    return revealedTiles

def shuffleBoard():
    tile_image = []
    for tile_color in ((255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 128, 0), (255, 0, 255), (0, 255, 255)):
        for tile_shape in ('a', 'b', 'c', 'd', 'e'):
            tile_image.append( (tile_shape, tile_color) )
    random.shuffle(tile_image)
    tile_image = tile_image[:35] * 2
    random.shuffle(tile_image)
    board_elements = []
    for x in range(10):
        column = []
        for y in range(7):
            column.append(tile_image[0])
            del tile_image[0]
        board_elements.append(column)
    return board_elements

def gameHintTiles(vv, uu):
    ww = []
    for i in range(0, len(uu), vv):
        ww.append(uu[i:i + vv])
    return ww

def leftTopCoordinatesOfTiles(bb, ee):
    return (bb * 50 + 70, ee * 50 + 65)

def findTilesAtCoordinates(x, y):
    for bb in range(10):
        for ee in range(7):
            oo, ddd = leftTopCoordinatesOfTiles(bb, ee)
            aaa = pygame.Rect(oo, ddd, 40, 40)
            if aaa.collidepoint(x, y):
                return (bb, ee)
    return(None,None)

def drawTileShapesandColors(ss, tt, bb, ee):
    oo, ddd = leftTopCoordinatesOfTiles(bb, ee)
    if ss == 'a':
        pygame.draw.circle(screen, tt, (oo + 20, ddd + 20), 15)
        pygame.draw.circle(screen, (60, 60, 100), (oo + 20, ddd + 20), 5)
    elif ss == 'b':
        pygame.draw.rect(screen, tt, (oo + 10, ddd + 10, 20, 20))
    elif ss == 'c':
        pygame.draw.polygon(screen, tt, ((oo + 20, ddd), (oo + 40 - 1, ddd + 20), (oo + 20, ddd + 40 - 1), (oo, ddd + 20)))
    elif ss == 'd':
        for i in range(0, 40, 4):
            pygame.draw.line(screen, tt, (oo, ddd + i), (oo + i, ddd))
            pygame.draw.line(screen, tt, (oo + i, ddd + 39), (oo + 39, ddd + i))
    elif ss == 'e':
        pygame.draw.ellipse(screen, tt, (oo, ddd + 10, 40, 20))

def getTilesCharacteristics(board_elements, bb, ee):
    return board_elements[bb][ee][0], board_elements[bb][ee][1]

def coverTiles(board_elements, boxes, gg):
     for box in boxes:
        oo, ddd = leftTopCoordinatesOfTiles(box[0], box[1])
        pygame.draw.rect(screen, (60, 60, 100), (oo, ddd, 40, 40))
        ss, tt = getTilesCharacteristics(board_elements, box[0], box[1])
        drawTileShapesandColors(ss, tt, box[0], box[1])
        if gg > 0:
            pygame.draw.rect(screen, (255, 255, 255), (oo, ddd, gg, 40))
     pygame.display.update()
     fps_clock.tick(30)
     
def revealTile(board_elements, cc):
    for gg in range(40, (-8) - 1, -8):
        coverTiles(board_elements, cc, gg)
def coverTile(board_elements, ff):
    for gg in range(0, 48, 8):
        coverTiles(board_elements, ff, gg)
def drawGamingBoard(board_elements, pp):
    for bb in range(10):
        for ee in range(7):
            oo, ddd = leftTopCoordinatesOfTiles(bb, ee)
            if not pp[bb][ee]:
                pygame.draw.rect(screen, (255, 255, 255), (oo, ddd, 40, 40))
            else:
                ss, tt = getTilesCharacteristics(board_elements, bb, ee)
                drawTileShapesandColors(ss, tt, bb, ee)
def highlightTiles(bb, ee):
    oo, ddd = leftTopCoordinatesOfTiles(bb, ee)
    pygame.draw.rect(screen, (0, 0, 255), (oo - 5, ddd - 5, 50, 50), 4)
def gameStartAnimation(board_elements):
    mm = generateRevealedTilesData(False)
    boxes = []
    for x in range(10):
        for y in range(7):
            boxes.append( (x, y) )
    random.shuffle(boxes)
    kk = gameHintTiles(8, boxes)
    drawGamingBoard(board_elements, mm)
    for nn in kk:
        revealTile(board_elements, nn)
        coverTile(board_elements, nn)
        
def gameCompletedAnimation(board_elements):
    mm = generateRevealedTilesData(True)
    tt1 = (100, 100, 100)
    tt2 = (60, 60, 100)
    for i in range(13):
        tt1, tt2 = tt2, tt1
        screen.fill(tt1)
        drawGamingBoard(board_elements, mm)
        pygame.display.update()
        pygame.time.wait(300)
        
def gameWinned(revealedTiles):
    for i in revealedTiles:
        if False in i:
            return False
    return True

if __name__ =="__main__":
    main()
