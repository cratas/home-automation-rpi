from pickle import FALSE
import threading
# --------------
# SINGLETON Class with cash memory impemented as ring buffer
# --------------
class Cache:
    __instance = None
    capacity = 1            # THERE IS POSSIBLE TO CHANGE CASH SIZE (SHOULD BE EVEN)
    queue = [None] * capacity
    tail = -1
    head = 0
    size = 0
    saving_thread_run = False

    # static method for getting instance of Cash
    @staticmethod 
    def get_instance():
        if Cache.__instance == None:
            Cache()
        return Cache.__instance            

    def __init__(self):
        if Cache.__instance != None:
            raise Exception("Cache class is singleton")
        else:
            Cache.__instance = self

    #  method for adding new object into cash
    def add(self,item):
        # if capacity is 1, cash is turned off
        if self.capacity == 1:
            item.device_values.save()
            item.save()
            return None
        # else circle buffer cashing works 
        else:
            # if capacity is reached, print warning and return
            if self.size == self.capacity:
                print("Queue is full")
                return 

            # add new item into cash and move tail pointer
            self.tail = (self.tail + 1) % self.capacity
            self.queue[self.tail] = item
            self.size = self.size + 1

            # if capacity of cash memory is 50% occupied, save into database in created thread
            if self.size > round(self.capacity / 2) and self.saving_thread_run is False:
                t = threading.Thread(target=self.save_cash(), daemon=True)
                t.start()
            
        # Cash.display()

    #  method for saving all objects from cash memory
    def save_cash(self):
        self.saving_thread_run = True
        [ self.remove() for _ in range(self.size) ]
        self.saving_thread_run = False

    #  method for removing object from cash and write data into database
    def remove(self):
        if self.size == 0:
            print("Queue is empty")
            return
        else:
            # get object from queue
            cash_object = self.queue[self.head]
            # save into database
            cash_object.device_values.save()
            cash_object.save()
            # set objects place in queue for None
            self.queue[self.head] = None
            # change head pointer
            self.head = (self.head + 1) % self.capacity

        # decrement cash size
        self.size = self.size - 1
        return cash_object

    # printing actual cash status static method
    def display(self):
        if self.size == 0:
            print("Queue is empty")
        else:
            print("------")
            print(self.queue)
            print(self.size)
