# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 11:22:01 2022

@author: Administrator
"""
import random 
import SymbolGenerator
from threading import Thread
import time
import Board

class Observer():
    _observers = []
    def __init__(self):
        #Creation d'une liste d'observers
        self._observers.append(self)
        self._observables = {}
        
    def observe(self, event_name, callback):
        self._observables[event_name] = callback
        
    def notify(self, modifier = None):
        # Notification des observers
        for observer in self._observers:
            observer.update(self)
            
    def attach(self, observer):
        # si l'observer n'est pas dans la 
        # liste d'observers, on le rajoute à la liste
        if observer not in self._oberservers : 
            self._observers.append(observer)
                
    def detach(self, observer):
        # supprimer l'observer de la liste
        try : 
            self._observers.remove(observer)
        except ValueError : 
            pass

# Event quand l'agent se déplace
class Event():
    def __init__(self, name, data, autofire = True):
        self.name = name
        self.data = data
        if autofire:
            self.fire()
    def fire(self):
        for observer in Observer._observers:
            if self.name in observer._observables:
                observer._observables[self.name](self.data)  

class Agent(Observer, Thread) :

    def __init__(self, _grid, _id, _symbol, x_init, y_init, x, y, x_fin, y_fin):
        self._grid = _grid
        self._id = _id
        self._symbol = _symbol
        self.x_init = x_init
        self.y_init = y_init
        self.x = x
        self.y = y
        self.x_fin = x_fin
        self.y_fin = y_fin
        print("Agent "+ _id +" was created.")
        Observer.__init__(self)
        Thread.__init__(self)
    
    def start():
        Thread.start()
            
    def stop() :
        Thread.terminate()
        
    def agent_is_moving(self, where):
        print("Agent is moving to "+where)
        
    def run():
        if Thread.is_alive == True : 
            Thread.run()
    
    Thread.start()
    

#def ajouterAgent(agent: Agent)