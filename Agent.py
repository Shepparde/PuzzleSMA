# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 11:22:01 2022

@author: Administrator
"""
import random 
import SymbolGenerator
from threading import Thread
import time


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
    id_ = 1
    id_agent = id_
    symbol_agent = SymbolGenerator.getRandomSymbol()
    # ligne sur laquelle se trouve l'agent
    x = int()
    # colonne sur laquelle se trouve l'agent
    y = int()
    x_fin = int()
    y_fin = int()
    position = [x,y]
    position_init = [x,y]
    position_final = [x_fin, y_fin]
    
    #un agent est un thread qui observe et qui est observé
    #par les autres threads
    
    def __init__(self, x, y, x_fin, y_fin):
        print("Agent "+ id_agent +" was created.")
        Observer.__init__(self)
        Thread.__init__(self)
        self.x = x
        self.y = y
        self.x_fin = x_fin
        self.y_fin = y_fin

    
    def run(self):
        #self.position = 
        pass
    
    def start():
        if (Thread == null | Thread.is_alive == True) : 
            Thread.run()
            
    def stop() :
        ThreadBol.set(False)
        Thread.join(500)
        
    def agent_is_moving(self, where):
        print("Agent is moving to "+where)
        
            
    Thread.start()
    

#def ajouterAgent(agent: Agent)