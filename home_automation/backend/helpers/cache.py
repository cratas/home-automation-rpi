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
            raise Exception("This class is singleton")
        else:
            Cache.__instance = Cache

    # static method for adding new object into cash
    @staticmethod
    def add(item):
        # if capacity is 1, cash is turned off
        if Cache.capacity == 1:
            item.device_values.save()
            item.save()
            return None
        # else circle buffer cashing works 
        else:
            # if capacity is reached, print warning and return
            if Cache.size == Cache.capacity:
                print("Queue is full")
                return 

            # add new item into cash and move tail pointer
            Cache.tail = (Cache.tail + 1) % Cache.capacity
            Cache.queue[Cache.tail] = item
            Cache.size = Cache.size + 1

            # if capacity of cash memory is 50% occupied, save into database in created thread
            if Cache.size > round(Cache.capacity / 2) and Cache.saving_thread_run is False:
                t = threading.Thread(target=Cache.save_cash(), daemon=True)
                t.start()
            
        # Cash.display()

    # static method for saving all objects from cash memory
    @staticmethod
    def save_cash():
        Cache.saving_thread_run = True
        [ Cache.remove() for _ in range(Cache.size) ]
        Cache.saving_thread_run = False

    # static method for removing object from cash and write data into database
    @staticmethod
    def remove():
        if Cache.size == 0:
            print("Queue is empty")
            return
        else:
            # get object from queue
            cash_object = Cache.queue[Cache.head]
            # save into database
            cash_object.device_values.save()
            cash_object.save()
            # set objects place in queue for None
            Cache.queue[Cache.head] = None
            # change head pointer
            Cache.head = (Cache.head + 1) % Cache.capacity

        # decrement cash size
        Cache.size = Cache.size - 1
        return cash_object

    # printing actual cash status static method
    @staticmethod
    def display():
        if Cache.size == 0:
            print("Queue is empty")
        else:
            print("------")
            print(Cache.queue)
            print(Cache.size)
