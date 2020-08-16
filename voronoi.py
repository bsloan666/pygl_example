#!/usr/bin/env python

import math
import random

from numpy import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtOpenGL import *
from PyQt5.QtWidgets import QMainWindow, QApplication
import os,sys,re

points = []
width = 1280
height = 1280


def generate_point():
    points.append({'x':random.randint(0,width), 'y':random.randint(0,height),
        'r':random.rand(), 'g':random.rand(), 'b':random.rand(), 'wide':width})


def init_points(count):
    '''
    Start the scene with some random vertices
    '''
    for i in range(0,count):
        generate_point()

class ViewerWidget(QGLWidget):
    '''
    Widget for drawing 3D geometry 
    '''

    def __init__(self, parent):
        QGLWidget.__init__(self, parent)
        self.setMinimumSize(width, height)

    def iterate(self):
        xaccum = 0
        yaccum = 0
        for point in points:
            xaccum = xaccum + point['x']
            yaccum = yaccum + point['y']
        xaccum = float(xaccum)/len(points)
        yaccum = float(yaccum)/len(points)
        for point in points:
            point['x'] = point['x'] * 0.995 + xaccum  * 0.005 + point['r']-0.5
            point['y'] = point['y'] * 0.995 + yaccum  *  0.005 + point['g']-0.5
        self.update()

    def paintGL(self):
        '''
        Drawing routine
        '''
        global nrms, pts, fcs,degrees, amount, xrot

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW);
        glLoadIdentity()
        incr = (math.pi * 2) /90.0

        for p in points:

            glBegin(GL_TRIANGLE_FAN)

            glColor4f( p['r'],   p['g'],  p['b']  ,1.0)
            glVertex3f( p['x'] , p['y'] , -0.1  )
            glColor4f( p['r'],   p['g'],  p['b']  ,1.0)
            wide = p['wide']
            for i in range(0,91):
                ang = i * incr
                glVertex3f( p['x'] + sin(ang) * wide , p['y'] + cos(ang) * wide , -wide  )

            
            glEnd()
            incr = (math.pi * 2) /32.0
            glBegin(GL_TRIANGLE_FAN)
            glColor4f( p['r']/2.0,   p['g']/2,  p['b']/2  ,1.0)
            glVertex3f( p['x'] , p['y'] , -0.1  )
            glColor4f( p['r']/2.0,   p['g']/2,  p['b']/2  ,0.0)
            for i in range(0,33):
                ang = i * incr
                glVertex3f( p['x'] + sin(ang) * 5 , p['y'] + cos(ang) * 5 , -0.05  )

            glEnd()
        glFlush()
        self.iterate()

    def resizeGL(self, w, h):
        '''
        Resize the GL window 
        '''

        width = w
        height = h
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, width, 0.0, height, 0.0, 640.0)
        self.update()

    def initializeGL(self):
        '''
        Initialize GL
        '''

        # set viewing projection
        glClearColor(0.3, 0.3, 0.3, 1.0)
        glClearDepth(1.0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, width, 0.0, height, 0.0, 640.0)
        glEnable(GL_DEPTH_TEST)
#        glEnable(GL_BLEND)
#        glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


    def mousePressEvent (self, event):
        pos = event.pos()
        if event.button() == 1:
            points.append({'x':pos.x(), 'y':height - pos.y(),
                'r':random.rand(), 'g':random.rand(), 'b':random.rand(), 'wide':width})
        else:
            points.append({'x':pos.x(), 'y':height - pos.y(),
                'r':0.1, 'g':0.5, 'b':0.1, 'wide':width})
        self.update()

# You don't need anything below this
class ViewerWidgetDemo(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        widget = ViewerWidget(self)
        self.setCentralWidget(widget)

if __name__ == '__main__':
    app = QApplication(['Voronoi Segementation Demo'])
    print( "")
    print( "     *****")
    print( "     Voronoi Segementation Demo")
    print( "     *****")
    print( "     Left mouse button ......... create new region")
    print( "     *****")
    print( "")

    window = ViewerWidgetDemo()
    window.show()
    pcount = 100
    if len(sys.argv) > 1:
        pcount = int(sys.argv[1])
    init_points(pcount)
    app.exec_()

