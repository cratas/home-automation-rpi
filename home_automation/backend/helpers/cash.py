from pickle import FALSE
import threading
import time
# --------------
# SINGLETON Class with cash memory impemented as ring buffer
# --------------
class Cash:
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
        if Cash.__instance == None:
            Cash()
        return Cash.__instance            

    def __init__(self):
        if Cash.__instance != None:
            raise Exception("This class is singleton")
        else:
            Cash.__instance = Cash

    # static method for adding new object into cash
    @staticmethod
    def add(item):
        # if capacity is 1, cash is turned off
        if Cash.capacity == 1:
            item.device_values.save()
            item.save()
            return None
        # else circle buffer cashing works 
        else:
            # if capacity is reached, print warning and return
            if Cash.size == Cash.capacity:
                print("Queue is full")
                return 
            else:
                # add new item into cash and move tail pointer
                Cash.tail = (Cash.tail + 1) % Cash.capacity
                Cash.queue[Cash.tail] = item
                Cash.size = Cash.size + 1

                # if capacity of cash memory is 50% occupied, save into database in created thread
                if Cash.size > round(Cash.capacity / 2) and Cash.saving_thread_run is False:
                    t = threading.Thread(target=Cash.save_cash(), daemon=True)
                    t.start()
            
        # Cash.display()

    # static method for saving all objects from cash memory
    @staticmethod
    def save_cash():
        Cash.saving_thread_run = True
        [ Cash.remove() for _ in range(Cash.size) ]
        Cash.saving_thread_run = False

    # static method for removing object from cash and write data into database
    @staticmethod
    def remove():
        if Cash.size == 0:
            print("Queue is empty")
            return
        else:
            # get object from queue
            cash_object = Cash.queue[Cash.head]
            # save into database
            cash_object.device_values.save()
            cash_object.save()
            # set objects place in queue for None
            Cash.queue[Cash.head] = None
            # change head pointer
            Cash.head = (Cash.head + 1) % Cash.capacity

        # decrement cash size
        Cash.size = Cash.size - 1
        return cash_object

    # printing actual cash status static method
    @staticmethod
    def display():
        if Cash.size == 0:
            print("Queue is empty")
        else:
            print("------")
            print(Cash.queue)
            print(Cash.size)
