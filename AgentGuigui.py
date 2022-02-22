
"""
Created on Mon Feb 21 11:01:24 2022

@author: guillaume.orset-prelet
"""
from threading import Thread
import random
import time

class Agent(Thread):
    """
    The Subject owns some important state and notifies observers when their position
    changes.
    """
    def __init__(self,x,y,x_final,y_final,_symbol) -> None:
        
        self.x=x
        self.y=y
        self.x_prev = x
        self.y_prev = y
        self.x_final = x_final
        self.y_final = y_final
        self._symbol = _symbol
        print("Agent "+ str(id(self))[-4:] +" was created.")
        Thread.__init__(self)
    
        self._state = True
    """
    State : can be whether a pawn has reached the final point 
    """

    _observers = []
    """
    List of subscribers. 
    """

    def attach(self, observer) -> None:
        print("Pawn: "+str(id(self))[-4:] +" Attached an observer.")
        self._observers.append(observer)

    def detach(self, observer) -> None:
        self._observers.remove(observer)


    def notify(self) -> None:
        """
        Trigger an update in each subscriber.
        """

        for observer in self._observers:
            observer.update(self)

    def move(self,x_new,y_new) -> None:
        """
        function to move a pawn if a box is available and that the new and previous box are close (+/-1 x,y)
        """
        if self._observers[0].get_position(x_new,y_new) == 0:
            if (abs(x_new - self.x)+abs(y_new - self.y))<=1:
                print("Position Available")
                print("Pawn: " + str(id(self))[-4:]+" I have changed my position from: ({},{}) to ({},{})".format(self.x,self.y,x_new,y_new))
                self.x_prev = self.x
                self.y_prev = self.y
                self.x = x_new
                self.y = y_new
                self.notify()
                if (self.x_final == x_new)&(self.y_final == y_new):
                    self._state = False
            else:
                print("Pawn: " + str(id(self))[-4:]+" position ({},{}) to far from you".format(x_new,y_new))

        else:
            print("Pawn: " + str(id(self))[-4:]+" position ({},{}) not available".format(x_new,y_new))
            
    def run(self):
        while self._state:
            time.sleep(0.5)
            top_x = self._observers[0].n_rows - 1
            top_y = self._observers[0].n_cols - 1 
            
            #pawn is not on any edge
            if (0<self.x<top_x)&(0<self.y<top_y):
                self.move(random.randint(self.x-1,self.x+1),random.randint(self.y-1,self.y+1))
            #pawn is on a col edge but not on a row edge
            elif (0<self.x<top_x):
                if self.y==0:
                    self.move(random.randint(self.x-1,self.x+1),random.randint(self.y,self.y+1))
                else:
                    self.move(random.randint(self.x-1,self.x+1),random.randint(self.y-1,self.y))
            #pawn is on a row edge but not on a col edge
            elif (0<self.y<top_y):
                if self.x==0:
                    self.move(random.randint(self.x,self.x+1),random.randint(self.y-1,self.y+1))
                else:
                    self.move(random.randint(self.x-1,self.x),random.randint(self.y-1,self.y+1))
            #pawn is on a row edge AND not on a col edge
            else:
                #fix problem when x==0 and y==4
                if (self.x==0)&(self.y==0):
                    self.move(random.randint(self.x,self.x+1),random.randint(self.y,self.y+1))
                elif (self.x==0)&(self.y==top_y):
                    self.move(random.randint(self.x,self.x+1),random.randint(self.y-1,self.y))
                elif self.y==0:
                    self.move(random.randint(self.x-1,self.x),random.randint(self.y,self.y+1))
                else:
                    self.move(random.randint(self.x-1,self.x),random.randint(self.y-1,self.y))
class Observer():
    """
    The Observer declares the update method, used by subjects.
    """
    def __init__(self, subjects,n_rows,n_cols) -> None:

        self.n_rows = n_rows
        self.n_cols = n_cols
        self.positions = {}
        self.board=[["--" for j in range(n_cols)] for i in range(n_rows)]
        #create board positions and availability
        for row in range(n_rows):
            for col in range(n_cols):
                 self.positions[(row,col)] = 0
        for subject in subjects:
            subject.attach(self)
            self._set_position(subject._symbol,subject.x,subject.y,subject.x_prev,subject.y_prev)
        
            
    def get_position(self,x,y) -> int:
        return self.positions[(x,y)]
    def _set_position(self,symbol,x,y,x_prev,y_prev) -> None :
        

        #previous position of the pawn is set to 0
        self.positions[(x_prev,y_prev)] = 0
        self.board[x_prev][y_prev] = "--"
        #new position of the pawn is set to 1 because box (x,y) not available anymore
        self.positions[(x,y)] = 1
        self.board[x][y] = symbol
    def update(self, subject) -> None:
        self._set_position(subject._symbol,subject.x,subject.y,subject.x_prev,subject.y_prev)
