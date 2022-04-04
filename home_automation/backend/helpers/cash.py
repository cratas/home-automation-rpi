
# --------------
# SINGLETON Class with cash memory impemented as ring buffer
# --------------
class Cash:
    __instance = None
    capacity = 1            #THERE IS POSSIBLE TO CHANGE CASH SIZE (SHOULD BE EVEN)
    queue = [None] * capacity
    tail = -1
    head = 0
    size = 0

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

    #static method for adding new object into cash
    @staticmethod
    def add(item):
        #if capacity is 1, cash is turned off
        if Cash.capacity == 1:
            item.device_values.save()
            item.save()
        #else circle buffer cashing works 
        else:
            #if capacity of cash memory is 50% occupied, save into database
            if Cash.size >= round(Cash.capacity / 2):
                [ Cash.remove() for _ in range(round(Cash.capacity / 2)) ]
            
            #add new item into cash and move tail pointer
            Cash.tail = (Cash.tail + 1) % Cash.capacity
            Cash.queue[Cash.tail] = item
            Cash.size = Cash.size + 1

    @staticmethod
    def remove():
        if Cash.size == 0:
            print("Queue is empty")
            return
        else:
            #get object from queue
            cash_object = Cash.queue[Cash.head]
            #save into database
            cash_object.device_values.save()
            cash_object.save()
            #set objects place in queue for None
            Cash.queue[Cash.head] = None
            #change head pointer
            Cash.head = (Cash.head + 1) % Cash.capacity

        #decrement cash size
        Cash.size = Cash.size - 1
        return cash_object

    @staticmethod
    def display():
        if Cash.size == 0:
            print("Queue is empty")
        else:
            print("------")
            print(Cash.queue)
            print(Cash.size)
