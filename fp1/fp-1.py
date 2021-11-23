import pygame
import pygame.locals as pyg_locals
import OpenGL.GL as ogl
import OpenGL.GLU as oglu
import keyboard, pynput, time

class MainApp:

    def __init__(self):
        pygame.init()
        pygame.display.set_mode((800, 600), pyg_locals.DOUBLEBUF | pyg_locals.OPENGL)

        #fps and xyz text
        pygame.font.init()
        self.fpsfont = pygame.font.SysFont("Proxy 1", 5)
            
        oglu.gluPerspective(45, 800/600, 0.1, 50.0)
        oglu.gluLookAt(-15, 15, -15, 0, 0, 0, 0, 1,0)  
            
        #ogl.glTranslatef(0.0, 0.0, -15)
        #ogl.glRotatef(0, 0, 0, 0)

        #self.mouse = pynput.mouse.Controller()
        #self.previousMousePos = self.mouse.position

        self.current_frame = 0

        self.i = 0

        self.previousTime = time.time()
            
        self.cube = Cube((0.4746, 0.9098, 0.57647))
        self.cube2 = Cube((0.8235, 0.4039, 0.8784), (2, 1.5, 1.5))

        self.cube2.x=10
        self.cube2.z=6

        self.collision = [[self.cube2.x-1*self.cube2.w, self.cube2.y+1*self.cube2.h, self.cube2.z-1*self.cube2.l], [self.cube2.x+1*self.cube2.w, self.cube2.y-1*self.cube2.h, self.cube2.z+1*self.cube2.l]]

        self.floor = Floor()
        
        self.mainloop()

    @property
    def delta(self):
        out = time.time()-self.previousTime
        self.previousTime = time.time()
        return out

    def mainloop(self):

        #move these to class attributes
        isJump = False
        jump_height = 6
        jump_speed = 25
        jump_progress = 0

        movement_speed = 15
        accel = 18
        current_speed = 0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.current_frame += 1

            #move the cube based on keyboard
            x_vel = 0
            y_vel = 0
            z_vel = 0

            delta = self.delta
            if delta == 0:
                delta = 1

            if keyboard.is_pressed("w") and self.cube.z < 15.5 and not self.checkCollision("N"):
                z_vel += current_speed
            if keyboard.is_pressed("s") and self.cube.z > -6.25 and not self.checkCollision("S"):
                z_vel -= current_speed
            if keyboard.is_pressed("a") and self.cube.x < 15.5 and not self.checkCollision("E"):
                x_vel += current_speed
            if keyboard.is_pressed("d") and self.cube.x > -6.25 and not self.checkCollision("W"):
                x_vel -= current_speed

            #code for acceleration
            if keyboard.is_pressed("w") or keyboard.is_pressed("s") or keyboard.is_pressed("a") or keyboard.is_pressed("d"):
                if current_speed < movement_speed:
                    current_speed += accel*delta

            if not (keyboard.is_pressed("w") or keyboard.is_pressed("s") or keyboard.is_pressed("a") or keyboard.is_pressed("d")):
                current_speed = 0

            #jump code
            if keyboard.is_pressed("space") and (self.checkCollision("D") or self.cube.y<=0) and not isJump:
                isJump = True

            if isJump:
                if jump_progress < jump_height:
                    self.cube.y += jump_speed*delta
                    jump_progress += jump_speed*delta
                else:
                    jump_progress = 0
                    isJump = False
                
            if self.cube.y > 0 and not self.checkCollision("D"):
                self.cube.y -= 9*delta

            self.cube.x += x_vel*delta
            self.cube.z += z_vel*delta

            #print(self.cube.x, self.cube.z, self.cube.y)

            if keyboard.is_pressed("j"):
                ogl.glRotatef(180*self.delta, 0, 0, 0)
              
            ogl.glClear(ogl.GL_COLOR_BUFFER_BIT | ogl.GL_DEPTH_BUFFER_BIT)
            self.floor.drawFloor()

            #display fps on window title every 15 frames
            if self.current_frame%15 == 0:
                pygame.display.set_caption(f"FPS:{int(1/delta)}")

            if self.cube.x-self.cube.w+0.1 < self.cube2.x+self.cube2.w and self.cube.z-self.cube.l+0.1 < self.cube2.z+self.cube2.l: #WHY ISNT THIS WORKING????????
                self.cube2.drawCube()
                self.cube.drawCube()
            else:
                self.cube.drawCube()
                self.cube2.drawCube()

            pygame.display.flip()
        

    def checkCollision(self, direction:str=None):
        if not direction:
            check_coords = [[self.cube.x-1, self.cube.y+1, self.cube.z-1], [self.cube.x+1, self.cube.y-1, self.cube.z+1]]
        elif direction == "N":
            check_coords = [[self.cube.x-0.9, self.cube.y+0.9, self.cube.z+1], [self.cube.x+0.9, self.cube.y-0.9, self.cube.z+1]]
        elif direction == "S":
            check_coords = [[self.cube.x-0.9, self.cube.y+0.9, self.cube.z-1], [self.cube.x+0.9, self.cube.y-0.9, self.cube.z-1]]
        elif direction == "E":
            check_coords = [[self.cube.x+1, self.cube.y+0.9, self.cube.z-0.9], [self.cube.x+1, self.cube.y-0.9, self.cube.z+0.9]]
        elif direction == "W":
            check_coords = [[self.cube.x-1, self.cube.y+0.9, self.cube.z-0.9], [self.cube.x-1, self.cube.y-0.9, self.cube.z+0.9]]
        elif direction == "D":
            check_coords = [[self.cube.x-0.99, self.cube.y-1, self.cube.z-0.99], [self.cube.x+0.99, self.cube.y-1, self.cube.z+0.99]]
            
        if (check_coords[1][0]>=self.collision[0][0]) and (check_coords[0][0]<=self.collision[1][0]):
            if (check_coords[1][1]<=self.collision[0][1]) and (check_coords[0][1]>=self.collision[1][1]):
                if (check_coords[1][2]>=self.collision[0][2]) and (check_coords[0][2]<=self.collision[1][2]):
                    return True
        
        return False



