import pygame, sys, random, math
import random

class Wall():

    def __init__(self,a,b):
        self.a = pygame.math.Vector2(a)
        self.b = pygame.math.Vector2(b)
    
    def draw(self):
        pygame.draw.line(screen, pygame.Color((247, 252, 245)), self.a,self.b, 2)

'''class Map_generator():
    areas = random.randint(2, 6)
    x=[0]
    y=[0]
    x_ = 0
    for area in range(0, areas, 2):
        x_ = random.randrange(x_, w, 100)
        x.append(x_)'''

def map():
    vertices=[]
    map_walls=[]
    for _ in range(0, random.randint(4, 8)):
        x = random.randrange(0, w/2,10)
        y = random.randrange(0, h/2,10)
        vertices.append((x,y))
    vertices = sorted(vertices, key=lambda v: math.atan2(v[1]-h *1/4 , v[0]-w * 1/4))
    for i in range(0, len(vertices)):
        if(i!=len(vertices)-1):
            map_walls.append(Wall(vertices[i], vertices[i+1]))
        else: map_walls.append(Wall(vertices[i], vertices[0]))
    vertices=[]
    for _ in range(0, random.randint(4, 8)):
        x = random.randrange(w/2, w,10)
        y = random.randrange(0, h/2,10)
        vertices.append((x,y))
    vertices = sorted(vertices, key=lambda v: math.atan2(v[1]-h *1/4 , v[0]-w * 3/4))
    for i in range(0, len(vertices)):
        if(i!=len(vertices)-1):
            map_walls.append(Wall(vertices[i], vertices[i+1]))
        else: map_walls.append(Wall(vertices[i], vertices[0]))
    vertices=[]    
    for _ in range(0, random.randint(4, 8)):
        x = random.randrange(0, w/2,10)
        y = random.randrange(h/2, h,10)
        vertices.append((x,y))
    vertices = sorted(vertices, key=lambda v: math.atan2(v[1]-h *3/4 , v[0]-w * 1/4))
    for i in range(0, len(vertices)):
        if(i!=len(vertices)-1):
            map_walls.append(Wall(vertices[i], vertices[i+1]))
        else: map_walls.append(Wall(vertices[i], vertices[0]))
    vertices=[]
    for _ in range(0, random.randint(4, 8)):
        x = random.randrange(w/2, w,10)
        y = random.randrange(h/2, h,10)
        vertices.append((x,y))
    vertices = sorted(vertices, key=lambda v: math.atan2(v[1]-h *3/4 , v[0]-w * 3/4))
    for i in range(0, len(vertices)):
        if(i!=len(vertices)-1):
            map_walls.append(Wall(vertices[i], vertices[i+1]))
        else: map_walls.append(Wall(vertices[i], vertices[0]))
    vertices=[]
    return map_walls
    
class Light():

    def __init__(self , walls ):
        self.pos = pygame.math.Vector2(w/2, h/2)
        self.rays = []
        self.light_points =[]
    
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
                self.light_points.append(closest)
                #pygame.draw.line(screen, pygame.Color((227, 30, 5)), self.pos , (closest.x, closest.y))
                #pygame.draw.circle(screen,pygame.Color((242, 133, 119)),(closest.x, closest.y),5,0)
    
    def controller(self, x, y):
        self.pos.x = x
        self.pos.y = y
        self.rays = []
        self.light_points = []
        for wall in walls:
            self.rays.append(Ray(self.pos, wall.a))
            self.rays.append(Ray(self.pos, wall.b))

            #2 extra rays for each wall edge with offset of +- 0.001. this is to hit the boundary
            #find the distance using (wall.a.x - self.pos.x) i.e radius and multiply this with angle
            #add the calulated radius to the self.pos to adjust the position of the calulated radius wrt self.pos
            dist_a = pygame.math.Vector2.distance_to(self.pos, wall.a)
            dist_b = pygame.math.Vector2.distance_to(self.pos, wall.b)
            self.rays.append(Ray(self.pos, pygame.math.Vector2((self.pos.x + ( dist_a * math.cos( math.atan2(wall.a.y-self.pos.y, wall.a.x-self.pos.x) + 0.001))),  (self.pos.y + (dist_a * math.sin(math.atan2(wall.a.y-self.pos.y, wall.a.x-self.pos.x) + 0.001))))))
            self.rays.append(Ray(self.pos, pygame.math.Vector2((self.pos.x + ( dist_b * math.cos( math.atan2(wall.b.y-self.pos.y, wall.b.x-self.pos.x) + 0.001))),  (self.pos.y + (dist_b * math.sin(math.atan2(wall.b.y-self.pos.y, wall.b.x-self.pos.x) + 0.001))))))
            self.rays.append(Ray(self.pos, pygame.math.Vector2((self.pos.x + ( dist_a * math.cos( math.atan2(wall.a.y-self.pos.y, wall.a.x-self.pos.x) - 0.001))),  (self.pos.y + (dist_a * math.sin(math.atan2(wall.a.y-self.pos.y, wall.a.x-self.pos.x) - 0.001))))))
            self.rays.append(Ray(self.pos, pygame.math.Vector2((self.pos.x + ( dist_b * math.cos( math.atan2(wall.b.y-self.pos.y, wall.b.x-self.pos.x) - 0.001))),  (self.pos.y + (dist_b * math.sin(math.atan2(wall.b.y-self.pos.y, wall.b.x-self.pos.x) - 0.001))))))

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
boundary = []

#draw boundary
boundary.append(Wall((0,0),(0,h+0)))
boundary.append(Wall((0,0),(w+0,0)))
boundary.append(Wall((0,h+0),(w+0,h+0)))
boundary.append(Wall((w+0,h+0),(w+0,0)))

walls+=boundary
walls+= map()

'''for i in range(1):
    walls.append(Wall((random.randint(0, w),random.randint(0, h)),  (random.randint(0, w),random.randint(0, h)) ))'''

light = Light(walls)

def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
        screen.fill((11,14,15))
        mouse_position = pygame.mouse.get_pos()
        light.controller(mouse_position[0], mouse_position[1])
        light.check_intersection(walls)
        pygame.draw.polygon(screen, pygame.Color((181, 161, 194)), sorted((tuple(v) for v in light.light_points), key=lambda v: math.atan2(v[1]-light.pos.y, v[0]-light.pos.x)) )
        for wall in walls:
            wall.draw()
        pygame.draw.circle(screen,pygame.Color((255, 235, 156)),(light.pos.x, light.pos.y),20)
        
        pygame.display.update()
        clock.tick(120)
        

if __name__ == "__main__":
    main()
