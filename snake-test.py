import pygame
import random
pygame.init()
pygame.font.init() 
score_font = pygame.font.SysFont("Arial", 25)
clock = pygame.time.Clock()
screen = pygame.display.set_mode([500, 500])
score=0
moves = {"left" : (-1,0),
        "right":(1,0),
        "up" : (0,-1),
        "down": (0,1)}
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
    
dirx=1
diry=0
sn=[snake(6,6),snake(5,6),snake(4,6),snake(3,6)]            
running = True
apple=food()
move_timer=0
move_delay=150

while running:
    dt=clock.tick(60)
    move_timer+= dt
    for event in pygame.event.get():
        # Check if the user clicked the 'X' to close
        if event.type == pygame.QUIT:
            running = False
        
        # Check if a key was pressed down
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z and direction !="down":    # Z (Up)
                direction = "up"
            elif event.key == pygame.K_s and direction !="up":  # S (Down)
                direction = "down"
            elif event.key == pygame.K_q and direction !="right":  # Q (Left)
                dirx+=1
                diry+=1
            elif event.key == pygame.K_d and direction !="left":  # D (Right)
                direction = "right" 

    screen.fill((0, 0, 0))
    
    for r in range(12):
        for c in range(12):
            x = 20 + c * 30
            y = 20 + r * 30
            pygame.draw.rect(screen, (0, 0, 255), (x, y, 30, 30), 1)
    
    center_x = 20 + (apple.x * 30) + 15
    center_y = 20 + (apple.y * 30) + 15
    pygame.draw.circle(screen, (0, 255, 0), (center_x, center_y), 13)  
    for segment in sn:
        center_x = 20 + (segment.x * 30) + 15
        center_y = 20 + (segment.y * 30) + 15

        pygame.draw.circle(screen, (255, 0, 0), (center_x, center_y), 13)

    pygame.display.flip()
    if score >= 1000 - 50 :
        running =False
    if move_timer>=move_delay :
        move_timer=0
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
    pygame.display.flip()

if score > 960 :
    text_surface = score_font.render("SUCCESS", True, (255, 200, 255))
    screen.blit(text_surface, (20, 460))
pygame.quit()
print(score)
score =0