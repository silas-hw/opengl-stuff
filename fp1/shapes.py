import OpenGL.GL as ogl
import OpenGL.GLU as oglu

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
        ogl.glBegin(ogl.GL_LINES)
        ogl.glColor3fv((1, 1, 1))
        for edge in self.lines:
            for vertex in edge:
                vertex = self.verticies[vertex]
                vertex = (vertex[0]+self.x+1, vertex[1]+self.y+1, vertex[2]+self.z+1)
                ogl.glVertex3fv(vertex)
        ogl.glEnd()
        
        ogl.glBegin(ogl.GL_QUADS)
        for face in self.faces:
            ogl.glColor3fv(self.color)
            for j, vertex in enumerate(face):
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