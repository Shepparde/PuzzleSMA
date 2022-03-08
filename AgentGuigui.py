
"""
Created on Mon Feb 21 11:01:24 2022

@author: guillaume.orset-prelet
"""
from threading import Thread,Semaphore
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
    
        self._state = True
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
    def _sendMessage(self,x_new,y_new,x_final,y_final):
        self._observers[0].receiveMessage(x_new,y_new,x_final,y_final)
        
        
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
        print("Pawn: " +str(id(self))[-4:]+" I have changed my position from: ({},{}) to ({},{})".format(self.x,self.y,x_new,y_new))

        if (self.x_final == x_new)&(self.y_final == y_new):
            print("Final Point Reached")
            self._state = False
            for subject in self._observers[0].subjects:
                print("in the loop")
                if subject.hasMovedFromFinalPoint==1:
                    subject.run()
                    print("cannot move")


        
    def run(self):
        while self._state:
            time.sleep(0.5)
            bestChoices = self._getBestPositions()
            hasMoved=0
            best = random.choice(bestChoices)
            #Check if the position is still available
            availability =self._observers[0].get_position(best[0],best[1])
            if availability==0:
                self.move(best[0],best[1])
                hasMoved=1
                self._observers[0].semaphore.release()
            else:
                print("Position Finally not available")
                self._observers[0].semaphore.release()
            if (len(bestChoices)==1)&(hasMoved==0):
                print("Message sent")
                choice = random.choice(bestChoices)
                self._sendMessage(choice[0],choice[1],self.x_final,self.y_final)

            


class Observer():
    """
    The Observer declares the update method, used by subjects.
    """
    def __init__(self, subjects,n_rows,n_cols) -> None:

        self.n_rows = n_rows
        self.n_cols = n_cols
        self.subjects=subjects
        self.positions = {}
        self.semaphore = Semaphore(1)

        self.board=[["--" for j in range(n_cols)] for i in range(n_rows)]
        #create board positions and availability
        for row in range(n_rows):
            for col in range(n_cols):
                 self.positions[(row,col)] = 0
        for subject in  self.subjects:
            subject.attach(self)
            self._set_position(subject._symbol,subject.x,subject.y,subject.x_prev,subject.y_prev)
    def receiveMessage(self,x_new,y_new,x_final,y_final):
        for subject in self.subjects:
            if (subject.x_final==x_new)&(subject.y_final==y_new):
                print("message received")
                subject._state = True
                worstChoices = subject._getWorstPositions(x_final,y_final)
                hasMoved=0
                for worst in worstChoices:
                    if self.get_position(worst[0],worst[1])==0:
                        subject.move(worst[0],worst[1])
                        subject.hasMovedFromFinalPoint=1
                        hasMoved=1
                        print("moves from path of another Pawn")
                        break
                if hasMoved==0:
                    print("has to move from path of another Pawn but none available position")
                break
        for subject in self.subjects:
            if (subject.x_final==x_final)&(subject.y_final==y_final):
                subject.move(x_new,y_new)
                time.sleep(2)
        self.semaphore.release()
            
    def get_position(self,x,y) -> int:
        self.semaphore.acquire()
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
