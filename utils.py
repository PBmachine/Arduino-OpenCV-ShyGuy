#my utils

import time
class timer(object):
    def __init__(self,delay,scale=1000):
        #timer class with a delay (seconds) and scale factor (default is 1/1000)
        #defaults to 
        self.scale = scale  
        self.timer = round(time.monotonic()*scale)
        self.init_time =self.timer
        self.delay = delay*self.scale
    
    
    def elapsed(self, reset = True):
        curr_time = self.curr_time()
        if (curr_time -self.timer>self.delay):
            if reset:
                self.timer = curr_time
            return True
        else:
            return False
        
    def curr_time(self):
        return round(time.monotonic()*self.scale)
        
    def reset(self):
        curr_time = self.curr_time()
        self.timer = curr_time

    def time_elapsed(self):
        curr_time = self.curr_time()
        return (curr_time-self.timer)
    
    def time_since_init(self):
        time_elapsed = self.curr_time()-self.init_time

        return (round(time_elapsed/self.scale,1))
    
    
    def time_remaining(self):
        elapsed = self.time_elapsed
        return (self.delay-elapsed)
    
def mapValue(value, leftMin, leftMax, rightMin, rightMax):
    # https://stackoverflow.com/questions/1969240/mapping-a-range-of-values-to-another
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def checkData(item,check_list):
    good = False
    if len(check_list)<2:
        check_list.insert(item,0)
        return
    if checkLen(item,check_list):
        check_list.insert(item,0)
        good = True


    if len(check_list)>numcheck:
         check_list.pop()

    if good:
        return item
    else:
        return check_list[0]
    
numcheck = 20
def checkAvgLen(list,check_list):
    item = len(list)
    good = False
    avg = 0
    for element in check_list:
        avg += element
    avg = round(avg/(len(check_list)+0.00001),1)
    check_list.insert(0,item)

    if (len(check_list)>=numcheck):
        check_list.pop()

    if (abs(item-avg)<1):
        return item
    else:
        return avg


def checkLen(item,check_list):
    avg = 0

    check_item = len(item)
    for element in check_list:
        avg += len(element)
    avg /= len(check_list)
    if (abs(check_item-avg)<.5):
        return True
    else:
        return False