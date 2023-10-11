"""
ShyGuy 
Object with finite state machine and parameters to express "shyness"
attaches to an output
"""
import time
import utils

class shyguy(object):
    def __init__(self):
        self.start_time = round(time.monotonic()*1000)
        self.last_motion = 0
        self.states = ["hiding","dancing","waiting"]
        self.state = "waiting"
        self.shyness_param()
        self.prev_state = "waiting"
        self.prev_motion = 0.2

    def shyness_param(self):
        self.motion_tol = 3 #tolerance for num of moving objects
        self.face_tol = 0 #tolerance for num of faces
        self.waitdelay = 5*1000
        self.hidedelay = 5*1000
        self.dancemax = 3*60*1000
        self.movement= 0.2 #percentage movement

    def set_face_tol(self,new_tol):
        self.face_tol = new_tol

    def set_motion_tol(self,new_tol):
        self.motion_tol = new_tol

    def hide(self,curr_time):
        #if environment is unsafe stop dancing and set motion timer
        self.state = "hiding"
        self.movement = 0
        self.last_motion = curr_time
        print("AH! I HIDE!")

    def hiding(self,curr_time):
        #while hiding no motion
        if (curr_time-self.last_motion>self.hidedelay):
            #if an amount of time has elapsed begin to wait
            self.state = "waiting"
            self.last_motion = curr_time
            self.movement = 0.05
            print("anyone there???")
        
    def waiting(self,curr_time,safe):
        #if environment is safe then either stay waiting or start dancing
        if safe:
            timer = curr_time-self.last_motion
            if (timer>self.waitdelay):
                self.state = "dancing"
                self.last_motion = curr_time
                print("TIME TO DANCE!")
                return
            else:
                time_percent = timer/self.waitdelay
                self.movement =  round(0.2*time_percent,2)
        else:
            self.last_motion = curr_time
        self.movement = 0.05 
        
  
    def dance(self,curr_time):
        time_dancing = curr_time-self.last_motion
        self.movement = round(utils.mapValue(time_dancing,0,self.dancemax,0.25,1),2)

    def update(self,n_faces,n_motion):
        #takes input of num faces or motion available and acts based on current state
        curr_time = round(time.monotonic()*1000)

        #FSM state update
        if (self.state =="dancing"):
            #dancing state
            #hide if motion or faces are detected
            if (n_faces>self.face_tol): self.hide(curr_time)
            elif (n_motion>self.motion_tol): self.hide(curr_time)
            #else keep dancing
            else:
                self.dance(curr_time)

        elif(self.state =="hiding"):
            #for hiding state stays motionless until timer elapses
            #regardless of motion or faces
            self.hiding(curr_time)
        
        elif(self.state == "waiting"):
            #in waiting state does small motions
            #when alone timer counts down and it begins to dance
            alone = False
            if (n_faces<=self.face_tol and n_motion<=self.motion_tol): 
                alone = True
            self.waiting(curr_time, alone)

        return (self.state,self.movement)
        










    

    
