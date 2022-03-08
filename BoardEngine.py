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

DIMENSION = 5
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces=["sablier","croix-encerclée","plus","étoile"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/"+piece+".png"),(SQ_SIZE,SQ_SIZE))
                                          
def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    screen.fill(p.Color("white"))
    pion = Agent(0,0,2,4,"étoile")
    pion2 = Agent(0,1,2,2,"plus")
    pion3 = Agent(0,2,1,3,"croix-encerclée")
    pion4 = Agent(4,2,1,2,"étoile")
    pion5 = Agent(4,1,1,4,"plus")
    pawns = [pion,pion2, pion3,pion4,pion5]
    observer = Observer(pawns,5,5)
    gs=observer.board
    loadImages()
    pion.start()
    pion2.start()
    pion3.start()
    pion4.start()
    pion5.start()
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