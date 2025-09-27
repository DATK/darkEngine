import pygame
import math
import random

# ---------------- Vector2 ----------------
class Vector2:
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
    def __add__(self,o): return Vector2(self.x+o.x,self.y+o.y)
    def __sub__(self,o): return Vector2(self.x-o.x,self.y-o.y)
    def __mul__(self,f): return Vector2(self.x*f,self.y*f)
    __rmul__ = __mul__
    def dot(self,o): return self.x*o.x + self.y*o.y
    def length(self): return math.hypot(self.x,self.y)
    def normalized(self):
        l=self.length()
        return Vector2(0,0) if l==0 else Vector2(self.x/l,self.y/l)

# ---------------- RectangleShape ----------------
class RectangleShape:
    def __init__(self,hx,hy):
        self.hx=hx
        self.hy=hy
    @property
    def inertia(self):
        return ((self.hx*2)**2 + (self.hy*2)**2)/12
    def get_vertices_world(self,pos,angle):
        cos_a=math.cos(angle)
        sin_a=math.sin(angle)
        pts=[Vector2(-self.hx,-self.hy),Vector2(self.hx,-self.hy),
             Vector2(self.hx,self.hy),Vector2(-self.hx,self.hy)]
        world=[]
        for p in pts:
            x=cos_a*p.x - sin_a*p.y + pos.x
            y=sin_a*p.x + cos_a*p.y + pos.y
            world.append(Vector2(x,y))
        return world

# ---------------- RigidBody ----------------
class RigidBody:
    def __init__(self,shape,mass,pos,angle=0.0,e=0.3):
        self.shape=shape
        self.pos=pos
        self.angle=angle
        self.vel=Vector2(0,0)
        self.omega=0.0
        self.mass=mass
        self.inv_mass=0 if mass==0 else 1/mass
        self.I=shape.inertia*mass
        self.inv_I=0 if self.I==0 else 1/self.I
        self.e=e
        self.supported=False
        self.pivot=None

# ---------------- SAT Collision ----------------
def project_polygon(axis,verts):
    dots=[v.dot(axis) for v in verts]
    return min(dots),max(dots)
def overlap_intervals(a_min,a_max,b_min,b_max):
    return min(a_max,b_max)-max(a_min,b_min)
def sat_collision(a,b):
    verts_a=a.shape.get_vertices_world(a.pos,a.angle)
    verts_b=b.shape.get_vertices_world(b.pos,b.angle)
    axes=[]
    for verts in [verts_a,verts_b]:
        for i in range(4):
            p1=verts[i]; p2=verts[(i+1)%4]
            edge=p2-p1
            normal=Vector2(-edge.y,edge.x)
            l=normal.length()
            if l>0: normal=Vector2(normal.x/l,normal.y/l)
            axes.append(normal)
    min_overlap=float('inf'); smallest_axis=None
    for axis in axes:
        min_a,max_a=project_polygon(axis,verts_a)
        min_b,max_b=project_polygon(axis,verts_b)
        o=overlap_intervals(min_a,max_a,min_b,max_b)
        if o<=0: return None
        if o<min_overlap:
            min_overlap=o
            smallest_axis=axis
    d=a.pos - b.pos
    if d.dot(smallest_axis)<0: smallest_axis=smallest_axis*-1
    return smallest_axis,min_overlap