class Cube:
    def __init__(self, color:tuple=(1, 1, 1), size:tuple=(1, 1, 1)):
        self.l = size[0]
        self.w = size[1]
        self.h = size[2]

        self.x = 0
        self.y = self.h-1
        self.z = 0

        self.verticies = (
        (1*self.w, 1*self.h, -1*self.l),
        (1*self.w, -1*self.h, -1*self.l),
        (-1*self.w, -1*self.h, -1*self.l),
        (-1*self.w, 1*self.h, -1*self.l),
        (1*self.w, 1*self.h, 1*self.l),
        (1*self.w, -1*self.h, 1*self.l),
        (-1*self.w, -1*self.h, 1*self.l),
        (-1*self.w, 1*self.h, 1*self.l)
        )

        self.lines = (
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),
        (0, 4),
        (2, 6),
        (3, 7),
        (6, 7),
        (7, 4)
        )

        self.faces = (
            (0, 1, 2, 3),
            (0, 4, 7, 3),
            (0, 1, 5, 4),
            (1, 5, 6, 2),
            (2, 3, 7, 6),
            (4, 5, 6, 7)
        )

        self.color = color

    @property
    def coords(self):
        return (self.x, self.y, self.z)

    def drawCube(self):
        ogl.glBegin(ogl.GL_QUADS)
        for face in self.faces:
            ogl.glColor3fv(self.color)
            for j, vertex in enumerate(face):
                vertex = self.verticies[vertex]
                vertex = (vertex[0]+self.x+1, vertex[1]+self.y+1, vertex[2]+self.z+1)
                ogl.glVertex3fv(vertex)
        ogl.glEnd()

        ogl.glBegin(ogl.GL_LINES)
        ogl.glColor3fv((1, 1, 1))
        for edge in self.lines:
            for vertex in edge:
                vertex = self.verticies[vertex]
                vertex = (vertex[0]+self.x+1, vertex[1]+self.y+1, vertex[2]+self.z+1)
                ogl.glVertex3fv(vertex)
        ogl.glEnd()

class Floor():

    def __init__(self):
        self.y = 0

        self.verticies = (
            (17.5, 0, 17.5),
            (17.5, 0, -6.25),
            (-6.25, 0, -6.25),
            (-6.25, 0, 17.5)
        )

        self.lines = (
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 0)
        )

        self.faces = [(0, 1, 2, 3)]

        self.color = (0.478, 0.757, 0.922)

    def drawFloor(self):
        ogl.glBegin(ogl.GL_QUADS)
        for face in self.faces:
            ogl.glColor3fv(self.color)
            for vertex in face:
                vertex = self.verticies[vertex]
                vertex = (vertex[0], vertex[1]+self.y, vertex[2])
                ogl.glVertex3fv(vertex)
        ogl.glEnd()

        ogl.glBegin(ogl.GL_LINES)
        ogl.glColor3fv((1, 1, 1))
        for edge in self.lines:
            for vertex in edge:
                vertex = self.verticies[vertex]
                vertex = (vertex[0], vertex[1]+self.y, vertex[2])
                ogl.glVertex3fv(vertex)
        ogl.glEnd()

if __name__ == '__main__':
  app = MainApp()
  app.mainloop()