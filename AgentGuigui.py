
class Agent():
    """
    The Subject owns some important state and notifies observers when the state
    changes.
    """

    _state = None
    """
    For the sake of simplicity, the Subject's state, essential to all
    subscribers, is stored in this variable.
    """

    _observers = []
    """
    List of subscribers. In real life, the list of subscribers can be stored
    more comprehensively (categorized by event type, etc.).
    """

    def attach(self, observer) -> None:
        print("Subject: Attached an observer.")
        self._observers.append(observer)

    def detach(self, observer) -> None:
        self._observers.remove(observer)


    def notify(self) -> None:
        """
        Trigger an update in each subscriber.
        """

        print("Subject: Notifying observers...")
        for observer in self._observers:
            observer.update(self)

    def some_business_logic(self) -> None:
        """
        Usually, the subscription logic is only a fraction of what a Subject can
        really do. Subjects commonly hold some important business logic, that
        triggers a notification method whenever something important is about to
        happen (or after it).
        """

        print("\nSubject: I'm doing something important.")

        print(f"Subject: My state has just changed to: {self._state}")
        self.notify()

class Observer():
    """
    The Observer interface declares the update method, used by subjects.
    """

    def update(self, subject) -> None:
        """
        Receive update from subject.
        """
        pass


"""Les deux classes concreteObserver sont des observer qui réagissent à des actions particulières d'un agent
VOIR quels sont les états que l'on peut avoir pour nos agents
Un état peut correspondre à la position de chaque pion"""
class ConcreteObserverA(Observer):
    def update(self, subject) -> None:
        if subject._state < 3:
            print("ConcreteObserverA: Reacted to the event")



class ConcreteObserverB(Observer):
    def update(self, subject) -> None:
        if subject._state == 0 or subject._state >= 2:
            print("ConcreteObserverB: Reacted to the event")