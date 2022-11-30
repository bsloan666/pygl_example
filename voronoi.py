#!/usr/bin/env python
"""
Demonstrate using OpenGL to do something intersting.
"""
import math

from numpy import random, sin, cos
from OpenGL.GL import * 
from OpenGL.GLUT import *

import os
import sys
import re

points = []
WIDTH = 1280
HEIGHT = 1280


def generate_point():
    """
    Create a 2d point
    """
    points.append({
        'x':random.randint(0, WIDTH),
        'y':random.randint(0, HEIGHT),
        'r':random.rand(), 'g':random.rand(),
        'b':random.rand(), 'wide':WIDTH})


def init_points(count):
    '''
    Start the scene with some random vertices
    '''
    for i in range(0, count):
        generate_point()

class ViewerWidget():
    '''
    Widget for drawing 3D geometry
    '''

    def __init__(self):
        pass

    def iterate(self):
        xaccum = 0
        yaccum = 0
        for point in points:
            xaccum = xaccum + point['x']
            yaccum = yaccum + point['y']
        xaccum = float(xaccum)/len(points)
        yaccum = float(yaccum)/len(points)
        for point in points:
            point['x'] = point['x'] * 0.995 + xaccum  * 0.005 + point['r'] - 0.5
            point['y'] = point['y'] * 0.995 + yaccum  *  0.005 + point['g'] - 0.5

    def paintGL(self):
        '''
        Drawing routine
        '''

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        incr = (math.pi * 2)/90.0

        for p in points:

            glBegin(GL_TRIANGLE_FAN)

            glColor4f(p['r'], p['g'], p['b'], 1.0)
            glVertex3f(p['x'], p['y'], -0.1)
            glColor4f(p['r'], p['g'], p['b'], 1.0)
            wide = p['wide']
            for i in range(0, 91):
                ang = i * incr
                glVertex3f(p['x'] + sin(ang) * wide, p['y'] + cos(ang) * wide, -wide)


            glEnd()
            incr = (math.pi * 2) /32.0
            glBegin(GL_TRIANGLE_FAN)
            glColor4f(p['r']/2.0, p['g']/2, p['b']/2, 1.0)
            glVertex3f(p['x'], p['y'], -0.1)
            glColor4f(p['r']/2.0, p['g']/2, p['b']/2, 0.0)
            for i in range(0, 33):
                ang = i * incr
                glVertex3f(p['x'] + sin(ang) * 5, p['y'] + cos(ang) * 5, -0.05)

            glEnd()
        glFlush()
        self.iterate()


    def resizeGL(self, w, h):
        '''
        Resize the GL window
        '''

        WIDTH = w
        HEIGHT = h
        glViewport(0, 0, WIDTH, HEIGHT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, WIDTH, 0.0, HEIGHT, 0.0, 640.0)


    def initializeGL(self):
        '''
        Initialize GL
        '''

        # set viewing projection
        glClearColor(0.3, 0.3, 0.3, 1.0)
        glClearDepth(1.0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, WIDTH, 0.0, HEIGHT, 0.0, 640.0)
        glEnable(GL_DEPTH_TEST)


    def mousePressEvent(self, event):
        pos = event.pos()
        if event.button() == 1:
            points.append({
                'x':pos.x(), 'y':HEIGHT - pos.y(),
                'r':random.rand(), 'g':random.rand(),
                'b':random.rand(), 'wide':WIDTH})
        else:
            points.append({
                'x':pos.x(), 'y':HEIGHT - pos.y(),
                'r':0.1, 'g':0.5, 'b':0.1, 'wide':WIDTH})

if __name__ == '__main__':
    print("")
    print("     *****")
    print("     Voronoi Segementation Demo")
    print("     *****")
    print("     Left mouse button ......... create new region")
    print("     *****")
    print("")

    vor = ViewerWidget()

    glutInit() # Initialize a glut instance which will allow us to customize our window
    glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH) # Set the display mode to be colored
    glutInitWindowSize(WIDTH, HEIGHT)   # Set the width and height of your window
    glutInitWindowPosition(0, 0)   # Set the position at which this windows should appear
    wind = glutCreateWindow("OpenGL Voronoi") # Give your window a title
    glutDisplayFunc(vor.paintGL)  # Tell OpenGL to call the showScreen method continuously
    glutIdleFunc(vor.paintGL)  # Tell OpenGL to call the showScreen method continuously

    pcount = 3 
    if len(sys.argv) > 1:
        pcount = int(sys.argv[1])
    vor.initializeGL()
    init_points(pcount)
    glutMainLoop()  # 
