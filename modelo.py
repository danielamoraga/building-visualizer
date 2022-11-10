
import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grafica.transformations as tr
import grafica.basic_shapes as bs
from grafica.basic_shapes import createColorNormalsCube
import grafica.easy_shaders as es
import grafica.scene_graph as sg
from grafica.scene_graph import SceneGraphNode
import grafica.lighting_shaders as ls
from grafica.assets_path import getAssetPath
import off_obj_reader as obj

############################################################################

def floor_empire_state(pipeline):
    shapeFloor = bs.createTextureQuad(1, 1)
    gpuFloor = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuFloor)
    gpuFloor.texture = es.textureSimpleSetup(
        getAssetPath("EMPIRESTATEMAP.png"), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_LINEAR, GL_LINEAR)
    gpuFloor.fillBuffers(shapeFloor.vertices, shapeFloor.indices, GL_STATIC_DRAW)

    floor = sg.SceneGraphNode("floor")
    floor.transform = tr.matmul([tr.translate(0, 0, 0),tr.scale(2, 2, 0)])
    floor.childs += [gpuFloor]

    return floor


def floor_willis_tower(pipeline):
    shapeFloor = bs.createTextureQuad(1, 1)
    gpuFloor = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuFloor)
    gpuFloor.texture = es.textureSimpleSetup(
        getAssetPath("WILLISTOWERMAP.png"), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_LINEAR, GL_LINEAR)
    gpuFloor.fillBuffers(shapeFloor.vertices, shapeFloor.indices, GL_STATIC_DRAW)

    floor = sg.SceneGraphNode("floor")
    floor.transform = tr.matmul([tr.translate(0, 0, 0),tr.scale(2, 2, 0)])
    floor.childs += [gpuFloor]

    return floor


def floor_burj_khalifa(pipeline):
    shapeFloor = bs.createTextureQuad(1, 1)
    gpuFloor = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuFloor)
    gpuFloor.texture = es.textureSimpleSetup(
        getAssetPath("burjkhalifamap.jpeg"), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_LINEAR, GL_LINEAR)
    gpuFloor.fillBuffers(shapeFloor.vertices, shapeFloor.indices, GL_STATIC_DRAW)

    floor = sg.SceneGraphNode("floor")
    floor.transform = tr.matmul([tr.translate(0, 0, 0),tr.scale(2, 2, 0)])
    floor.childs += [gpuFloor]

    return floor


