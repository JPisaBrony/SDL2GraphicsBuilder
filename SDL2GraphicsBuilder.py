import pygame, sys
from pygame.locals import *
from sdl2code import *
import subprocess

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 600
GUI_WIDTH = 160
GUI_START_X = WINDOW_WIDTH - GUI_WIDTH
GUI_COLOR = (221, 143, 255)
guiRect = (GUI_START_X, 0, GUI_START_X, WINDOW_HEIGHT)
rectTool = (GUI_START_X + 20, 40, GUI_WIDTH * 2 / 3, 30)
delTool = (GUI_START_X + 20, 120, GUI_WIDTH * 2 / 3, 30)
moveTool = (GUI_START_X + 20, 200, GUI_WIDTH * 2 / 3, 30)
toolState = 1
selRect = -1
createRect = -1
clickOccured = False

pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
font = pygame.font.Font("FreeMonoBold.ttf", 20)
white = pygame.Color(255, 255, 255)
blue = pygame.Color(0, 0, 255)
mousex = 0
mousey = 0
xOff = -1
yOff = -1
rectStartx = -1
rectStarty = -1
rects = []

def drawText(window, text, yOffset):
    msgSurf = font.render(text, False, white)
    msgRect = msgSurf.get_rect()
    msgRect.topleft = (GUI_START_X + 20, yOffset)
    window.blit(msgSurf, msgRect)

def clickCheck(rect):
    if mousex >= rect[0] and mousex <= rect[0] + rect[2] and mousey >= rect[1] and mousey <= rect[1] + rect[3]:
        return True
    return False

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == MOUSEMOTION:
            mousex, mousey = event.pos
        elif event.type == MOUSEBUTTONDOWN:
            if clickCheck(rectTool):
                toolState = 1
            elif clickCheck(delTool):
                toolState = 2
            elif clickCheck(moveTool):
                toolState = 3
            elif clickCheck(guiRect):
                break
            else:
                clickOccured = True
        elif event.type == MOUSEBUTTONUP:
            if toolState == 3:
                selRect = -1
                xOff = -1
                yOff = -1
        elif event.type == KEYDOWN:
            if event.key == K_c:
                rects = []
            elif event.key == K_s:
                buildCode(rects)
            elif event.key == K_r:
                buildCode(rects)
                subprocess.check_output(['gcc -lSDL2 main.c -o main'], shell=True)
                subprocess.call(['./main'], shell=True)
            elif event.key == K_q:
                pygame.quit()
                sys.exit(0)

    window.fill((0, 0, 0))

    for rect in rects:
        pygame.draw.rect(window, white, tuple(rect))

    pygame.draw.rect(window, GUI_COLOR, guiRect)
    drawText(window, "Rect Tool", 0)
    if toolState == 1:
        pygame.draw.rect(window, blue, rectTool)
    else:
        pygame.draw.rect(window, white, rectTool)
    drawText(window, "Delete", 80)
    if toolState == 2:
        pygame.draw.rect(window, blue, delTool)
    else:
        pygame.draw.rect(window, white, delTool)
    drawText(window, "Move", 160)
    if toolState == 3:
        pygame.draw.rect(window, blue, moveTool)
    else:
        pygame.draw.rect(window, white, moveTool)

    if clickOccured:
        if toolState == 1:
            if rectStartx == -1 and rectStarty == -1:
                rectStartx = mousex
                rectStarty = mousey
            else:
                rects.append(createRect)
                rectStartx = -1
                rectStarty = -1
        elif toolState == 2:
            for rect in reversed(rects):
                if clickCheck(rect):
                    rects.remove(rect)
                    break
        elif toolState == 3:
            if selRect == -1:
                for rect in reversed(rects):
                    if clickCheck(rect):
                        selRect = rect
                        break
    
    if selRect != -1:
        if xOff == -1 and yOff == -1:
            xOff = mousex - selRect[0]
            yOff = mousey - selRect[1]
        selRect[0] = mousex - xOff
        selRect[1] = mousey - yOff
    
    if toolState != 1:
        rectStartx = -1
        rectStarty = -1

    if rectStartx != -1 and rectStarty != -1:
        rectX = rectStartx
        rectY = rectStarty
        rectW = mousex - rectStartx
        rectH = mousey - rectStarty
        
        if rectX > mousex:
            rectX = mousex
            rectW = rectStartx - mousex
        if rectY > mousey:
            rectY = mousey
            rectH = rectStarty - mousey

        createRect = [rectX, rectY, rectW, rectH]
        pygame.draw.rect(window, white, createRect)

    clickOccured = False

    pygame.display.flip()
