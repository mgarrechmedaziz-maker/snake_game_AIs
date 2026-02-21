import math
import random
import snakeAI 
moves = {"left" : (-1,0),
        "right":(1,0),
        "up" : (0,-1),
        "down": (0,1)}
n =20
class genome():
    def __init__(self,n,trie=1,movement=None):
        if movement ==None :
            self.movement=[ random.choice(["up","down","left","right"]) for _ in range(n)]
        else :
            self.movement=movement.copy()
            j=random.randint(0,n-1) #number of mutations
            for _ in range(j):
                k = random.randint(0,len(self.movement)-1)
                self.movement[k]=random.choice(["up","down","left","right"])
            if trie%8==7:
                while len(self.movement) <n:
                    self.movement.append(random.choice(["up","down","left","right"]))
        self.score=0
         
        
genomes=[genome(n) for _ in range(500)]
b_genome=genome(n) ; b_genome.score =0
for trie in range(1,500):
    random.seed(66)
    for i in range(500):
        genomes[i].score=snakeAI.snake_gm(genomes[i].movement,n)
        if genomes[i].score > b_genome.score : 
            b_genome = genomes[i]
    random.seed()
    if trie==20:
        print(b_genome.movement)
        print(n)
    if trie%8==0:
        n+=10
    genomes= [genome(n,trie,b_genome.movement) for _ in range(500)]
    random.seed(66)
    snakeAI.show(b_genome.movement,n)
    random.seed()
'''
n=5
testg=genome(n)
print(testg.movement)
testm1=genome(n,testg.movement)
print(testm1.movement)
testm2=genome(n,7,testm1.movement)
print(testm2.movement)
n+=10
testm3=genome(n,10,testm2.movement)
print(testm3.movement)'''
