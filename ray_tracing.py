import pygame, sys, random, math
import random

class Wall():

    def __init__(self,a,b):
        self.a = pygame.math.Vector2(a)
        self.b = pygame.math.Vector2(b)
    
    def draw(self):
        pygame.draw.line(screen, pygame.Color('White'), self.a,self.b, 5)

'''class Map_generator():
    areas = random.randint(2, 6)
    x=[0]
    y=[0]
    x_ = 0
    for area in range(0, areas, 2):
        x_ = random.randrange(x_, w, 100)
        x.append(x_)'''

class Light():

    def __init__(self , walls ):
        self.pos = pygame.math.Vector2(w/2, h/2)
        self.rays = []
    
    def check_intersection(self, walls):

        for ray in self.rays:
            min_dist = 999999
            closest = None
            for wall in walls:
                point = ray.cast(wall)
                if point:
                    dist = pygame.math.Vector2.distance_to(self.pos, point)
                    if(dist < min_dist):
                        min_dist = dist
                        closest = point
            if(closest):
                pygame.draw.circle(screen,pygame.Color('Red'),(closest.x, closest.y),5,0)
                pygame.draw.line(screen, pygame.Color('White'), self.pos , (closest.x, closest.y))
    
    def controller(self, x, y):
        self.pos.x = x
        self.pos.y = y
        self.rays = []
        for wall in walls:
            self.rays.append(Ray(self.pos, wall.a))
            self.rays.append(Ray(self.pos, wall.b))
        
    def draw(self):
        for ray in self.rays:
            ray.draw()
    
class Ray():

    def __init__(self,position,direction):
        self.position = position
        self.direction  = direction
        
    def draw(self):
        pygame.draw.line(screen, pygame.Color('White'), self.position , (self.position.x + 10 * self.direction.x, self.position.y + 10 * self.direction.y))
        
    def cast(self, wall):
        x1 = wall.a.x
        y1 = wall.a.y
        x2 = wall.b.x
        y2 = wall.b.y
        
        x3 = self.position.x
        y3 = self.position.y
        x4 = self.direction.x
        y4 = self.direction.y
        
        # Line–line intersection https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection

        d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if d==0:
            return
        
        t = ( (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4) ) / d
        u = - ( (x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3) ) / d
        
        if (t >= 0 and t <= 1 and u > 0):
            ptx = x1 + t * (x2 -x1)
            pty = y1 + t * (y2 -y1)
            point  = pygame.math.Vector2(ptx, pty)
            return point
        else: return
    
pygame.init()
monitor_size = [1280,720]
screen = pygame.display.set_mode(monitor_size)
pygame.display.set_caption('Ray Tracing')
clock = pygame.time.Clock()
w,h = pygame.display.get_surface().get_size()
walls = []
walls.append(Wall((0,0),(0,h)))
walls.append(Wall((0,0),(w,0)))
walls.append(Wall((0,h),(w,h)))
walls.append(Wall((w,h),(w,0)))
for i in range(3):
    walls.append(Wall((random.randint(0, w),random.randint(0, h)),  (random.randint(0, w),random.randint(0, h)) ))

light = Light(walls)

def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
        screen.fill((11,14,15))
        for wall in walls:
            wall.draw()
        mouse_position = pygame.mouse.get_pos()
        light.controller(mouse_position[0], mouse_position[1])
        light.check_intersection(walls)
        pygame.display.update()
        clock.tick(120)
        

if __name__ == "__main__":
    main()
