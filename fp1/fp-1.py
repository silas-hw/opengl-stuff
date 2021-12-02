import pygame
import pygame.locals as pyg_locals
import OpenGL.GL as ogl
import OpenGL.GLU as oglu
import keyboard, pynput, time, os, json, multiprocessing

import shapes, datatypes, config_menu
import tkinter as tk

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.Logger('log_1')

class MainApp:

    def __init__(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
    
        self.menu_process = multiprocessing.Process(target=self.menu_init)
        self.menu_process.start()

        pygame.init()
        pygame.display.set_mode((800, 600), pyg_locals.DOUBLEBUF | pyg_locals.OPENGL)
            
        oglu.gluPerspective(45, 800/600, 0.1, 50.0)
        oglu.gluLookAt(-15, 15, -15, 0, 0, 0, 0, 1,0)  
        ogl.glEnable(ogl.GL_DEPTH_TEST)

        self.current_frame = 0

        self.angle = 315 #starts at an angle

        self.previousTime = time.time()
            
        self.cube = shapes.Cube((0.4746, 0.9098, 0.57647))
        self.cube2 = shapes.Cube((0.8235, 0.4039, 0.8784), (2, 1.5, 1.5))

        self.cube2.x=10
        self.cube2.z=6
        self.cube2.y=0.5

        self.collision = [[self.cube2.x-1*self.cube2.w, self.cube2.y+1*self.cube2.h, self.cube2.z-1*self.cube2.l], [self.cube2.x+1*self.cube2.w, self.cube2.y-1*self.cube2.h, self.cube2.z+1*self.cube2.l]]

        self.floor = shapes.Floor()
        
        self.mainloop()

    @property
    def delta(self):
        out = time.time()-self.previousTime
        self.previousTime = time.time()
        return out

    @property
    def movement_speed(self):
        with open(f"{self.dir_path}\config.json", "r") as f:
            config = json.load(f)
        
        return config['movement_speed']

    @property
    def rotate_speed(self):
        with open(f"{self.dir_path}\config.json", "r") as f:
            config = json.load(f)
        
        return config['rotate_speed']

    def menu_init(self):
        root = tk.Tk() 
        self.menu = config_menu.Menu(root)
        self.menu.createWindow()

    def mainloop(self):

        #move these to class attributes
        isJump = False
        jump_height = 6
        jump_speed = 25
        jump_progress = 0

        accel = 18
        current_speed = 0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.menu_process.terminate()
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
                if current_speed < self.movement_speed:
                    current_speed += accel*delta

            if not (keyboard.is_pressed("w") or keyboard.is_pressed("s") or keyboard.is_pressed("a") or keyboard.is_pressed("d")):
                current_speed = 0

            #jump code
            if keyboard.is_pressed("space") and (self.checkCollision("D") or self.cube.y<=0.1) and not isJump:
                isJump = True

            if isJump:
                if jump_progress < jump_height:
                    self.cube.y += jump_speed*delta
                    jump_progress += jump_speed*delta
                else:
                    jump_progress = 0
                    isJump = False

            if keyboard.is_pressed("j"):
                ogl.glRotatef(self.rotate_speed*delta, 0, 1, 0) #sometimes zooms out????
                self.angle += self.rotate_speed*delta
                
                if self.angle > 360:
                    self.angle = 0

            if keyboard.is_pressed("l"):
                ogl.glRotatef(-self.rotate_speed*delta, 0, 1, 0) #sometimes zooms out????
                self.angle += -self.rotate_speed*delta
                
                if self.angle <= 0:
                    self.angle = 360

            #move back and forth at view angle
            if keyboard.is_pressed("i"):
                x_proportion = 0
                z_proportion = 0
                if self.angle<90:
                    x_proportion = (self.angle/90)
                    z_proportion = -(90-self.angle)/90
                elif self.angle<180:
                    x_proportion = ((90-(self.angle-90))/90)
                    z_proportion = ((self.angle-90)/90)
                elif self.angle<270:
                    x_proportion = -(self.angle-180)/90
                    z_proportion = ((90-(self.angle-180))/90)
                elif self.angle<360:
                    x_proportion = -(90-(self.angle-270))/90
                    z_proportion = -(self.angle-270)/90

                ogl.glTranslate(10*x_proportion*delta, 0, 10*z_proportion*delta)

            if keyboard.is_pressed("k"):
                x_proportion = 0
                z_proportion = 0
                if self.angle<90:
                    x_proportion = (self.angle/90)
                    z_proportion = -(90-self.angle)/90
                elif self.angle<180:
                    x_proportion = ((90-(self.angle-90))/90)
                    z_proportion = ((self.angle-90)/90)
                elif self.angle<270:
                    x_proportion = -(self.angle-180)/90
                    z_proportion = ((90-(self.angle-180))/90)
                elif self.angle<360:
                    x_proportion = -(90-(self.angle-270))/90
                    z_proportion = -(self.angle-270)/90

                ogl.glTranslate(-10*x_proportion*delta, 0, -10*z_proportion*delta)

            if self.cube.y > 0.1 and not self.checkCollision("D"):
                self.cube.y -= 9*delta

            self.cube.x += x_vel*delta
            self.cube.z += z_vel*delta

            #print(self.cube.x, self.cube.z, self.cube.y)
              
            ogl.glClear(ogl.GL_COLOR_BUFFER_BIT | ogl.GL_DEPTH_BUFFER_BIT)
            self.floor.drawFloor()

            #display fps on window title every 15 frames
            if self.current_frame%15 == 0:
                pygame.display.set_caption(f"FPS:{int(1/delta)}")

            #draw shapes
            self.cube.drawCube()
            self.cube2.drawCube()

            pygame.display.flip()

            self.log()
        
    def checkCollision(self, direction:str=None):
        check_coords = []
        if not direction:
            check_coords = [[self.cube.x-1, self.cube.y+1, self.cube.z-1], [self.cube.x+1, self.cube.y-1, self.cube.z+1]]
        elif direction == "N":
            check_coords = [[self.cube.x-0.9, self.cube.y+0.9, self.cube.z+1.2], [self.cube.x+0.9, self.cube.y-0.9, self.cube.z+1.2]]
        elif direction == "S":
            check_coords = [[self.cube.x-0.9, self.cube.y+0.9, self.cube.z-1.2], [self.cube.x+0.9, self.cube.y-0.9, self.cube.z-1.2]]
        elif direction == "E":
            check_coords = [[self.cube.x+1.2, self.cube.y+0.9, self.cube.z-0.9], [self.cube.x+1.2, self.cube.y-0.9, self.cube.z+0.9]]
        elif direction == "W":
            check_coords = [[self.cube.x-1.2, self.cube.y+0.9, self.cube.z-0.9], [self.cube.x-1.2, self.cube.y-0.9, self.cube.z+0.9]]
        elif direction == "D":
            check_coords = [[self.cube.x-0.99, self.cube.y-1.2, self.cube.z-0.99], [self.cube.x+0.99, self.cube.y-1.2, self.cube.z+0.99]]
            
        if (check_coords[1][0]>=self.collision[0][0]) and (check_coords[0][0]<=self.collision[1][0]):
            if (check_coords[1][1]<=self.collision[0][1]) and (check_coords[0][1]>=self.collision[1][1]):
                if (check_coords[1][2]>=self.collision[0][2]) and (check_coords[0][2]<=self.collision[1][2]):
                    return True
        
        return False

    def log(self):
        logging.info(f"[VIEW ANGLE] {self.angle}")
        logging.info(f"[CUBE COORDS] {self.cube.x}, {self.cube.y}, {self.cube.z}")

if __name__ == '__main__':
    app = MainApp()
    app.mainloop()