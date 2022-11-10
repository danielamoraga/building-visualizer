
import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.scene_graph as sg
import grafica.lighting_shaders as ls
from grafica.assets_path import getAssetPath
import off_obj_reader as obj

import modelo

EMPIRE_STATE = 0
WILLIS_TOWER = 1
BURJ_KHALIFA = 2

LUZ_LUNA = 0
LUZ_SOL = 1

CAMERA_1 = 1
CAMERA_2 = 2
CAMERA_3 = 3
CAMERA_4 = 4
CAMERA_5 = 5

# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.shape = 0
        self.light = 1
        self.camera = 5
###########################################################
        self.theta = np.pi
        self.eye = [0, 0, 0.1]
        self.at = [0, 1, 0.1]
        self.up = [0, 0, 1]
###########################################################


# global controller as communication with the callback function
controller = Controller()

def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS and action != glfw.REPEAT:
        return
    
    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)

    elif key == glfw.KEY_E:
        controller.shape = 0

    elif key == glfw.KEY_W:
        controller.shape = 1

    elif key == glfw.KEY_B:
        controller.shape = 2
    
    elif key == glfw.KEY_L:
        if controller.light==0: controller.light = 1
        else: controller.light = 0

    elif key == glfw.KEY_1:
        controller.camera = 1

    elif key == glfw.KEY_2:
        controller.camera = 2

    elif key == glfw.KEY_3:
        controller.camera = 3

    elif key == glfw.KEY_4:
        controller.camera = 4

    elif key == glfw.KEY_5:
        controller.camera = 5
    
####################################################################################

if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Building viewer", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Creating shader programs for textures and for colors
    textureShaderProgram = es.SimpleTextureModelViewProjectionShaderProgram()
    lightShaderProgram = ls.SimpleGouraudShaderProgram()  # Spoiler de luces
    textureLightShaderProgram = ls.SimpleTextureGouraudShaderProgram()

    # Different shader programs for different lighting strategies
    gouraudPipeline = ls.SimpleGouraudShaderProgram()

    lightingPipeline = gouraudPipeline

    # Setting up the clear screen color
    glClearColor(0.9, 0.9, 0.9, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # View and projection
    projection = tr.perspective(100, float(width)/float(height), 0.1, 50)

    t0 = glfw.get_time()
    camera_theta = -3 * np.pi / 4
    camera_z = 0.0

    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)

    t1 = glfw.get_time()
    t1 = glfw.get_time()

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        # Filling or not the shapes depending on the controller state
        
        if controller.camera == CAMERA_5:

            if (glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS):
                camera_theta += 2 * dt

            if (glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS):
                camera_theta -= 2* dt

            if (glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS):
                camera_z += dt

            if (glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS):
                camera_z -= dt


            projection = tr.ortho(-1, 1, -1, 1, 0.1, 100)
            projection = tr.perspective(45, float(width)/float(height), 0.1, 100)

            camX = 3 * np.sin(camera_theta)
            camY = 3 * np.cos(camera_theta)
            camZ = 3 * np.sin(camera_z)

            viewPos = np.array([camX,camY,1])

            view = tr.lookAt(
                viewPos,
                np.array([0,0,camZ+1.1]),
                np.array([0,0,1])
            )

        rotation_theta = glfw.get_time()

        if controller.camera == CAMERA_1: #edificio desde abajo
            projection = tr.perspective(120, float(width)/float(height), 0.1, 100)
            view = tr.lookAt(
            np.array([0,-1,0.2]),
            np.array([0,0,1]),
            np.array([0,1,1])
        )

        if controller.camera == CAMERA_2:
            #vista desde arriba
            projection = tr.ortho(-1, 1, -1, 1, 0.1, 100)
            view = tr.lookAt(
            np.array([0,0.1,10]),
            np.array([0,0,0]),
            np.array([0,0,2]) 
        )

        if controller.camera == CAMERA_3:
            #projection = tr.ortho(-1, 1, -1, 1, 1.4, 100)
            projection = tr.perspective(90, float(width)/float(height), 0.1, 100)
            view = tr.lookAt(
            np.array([1,1,0.2]),
            np.array([-0.5,-0.5,1]),
            np.array([0,0,1])
        )

        if controller.camera == CAMERA_4:
            #projection = tr.perspective(90, float(width)/float(height), 0.1, 100)
            projection = tr.ortho(-1, 1, -1, 1, 0.1, 100)
            view = tr.lookAt(
            np.array([-np.pi,10,10]),
            np.array([0,0,1]),
            np.array([0,0,2]) 
        )

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

###########################################################################

        glUseProgram(textureShaderProgram.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "view"), 1, GL_TRUE, view)
        
        if controller.shape == EMPIRE_STATE:
            floor = modelo.floor_empire_state(textureShaderProgram)
            edificio = modelo.empire_state(gouraudPipeline)
        elif controller.shape == WILLIS_TOWER:
            floor = modelo.floor_willis_tower(textureShaderProgram)
            edificio = modelo.willis_tower(gouraudPipeline)
        elif controller.shape == BURJ_KHALIFA:
            floor = modelo.floor_burj_khalifa(textureShaderProgram)
            edificio = modelo.burj_khalifa(gouraudPipeline)
        else:
            raise Exception()

        sg.drawSceneGraphNode(floor, textureShaderProgram, "model")

        glUseProgram(lightShaderProgram.shaderProgram)

        lightShaderProgram.set_light_attributes()


        if controller.light == LUZ_LUNA:
            (r,g,b) = (0.0,0.0,0.0)
            if controller.shape==EMPIRE_STATE: (r,g,b) = (0.4,0.4,0.6)
            elif controller.shape==WILLIS_TOWER: (r,g,b) = (0.4,0.2,0.2)
            elif controller.shape==BURJ_KHALIFA: (r,g,b) = (0.0,0.4,0.6)
            glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ka"), 0.17, 0.17, 0.17)
            glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Kd"), r, g, b)
            glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)
            glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "quadraticAttenuation"), 0.008)
                

        if controller.light == LUZ_SOL:
            (r,g,b) = (0.0,0.0,0.0)
            if controller.shape==EMPIRE_STATE: (r,g,b) = (0.6,1.0,1.0)
            elif controller.shape==WILLIS_TOWER: (r,g,b) = (0.8,1.0,1.0)
            elif controller.shape==BURJ_KHALIFA: (r,g,b) = (1.0,0.8,0.4)
            glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ka"), 0.26, 0.26, 0.26)
            glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Kd"), r-0.1, g-0.1, b-0.1)
            glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ks"), r, g, b)
            glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "quadraticAttenuation"), 0.005)

        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "lightPosition"), 5, -5, 5)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "viewPosition"), viewPos[0], viewPos[1], viewPos[2])
        glUniform1ui(glGetUniformLocation(lightingPipeline.shaderProgram, "shininess"), 10)

        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "constantAttenuation"), 0.0001)
        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "linearAttenuation"), 0.01)
        
        glUniformMatrix4fv(glGetUniformLocation(lightShaderProgram.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(lightShaderProgram.shaderProgram, "view"), 1, GL_TRUE, view)

        glUniformMatrix4fv(glGetUniformLocation(lightShaderProgram.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
        sg.drawSceneGraphNode(edificio, gouraudPipeline, "model")


        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    edificio.clear()
    floor.clear()

    glfw.terminate()
