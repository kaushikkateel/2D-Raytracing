import pygame, sys, random, math
import random

class Wall():

    def __init__(self,a,b):
        self.a = pygame.math.Vector2(a)
        self.b = pygame.math.Vector2(b)
    
    def draw(self):
        pygame.draw.line(screen, pygame.Color('White'), self.a,self.b)

class Light():

    def __init__(self):
        self.pos = pygame.math.Vector2(w/2, h/2)
        self.rays = []
        num_rays = 365
        for i in range(num_rays):
            angle = i * (2 * math.pi / num_rays)
            x = math.cos(angle)
            y = math.sin(angle)
            direction = pygame.math.Vector2(x, y)
            self.rays.append(Ray(self.pos, direction))
    
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
                pygame.draw.line(screen, pygame.Color('White'), self.pos , (closest.x, closest.y))
    
    def controller(self, x, y):
        self.pos.x = x 
        self.pos.y = y 
        
    def draw(self):
        for ray in self.rays:
            ray.draw()
    
class Ray():

    def __init__(self,position,direction):
        self.position = position
        self.direction  = direction
        
    def draw(self):
        pygame.draw.line(screen, pygame.Color('White'), self.position , (self.position.x + 10 * self.direction.x, self.position.y + 10 * self.direction.y))
    
    def setDir(self, x, y):
        self.direction.x = x - self.position.x
        self.direction.y = y - self.position.y
        self.direction = pygame.math.Vector2.normalize(self.direction)
        
    def cast(self, wall):
        x1 = wall.a.x
        y1 = wall.a.y
        x2 = wall.b.x
        y2 = wall.b.y
        
        x3 = self.position.x
        y3 = self.position.y
        x4 = self.position.x + self.direction.x
        y4 = self.position.y + self.direction.y
        
        # Line–line intersection https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
        
        d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if d==0:
            return
        
        t = ( (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4) ) / d
        u = - ( (x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3) ) / d
        
        if (t >0 and t < 1 and u > 0):
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
for i in range(5):
    walls.append(Wall((random.randint(0, w),random.randint(0, h)),  (random.randint(0, w),random.randint(0, h)) ))
#wall = Wall((600,300),(900, 400))
#ray = Ray(100,400)
light = Light()

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
        #light.draw()
        pygame.display.update()
        clock.tick(120)
        

if __name__ == "__main__":
    main()