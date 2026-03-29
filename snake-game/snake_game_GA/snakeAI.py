
import random
import math
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

def snake_gm(T,n): #T is the array of movements in the form : ["0","up","3","left",...]
    score=0
    moves = {"left" : (-1,0),
        "right":(1,0),
        "up" : (0,-1),
        "down": (0,1)}

  
    direction=(1,0)
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
        if T[i]==1 and direction !="down":    # Z (Up)
            direction = "up"
        elif T[i]=="down" and direction !="up":  # S (Down)
            direction = "down"
        elif T[i]=="left" and direction !="right":  # Q (Left)
            direction = "left"
        elif T[i]=="right" and direction !="left":  # D (Right)
            direction = "right" 
            
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

#__________________________________________________________

move_delay=150
def show(T, n):
    import pygame
    import random

    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()
    score_font = pygame.font.SysFont("Arial", 25)

    moves = {
        "left": (-1, 0),
        "right": (1, 0),
        "up": (0, -1),
        "down": (0, 1)
    }

    direction = "right"
    sn = [snake(6,6), snake(5,6), snake(4,6), snake(3,6)]
    score = 0
    running = True

    class food:
        def __init__(self):
            self.spawn()

        def spawn(self):
            while True:
                self.x = random.randint(0, 11)
                self.y = random.randint(0, 11)
                if all(b.x != self.x or b.y != self.y for b in sn):
                    break

    apple = food()

    move_delay = 50
    move_timer = 0
    i = 0  # genome index

    while running:
        dt = clock.tick(60)
        move_timer += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        if move_timer >= move_delay and i < len(T):
            move_timer = 0

            # apply genome move
            if T[i] in moves:
                if not (
                    (T[i] == "up" and direction == "down") or
                    (T[i] == "down" and direction == "up") or
                    (T[i] == "left" and direction == "right") or
                    (T[i] == "right" and direction == "left")
                ):
                    direction = T[i]

            i += 1

            # move snake
            sn.insert(0, sn[0] + moves[direction])

            # wrap
            sn[0].x %= 12
            sn[0].y %= 12

            if sn[0].x == apple.x and sn[0].y == apple.y:
                score += 10
                apple.spawn()
            else:
                sn.pop()

            if sn[0] in sn[1:]:
                running = False

        # draw
        screen.fill((0, 0, 0))

        for r in range(12):
            for c in range(12):
                pygame.draw.rect(
                    screen,
                    (0, 0, 255),
                    (20 + c*30, 20 + r*30, 30, 30),
                    1
                )

        pygame.draw.circle(
            screen,
            (0, 255, 0),
            (20 + apple.x*30 + 15, 20 + apple.y*30 + 15),
            13
        )

        for s in sn:
            pygame.draw.circle(
                screen,
                (255, 0, 0),
                (20 + s.x*30 + 15, 20 + s.y*30 + 15),
                13
            )

        score_text = score_font.render(f"Score: {score}", True, (255,255,255))
        screen.blit(score_text, (10, 460))

        pygame.display.flip()