def empire_state(pipeline):

    cone = obj.readOBJ(getAssetPath('cone.obj'), (0.5, 0.5, 0.5))
    gpuCone = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuCone)
    gpuCone.fillBuffers(cone.vertices, cone.indices, GL_STATIC_DRAW)

    cube=createColorNormalsCube(0.7,0.7,0.7)
    gpuCube=es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuCube)
    gpuCube.fillBuffers(cube.vertices, cube.indices, GL_STATIC_DRAW)

    base=sg.SceneGraphNode('base')
    base.transform=tr.matmul([tr.translate(0, 0.25/2, 0), tr.scale(1, 0.25, 0.45)])
    base.childs += [gpuCube]

    parte_dos = sg.SceneGraphNode('parte_dos')
    parte_dos.transform = tr.matmul([tr.translate(0, 0.25+0.7/2, 0), tr.scale(0.8, 0.7, 0.25)])
    parte_dos.childs += [gpuCube]

    ###exterior segunda parte del edificio###

    parte_dos_ext_der = sg.SceneGraphNode('parte_dos_exterior')
    parte_dos_ext_der.transform = tr.matmul([tr.translate(0.2625, 0.25+0.5/2, 0), tr.scale(0.35, 0.5, 0.35)])
    parte_dos_ext_der.childs += [gpuCube]

    parte_dos_ext_izq = sg.SceneGraphNode('parte_dos_exterior')
    parte_dos_ext_izq.transform = tr.matmul([tr.translate(-0.2625, 0.25+0.5/2, 0), tr.scale(0.35, 0.5, 0.35)])
    parte_dos_ext_izq.childs += [gpuCube]

    ######

    parte_tres = sg.SceneGraphNode('parte_tres')
    parte_tres.transform = tr.matmul([tr.translate(0, 0.95+1.85/2, 0), tr.scale(0.32, 1.85, 0.17)])
    parte_tres.childs += [gpuCube]

    ###exterior tercera parte del edificio###
    parte_tres_base = sg.SceneGraphNode('parte_tres_base')
    parte_tres_base.transform = tr.matmul([tr.translate(0, 0.95+0.2/2, 0), tr.scale(0.6, 0.2, 0.21)])
    parte_tres_base.childs += [gpuCube]

    parte_tres_izq = sg.SceneGraphNode('parte_tres_izq')
    parte_tres_izq.transform = tr.matmul([tr.translate(-0.195, 0.95+1.4/2, 0), tr.scale(0.21, 1.4, 0.21)])
    parte_tres_izq.childs += [gpuCube]

    parte_tres_der = sg.SceneGraphNode('parte_tres_der')
    parte_tres_der.transform = tr.matmul([tr.translate(0.195, 0.95+1.4/2, 0), tr.scale(0.21, 1.4, 0.21)])
    parte_tres_der.childs += [gpuCube]
    ######

    ultimo_piso = sg.SceneGraphNode('ultimo_piso')
    ultimo_piso.transform = tr.matmul([tr.translate(0, 2.8+0.15/2, 0), tr.scale(0.08, 0.15, 0.07)])
    ultimo_piso.childs += [gpuCube]

    antena2 = sg.SceneGraphNode('antena2')
    antena2.transform = tr.matmul([tr.translate(0, 2.95, 0), tr.scale(0.05,0.4,0.05),tr.rotationY(-np.pi/2)])
    antena2.childs += [gpuCone]

    # Ensamblamos el edificio
    edificio = sg.SceneGraphNode('edificio')
    edificio.transform = tr.matmul([tr.rotationX(np.pi/2), tr.translate(0,0,0), tr.scale(0.43,0.43,0.43)])
    edificio.childs += [
        base,
        parte_dos,
        parte_dos_ext_der,
        parte_dos_ext_izq,
        parte_tres,
        parte_tres_base,
        parte_tres_izq,
        parte_tres_der,
        ultimo_piso,
        antena2
    ]

    return edificio


def willis_tower(pipeline):

    cone = obj.readOBJ(getAssetPath('cone.obj'), (1, 1, 1))
    gpuCone = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuCone)
    gpuCone.fillBuffers(cone.vertices, cone.indices, GL_STATIC_DRAW)

    cube=createColorNormalsCube(0.5,0.5,0.5)
    gpuCube=es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuCube)
    gpuCube.fillBuffers(cube.vertices, cube.indices, GL_STATIC_DRAW)

    parte_uno_a = sg.SceneGraphNode('parte_uno_a')
    parte_uno_a.transform = tr.matmul([tr.translate(1/3,(150/69)/2,-1/3), tr.scale(1/3,150/69,1/3)])
    parte_uno_a.childs += [gpuCube]
    
    parte_uno_b = sg.SceneGraphNode('parte_uno_b')
    parte_uno_b.transform = tr.matmul([tr.translate(-1/3,(150/69)/2,1/3), tr.scale(1/3,150/69,1/3)])
    parte_uno_b.childs += [gpuCube]

    parte_dos_a = sg.SceneGraphNode('parte_dos_a')
    parte_dos_a.transform = tr.matmul([tr.translate(1/3,(200/69)/2,1/3), tr.scale(1/3,(200/69),1/3)])
    parte_dos_a.childs += [gpuCube]

    parte_dos_b = sg.SceneGraphNode('parte_dos_b')
    parte_dos_b.transform = tr.matmul([tr.translate(-1/3,(200/69)/2,-1/3), tr.scale(1/3,(200/69),1/3)])
    parte_dos_b.childs += [gpuCube]

    parte_tres_a = sg.SceneGraphNode('parte_tres_a')
    parte_tres_a.transform = tr.matmul([tr.translate(1/3,(350/69)/2,0), tr.scale(1/3,(350/69),1/3)])
    parte_tres_a.childs += [gpuCube]

    parte_tres_b = sg.SceneGraphNode('parte_tres_b')
    parte_tres_b.transform = tr.matmul([tr.translate(0,(350/69)/2,1/3), tr.scale(1/3,(350/69),1/3)])
    parte_tres_b.childs += [gpuCube]

    parte_tres_c = sg.SceneGraphNode('parte_tres_c')
    parte_tres_c.transform = tr.matmul([tr.translate(-1/3,(350/69)/2,0), tr.scale(1/3,(350/69),1/3)])
    parte_tres_c.childs += [gpuCube]

    parte_cuatro_a = sg.SceneGraphNode('parte_cuatro_a')
    parte_cuatro_a.transform = tr.matmul([tr.translate(0,(450/69)/2,0), tr.scale(1/3,(450/69),1/3)])
    parte_cuatro_a.childs += [gpuCube]

    parte_cuatro_b = sg.SceneGraphNode('parte_cuatro_b')
    parte_cuatro_b.transform = tr.matmul([tr.translate(0,(450/69)/2,-1/3), tr.scale(1/3,(450/69),1/3)])
    parte_cuatro_b.childs += [gpuCube]

    antena_a = sg.SceneGraphNode('antena_a')
    antena_a.transform = tr.matmul([tr.translate(0,(450/69),0), tr.scale(1/10,8/9,1/10),tr.rotationY(-np.pi/2)])
    antena_a.childs += [gpuCone]

    antena_b = sg.SceneGraphNode('antena_b')
    antena_b.transform = tr.matmul([tr.translate(0,(450/69),-1/3), tr.scale(1/10,8/9,1/10),tr.rotationY(-np.pi/2)])
    antena_b.childs += [gpuCone]

    # Ensamblamos el edificio
    edificio = sg.SceneGraphNode('edificio')
    edificio.transform = tr.matmul([tr.rotationX(np.pi/2), tr.translate(0,0,0),tr.scale(0.23,0.23,0.23)])
    edificio.childs += [
        parte_uno_a,
        parte_uno_b,
        parte_dos_a,
        parte_dos_b,
        parte_tres_a,
        parte_tres_b,
        parte_tres_c,
        parte_cuatro_a,
        parte_cuatro_b,
        antena_a,
        antena_b
        ]

    return edificio