# ---------------- PhysicsEngine ----------------
class PhysicsEngine:
    def __init__(self,gravity=500.0,window_size=(800,600)):
        self.bodies=[]
        self.gravity=gravity
        self.mu_k=0.3
        self.dt=1/60.0
        self.window_size=window_size
    def add_body(self,body):
        self.bodies.append(body)
    def apply_gravity(self):
        for b in self.bodies:
            if b.inv_mass!=0 and not b.supported: b.vel.y+=self.gravity*self.dt
    def detect_supports(self):
        for body in self.bodies:
            body.supported=False
            body.pivot=None
            # пол
            if body.pos.y + body.shape.hy >= self.window_size[1]:
                body.pos.y = self.window_size[1] - body.shape.hy
                body.vel.y = 0
                body.supported=True
            # поддержка на других кубах
            for other in self.bodies:
                if other==body or other.mass==0: continue
                if (body.pos.y - body.shape.hy <= other.pos.y + other.shape.hy + 1 and
                    body.pos.y - body.shape.hy >= other.pos.y - other.shape.hy):
                    if abs(body.pos.x - other.pos.x) <= other.shape.hx + body.shape.hx:
                        dx=body.pos.x - other.pos.x
                        if abs(dx) > other.shape.hx: 
                            pivot_x=other.pos.x + (other.shape.hx if dx>0 else -other.shape.hx)
                            pivot_y=other.pos.y - other.shape.hy
                            body.pivot=Vector2(pivot_x,pivot_y)
                        else:
                            body.supported=True
                            body.pivot=None
    def resolve_collisions(self):
        n=len(self.bodies)
        for i in range(n):
            for j in range(i+1,n):
                a=self.bodies[i]; b=self.bodies[j]
                res=sat_collision(a,b)
                if res:
                    norm,depth=res
                    # плавная коррекция
                    if not a.pivot: a.pos+=norm*(depth*0.5)
                    if not b.pivot: b.pos-=norm*(depth*0.5)
                    # скорости
                    rv=(a.vel - b.vel)
                    vel_along_norm=rv.dot(norm)
                    if vel_along_norm>0: continue
                    e=min(a.e,b.e)
                    penetration_scale = min(1, depth / 10)
                    j_imp=-(1+e)*vel_along_norm * penetration_scale
                    j_imp/=a.inv_mass+b.inv_mass
                    if abs(vel_along_norm) < 0.5: j_imp *= 0.2
                    impulse=norm*j_imp
                    a.vel+=impulse*a.inv_mass
                    b.vel-=impulse*b.inv_mass
                    # трение
                    tangent=rv - norm*(rv.dot(norm))
                    if tangent.length()>0.0001:
                        tangent=tangent.normalized()
                        jt=-rv.dot(tangent)/(a.inv_mass+b.inv_mass)
                        jt=max(-self.mu_k*j_imp,min(self.mu_k*j_imp,jt))
                        friction_impulse=tangent*jt
                        a.vel+=friction_impulse*a.inv_mass
                        b.vel-=friction_impulse*b.inv_mass
    def integrate(self):
        for b in self.bodies:
            if b.pivot:
                dx=b.pos.x - b.pivot.x
                dy=b.pos.y - b.pivot.y
                r=math.sqrt(dx*dx+dy*dy)
                F=b.mass*self.gravity
                M=F*dx
                alpha=M/b.I if b.I!=0 else 0
                alpha=max(-50,min(50,alpha))
                b.omega+=alpha*self.dt
                b.omega*=0.98
                b.angle+=b.omega*self.dt
                b.pos.x=b.pivot.x + math.cos(b.angle)*r
                b.pos.y=b.pivot.y + math.sin(b.angle)*r
                if abs(dx)<b.shape.hx/2 and abs(b.omega)<0.1:
                    b.supported=True
                    b.pivot=None
                    b.omega=0
            else:
                b.pos+=b.vel*self.dt
                b.angle+=b.omega*self.dt
                # границы
                left=b.pos.x-b.shape.hx; right=b.pos.x+b.shape.hx
                bottom=b.pos.y+b.shape.hy; top=b.pos.y-b.shape.hy
                if bottom>self.window_size[1]:
                    b.pos.y=self.window_size[1]-b.shape.hy
                    b.vel.y*=-b.e
                    b.vel.x*=(1-self.mu_k)
                    b.omega*=(1-self.mu_k)
                if top<0: b.pos.y=b.shape.hy; b.vel.y*=-b.e
                if left<0: b.pos.x=b.shape.hx; b.vel.x*=-b.e
                if right>self.window_size[0]: b.pos.x=self.window_size[0]-b.shape.hx; b.vel.x*=-b.e
    def step(self):
        self.apply_gravity()
        self.detect_supports()
        self.resolve_collisions()
        self.integrate()

# ---------------- Pygame Demo ----------------
def main():
    pygame.init()
    screen=pygame.display.set_mode((800,600))
    pygame.display.set_caption("Realistic 2D Physics Tower")
    clock=pygame.time.Clock()
    engine=PhysicsEngine(gravity=500)

    # пол
    floor=RigidBody(RectangleShape(400,10),0,Vector2(400,590))
    engine.add_body(floor)

    # кубы
    for i in range(20):
        w=random.randint(20,40); h=random.randint(20,40)
        x=400+random.randint(-50,50); y=50+i*45
        cube=RigidBody(RectangleShape(w/2,h/2),1.0,Vector2(x,y),angle=random.uniform(-0.1,0.1))
        engine.add_body(cube)

    running=True
    while running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
        engine.step()
        screen.fill((30,30,30))
        for b in engine.bodies:
            verts=b.shape.get_vertices_world(b.pos,b.angle)
            pygame.draw.polygon(screen,(200,200,200),[(v.x,v.y) for v in verts])
            if b.pivot:
                pygame.draw.circle(screen,(255,0,0),(int(b.pivot.x),int(b.pivot.y)),4)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__=="__main__":
    main()