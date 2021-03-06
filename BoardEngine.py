# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 13:31:02 2022

@author: Axel
"""
import pygame as p
import Board
import time
from AgentGuigui import Agent,Observer 
WIDTH = HEIGHT = 512

DIMENSION = 4
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces=["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15",]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/"+piece+".png"),(SQ_SIZE,SQ_SIZE))
                                          
def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    screen.fill(p.Color("white"))
    pion = Agent(2,1,0,0,"1")
    pion2 = Agent(3,1,0,1,"2")
    pion3 = Agent(3,0,0,2,"3")
    pion4 =Agent(2,0,0,3,"4")
    pion5 = Agent(2,2,1,0,"5")
    pion6 = Agent(3,2,1,1,"6")   
    pion7 = Agent(2,3,1,2,"7")
    pion8 = Agent(1,3,1,3,"8") 
    pion9 = Agent(1,2,2,0,"9")
    pion10 = Agent(0,1,2,1,"10") 
    pion11 = Agent(1,0,2,2,"11") 
    pion12 = Agent(3,3,2,3,"12") 

    pawns = [pion,pion2, pion3,pion4,pion5,pion6,pion7,pion8,pion9,pion10,pion11,pion12]
    observer = Observer(pawns,4,4)
    gs=observer.board
    loadImages()
    for pawn in pawns:
        pawn.start()
        
    #pion.start()
    running=True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running=False
    
        drawBoardState(screen,gs)
        p.display.flip()
        

def drawBoardState(screen,gs):
    drawBoard(screen)#draw squares on board
    drawPieces(screen,gs)#draw pieces on top of squares
        
def drawBoard(screen):
   colors=p.Color("black")
   screen.fill(p.Color("white"))
   for r in range(DIMENSION):
       for c in range(DIMENSION):
           
           p.draw.rect(screen,colors,p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE),2)
    
    
        
def drawPieces(screen,board):   
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": #if not empty
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
                
  
    
if __name__ == "__main__": #import main in another file
    main()