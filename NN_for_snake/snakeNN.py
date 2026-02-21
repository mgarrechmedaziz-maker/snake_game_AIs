import math
import random
import neural_network as nn
class snake():
        def __init__(self,x,y):
            self.x=x
            self.y=y
        def __eq__(self,other):
            return self.x==other.x and self.y==other.y
        def __add__(self,other : tuple):
            return snake(self.x+other[0],self.y+other[1])
        def __repr__(self):
            return f"snake: {self.x} , {self.y}"

def snake_gm(T): #T is the array of rotations in the form : ["0","-1","1","1",...]
    nn.MLP(9,[12,3])
    score=0
    moves = {"left" : (-1,0),
        "right":(1,0),
        "up" : (0,-1),
        "down": (0,1)}
    directions=["right","up","left","down"]
  
    dirIndex=0
    sn=[snake(6,6),snake(5,6),snake(4,6),snake(3,6)]            
    running = True
    class food():
        def __init__(self):
            self.x = 0
            self.y = 0
            self.spawn() # Spawn immediately when created

        def spawn(self):
        # 1. Assume the spot is dirty (invalid) to start the loop
            valid_spot = False
        
        # 2. Keep rolling UNTIL we find a clean spot
            while not valid_spot:
                self.x = random.randint(0, 11)
                self.y = random.randint(0, 11)

                # 3. innocent until proven guilty
                valid_spot = True 

                # 4. Check against every snake part
                for body in sn:
                    # Compare coordinates, not objects!
                    if body.x == self.x and body.y == self.y:
                        valid_spot = False # Found a collision!
                        break # Stop checking, go back to the top and reroll
                        
    apple=food()
    for i in range(len(T)-1):
        dirIndex+=T[i]
        direction=directions[(dirIndex)%4]
        print(direction)
        if score >= 1000 - 50 :
            break
        sn.insert (0,sn[0] + moves[direction])
        if sn[0].x == -1 :
            sn[0].x = 11
        elif sn[0].x ==12:
            sn[0].x =0
        if sn[0].y == -1 :
            sn[0].y = 11
        elif sn[0].y ==12:
            sn[0].y =0
        if sn[0] == apple :
            score+=10
            apple.spawn()
        else:
            sn.pop()   
        if sn[0] in sn[1:]:
            running = False
                 
    score += math.sqrt((sn[0].x-apple.x)**2+(sn[0].y-apple.y)**2)
    return score
def think (appx,appy,dir,p1,p2,p3,p4,p5,p6,p7,p8):
    pass