
"""
Created on Mon Feb 21 11:01:24 2022

@author: guillaume.orset-prelet
"""
from threading import Thread
import random
import time
from queue import Queue
import threading
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
    
        self.hasMovedFromFinalPoint = 0
    """
    State : can be whether a pawn has reached the final point 
    """

    _observers = []
    """
    List of subscribers. 
    """
    """function to get the distance from new point and final point 
    return 1 if new point is closer than current point to the final point
    else 0"""
    def _get_distance(self,x_new,y_new,x_target,y_target) -> int:
        currentDistance = abs(x_target - self.x)+abs(y_target - self.y)
        potentialDistance = abs(x_target - x_new)+abs(y_target - y_new)
        if potentialDistance <currentDistance:
            return 1
        else:
            return 0
        
    """Function to send a message to the observer to ask him to make other pawn moving from its path"""
    def _sendMessage(self,from_subject,to_subject):
        #print("Agent "+ str(id(self))[-4:] + " message sent")
        to_subject.receiveMessage(from_subject)
        
    def receiveMessage(self,from_subject) -> int:

        #print("Agent "+ str(id(self))[-4:] + " message received")
        worstChoices = self._getWorstPositions(from_subject.x_final,from_subject.y_final)
        worst=random.choice(worstChoices)
        hasMoved=0
        if self._observers[0].get_position(worst[0],worst[1])==0:
            self.move(worst[0],worst[1])
            hasMoved=1
            print("moves from path of another Pawn from ",self.x_prev," ",self.y_prev," to ",self.x," ",self.y )
            return 1
        if hasMoved==0:
            print("Ask again to see if the pawn can move")
            return 0


    def _getBestPositions(self) -> list:
        bestPositions = []

        if (self.x<self.top_x):
            if self._get_distance(self.x+1,self.y,self.x_final,self.y_final)==1:
                bestPositions.append((self.x+1,self.y))
        if (self.x>0):
            if self._get_distance(self.x-1,self.y,self.x_final,self.y_final)==1:
                bestPositions.append((self.x-1,self.y))
        if (self.y<self.top_y):
            if self._get_distance(self.x,self.y+1,self.x_final,self.y_final)==1:
                bestPositions.append((self.x,self.y+1))
        if (self.y>0):
            if self._get_distance(self.x,self.y-1,self.x_final,self.y_final)==1:
                bestPositions.append((self.x,self.y-1))
        if len(bestPositions)==0:
            print("vide avec coord ",self.x," ",self.y)
        return bestPositions

            
    def _getWorstPositions(self,x_final_other_pawn,y_final_other_pawn) -> list:
        worstPositions = []

        if (self.x<self.top_x):
            if self._get_distance(self.x+1,self.y,x_final_other_pawn,y_final_other_pawn)==0:
                worstPositions.append((self.x+1,self.y))
        if (self.x>0):
            if self._get_distance(self.x-1,self.y,x_final_other_pawn,y_final_other_pawn)==0:
                worstPositions.append((self.x-1,self.y))
        if (self.y<self.top_y):
            if self._get_distance(self.x,self.y+1,x_final_other_pawn,y_final_other_pawn)==0:
                worstPositions.append((self.x,self.y+1))
        if (self.y>0):
            if self._get_distance(self.x,self.y-1,x_final_other_pawn,y_final_other_pawn)==0:
                worstPositions.append((self.x,self.y-1))

        return worstPositions
    
    def attach(self, observer) -> None:
        print("Pawn: "+str(id(self))[-4:] +" Attached an observer.")
        self._observers.append(observer)
        self.top_x = self._observers[0].n_rows - 1
        self.top_y = self._observers[0].n_cols - 1 

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
        self.x_prev = self.x
        self.y_prev = self.y
        self.x = x_new
        self.y = y_new
        self.notify()
        print("Pawn: " +str(id(self))[-4:]+" I have changed my position from: ({},{}) to ({},{})".format(self.x_prev,self.y_prev,x_new,y_new))

        
    def run(self):
        while self._observers[0].global_state:
            time.sleep(random.randint(1,4))
            if (self.x,self.y)!=(self.x_final,self.y_final):

                bestChoices = self._getBestPositions()
                best = random.choice(bestChoices)
                #Check if the position is still available
                availability =self._observers[0].get_position(best[0],best[1])
                if availability==0:
                    self.move(best[0],best[1])
                else:
                    #print("Position Finally not available")
                    for subject in self._observers[0].subjects:
                        if (subject.x_final==best[0])&(subject.y_final==best[1]):
                            message = self._sendMessage(self,subject)
                            if message==1:
                                self.move(best[0],best[1])
                            else:
                                print("this pawn cannot move from his final position for now")
                            break
                        else:
                            pass
                   
            else:
                if self._observers[0].board==self._observers[0].final_board:
                    print("Final Global State Reached")
                    self._observers[0].global_state = False
                     
            


class Observer():
    """
    The Observer declares the update method, used by subjects.
    """
    def __init__(self, subjects,n_rows,n_cols) -> None:

        self.n_rows = n_rows
        self.n_cols = n_cols
        self.subjects=subjects
        self.positions = {}
        self.global_state = True
        self.board=[["--" for j in range(n_cols)] for i in range(n_rows)]
        self.final_board=[["--" for j in range(n_cols)] for i in range(n_rows)]

        #create board positions and availability
        for row in range(n_rows):
            for col in range(n_cols):
                 self.positions[(row,col)] = 0
        for subject in  self.subjects:
            subject.attach(self)
            self._set_position(subject._symbol,subject.x,subject.y,subject.x_prev,subject.y_prev)
            self._set_final_positions(subject)
        print(self.final_board)

    def get_position(self,x,y) -> int:

        return self.positions[(x,y)]
       
    def _set_position(self,symbol,x,y,x_prev,y_prev) -> None :
        
        #previous position of the pawn is set to 0
        self.positions[(x_prev,y_prev)] = 0
        self.board[x_prev][y_prev] = "--"
        #new position of the pawn is set to 1 because box (x,y) not available anymore
        self.positions[(x,y)] = 1
        self.board[x][y] = symbol
        
    #set_position for final board
    def _set_final_positions(self,subject) -> None :
        self.final_board[subject.x_final][subject.y_final] = subject._symbol
        
    def update(self, subject) -> None:
        self._set_position(subject._symbol,subject.x,subject.y,subject.x_prev,subject.y_prev)