def burj_khalifa(pipeline):

    cylinder = obj.readOBJ(getAssetPath('cilindar.obj'), (0.6, 0.6, 0.6))
    gpuCylinder = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuCylinder)
    gpuCylinder.fillBuffers(cylinder.vertices, cylinder.indices, GL_STATIC_DRAW)

    base1 = sg.SceneGraphNode('base1')
    base1.transform = tr.matmul([tr.scale(1/9,0.05,1/9),tr.translate(5.5,1,0)])
    base1.childs += [gpuCylinder]

    base2 = sg.SceneGraphNode('base2')
    base2.transform = tr.translate(-0.025,0.05,0)
    base2.childs += [base1]

    base3 = sg.SceneGraphNode('base3')
    base3.transform = tr.translate(-0.05,0.1,0)
    base3.childs += [base1]

    base = sg.SceneGraphNode('base')
    base.transform = tr.identity()
    base.childs += [base1,base2,base3]

    base_2 = sg.SceneGraphNode('base_2')
    base_2.transform = tr.rotationY(2*np.pi/3)
    base_2.childs += [base]

    base_3 = sg.SceneGraphNode('base_3')
    base_3.transform = tr.rotationY(-2*np.pi/3)
    base_3.childs += [base]

    bases = sg.SceneGraphNode('bases')
    bases.transform = tr.identity()
    bases.childs += [base,base_2,base_3]
    
    centro = sg.SceneGraphNode('centro')
    centro.transform = tr.matmul([tr.scale(1/9,5*2.5/7,1/9),tr.translate(0,1,0)])
    centro.childs += [gpuCylinder]

    side1_1 = sg.SceneGraphNode('side1_1')
    side1_1.transform = tr.matmul([tr.scale(1/9,5*2.5/7,1/9),tr.translate(1,1,0)])
    side1_1.childs += [gpuCylinder]

    side1_2 = sg.SceneGraphNode('side1_2')
    side1_2.transform = tr.matmul([tr.scale(1/9,3*2.5/7,1/9),tr.translate(2,1,0)])
    side1_2.childs += [gpuCylinder]

    side1_3 = sg.SceneGraphNode('side1_3')
    side1_3.transform = tr.matmul([tr.scale(1/9,2*2.5/7,1/9),tr.translate(3,1,0)])
    side1_3.childs += [gpuCylinder]

    side1_4 = sg.SceneGraphNode('side1_4')
    side1_4.transform = tr.matmul([tr.scale(1/9,2.5/7,1/9),tr.translate(4,1,0)])
    side1_4.childs += [gpuCylinder]

    side1 = sg.SceneGraphNode('side1')
    side1.transform = tr.identity()
    side1.childs += [
        side1_1,
        side1_2,
        side1_3,
        side1_4
        ]

    side2_1 = sg.SceneGraphNode('side2_1')
    side2_1.transform = tr.matmul([tr.scale(1/9,2.5/(21/2)+4*2.5/7,1/9),tr.translate(1,1,0)])
    side2_1.childs += [gpuCylinder]

    side2_2 = sg.SceneGraphNode('side2_2')
    side2_2.transform = tr.matmul([tr.scale(1/9,2.5/(21/2)+3*2.5/7,1/9),tr.translate(2,1,0)])
    side2_2.childs += [gpuCylinder]

    side2_3 = sg.SceneGraphNode('side2_3')
    side2_3.transform = tr.matmul([tr.scale(1/9,2.5/(21/2)+2*2.5/7,1/9),tr.translate(3,1,0)])
    side2_3.childs += [gpuCylinder]

    side2_4 = sg.SceneGraphNode('side2_4')
    side2_4.transform = tr.matmul([tr.scale(1/9,2.5/(21/2)+2.5/7,1/9),tr.translate(4,1,0)])
    side2_4.childs += [gpuCylinder]

    side2 = sg.SceneGraphNode('side2')
    side2.transform = tr.rotationY(4*np.pi/3)
    side2.childs += [
        side2_1,
        side2_2,
        side2_3,
        side2_4
        ]

    side3_1 = sg.SceneGraphNode('side3_1')
    side3_1.transform = tr.matmul([tr.scale(1/9,2.5/21+4*2.5/7,1/9),tr.translate(1,1,0)])
    side3_1.childs += [gpuCylinder]

    side3_2 = sg.SceneGraphNode('side3_2')
    side3_2.transform = tr.matmul([tr.scale(1/9,2.5/21+3*2.5/7,1/9),tr.translate(2,1,0)])
    side3_2.childs += [gpuCylinder]

    side3_3 = sg.SceneGraphNode('side3_3')
    side3_3.transform = tr.matmul([tr.scale(1/9,2.5/21+2*2.5/7,1/9),tr.translate(3,1,0)])
    side3_3.childs += [gpuCylinder]

    side3_4 = sg.SceneGraphNode('side3_4')
    side3_4.transform = tr.matmul([tr.scale(1/9,2.5/21+2.5/7,1/9),tr.translate(4,1,0)])
    side3_4.childs += [gpuCylinder]

    side3 = sg.SceneGraphNode('side3')
    side3.transform = tr.rotationY(2*np.pi/3)
    side3.childs += [
        side3_1,
        side3_2,
        side3_3,
        side3_4
        ]

    antena_base = sg.SceneGraphNode('antena_base')
    antena_base.transform = tr.matmul([tr.translate(0,1+1.6*5*2.5/7,0),tr.scale(1/15,2.5/7,1/15)])
    antena_base.childs += [gpuCylinder]

    antena_top =sg.SceneGraphNode('antena_top')
    antena_top.transform = tr.matmul([tr.translate(0,1+1.6*5*2.5/7+2*2.5/7,0),tr.scale(1/20,2.5/7,1/20)])
    antena_top.childs += [gpuCylinder]

    antena = sg.SceneGraphNode('antena')
    antena.transform = tr.identity()
    antena.childs += [antena_base,antena_top]

    # Ensamblamos el edificio
    edificio = sg.SceneGraphNode('edificio')
    edificio.transform = tr.matmul([tr.rotationX(np.pi/2), tr.translate(0,0,0),tr.scale(0.5,0.5,0.5),tr.rotationY(-np.pi/6)])
    edificio.childs += [
        bases,
        centro,
        side1,
        side2,
        side3,
        antena
        ]

    return edificio