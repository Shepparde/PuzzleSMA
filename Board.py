# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 11:53:42 2022

@author: Axel
"""


class BoardState():
    def __init__(self):
        self.board=[
            ["--","--","croix-encerclée","étoile","--"],
            ["--","--","sablier","--","--"],
            ["--","--","--","plus","--"],
            ["--","--","--","--","--"],
            ["--","--","--","--","--"]
            ]
            
        self.moveLog=[]
            
        
"""        
class Move():
    def __init__(self, startSq, endSq, board):
  
        
  """