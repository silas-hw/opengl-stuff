import pygame
import pygame.locals as pyg_locals
import OpenGL.GL as ogl
import OpenGL.GLU as oglu
import keyboard, pynput

class MainApp:

    def __init__(self):
        pygame.init()
        pygame.display.set_mode((800, 600), pyg_locals.DOUBLEBUF | pyg_locals.OPENGL)
            
        oglu.gluPerspective(45, 800/600, 0.1, 50.0)
        oglu.gluLookAt(5, 5, -15, 0, 0, 1, 0, 1,0)  

        self.x = 0
        self.y = 0
        self.z = -15
            
        #ogl.glTranslatef(0.0, 0.0, -15)
        #ogl.glRotatef(0, 0, 0, 0)

        #self.mouse = pynput.mouse.Controller()
        #self.previousMousePos = self.mouse.position

        self.i = 0
            
        self.cube = Cube()

        self.mainloop()

    def mainloop(self):
        flip = True

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            #move the camera based on keyboard input
            x_vel = 0
            y_vel = 0
            z_vel = 0

            if keyboard.is_pressed("w"):
                z_vel += 0.25
            if keyboard.is_pressed("s"):
                z_vel -= 0.25
            if keyboard.is_pressed("a"):
                x_vel += 0.25
            if keyboard.is_pressed("d"):
                x_vel -= 0.25
            if keyboard.is_pressed("e"):
                y_vel += 0.25
            if keyboard.is_pressed("q"):
                y_vel -= 0.25

            #ogl.glRotatef(1, 2, 3, 0)
            self.x += x_vel
            self.y += y_vel
            self.z += z_vel

            #ogl.glTranslatef(x_vel, y_vel, z_vel)
              
            ogl.glClear(ogl.GL_COLOR_BUFFER_BIT | ogl.GL_DEPTH_BUFFER_BIT)
            self.cube.drawCube()

            pygame.display.flip()


class Cube:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

        self.verticies = (
        [1, 1, -1],
        [1, -1, -1],
        [-1, -1, -1],
        [-1, 1, -1],
        [1, 1, 1],
        [1, -1, 1],
        [-1, -1, 1],
        [-1, 1, 1]
        )

        self.lines = (
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),
        (0, 4),
        (1, 5),
        (2, 6),
        (3, 7),
        (4, 5),
        (5, 6),
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

        self.faceColors = [
            (1, 0, 0),
            (0, 1, 0),
            (0, 0, 1),
            (1, 0, 1),
            (1, 1, 0),
            (0, 1, 1)
        ]

    @property
    def coords(self):
        return (self.x, self.y, self.z)
    def drawCube(self):
        ogl.glBegin(ogl.GL_QUADS)
        for i, face in enumerate(self.faces):
            ogl.glColor3fv(self.faceColors[i])
            for j, vertex in enumerate(face):
                vertex = self.verticies[vertex]
                vertex = (vertex[0]+self.x, vertex[1]+self.y, vertex[2]+self.y)
                ogl.glVertex3fv(vertex)
        ogl.glEnd()

        ogl.glBegin(ogl.GL_LINES)
        ogl.glColor3fv((1, 1, 1))
        for edge in self.lines:
            for j, vertex in enumerate(face):
                vertex = self.verticies[vertex]
                vertex = (vertex[0]+self.x, vertex[1]+self.y, vertex[2]+self.y)
                ogl.glVertex3fv(vertex)
        ogl.glEnd()

    def drawCubeNonFixedPipeline(self):
        pass

if __name__ == '__main__':
  app = MainApp()
  app.mainloop()