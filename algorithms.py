from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from math import *
from numpy import *
from numpy.linalg import *
from qpoint3df import *
from edge import *

class Algorithms:
    def __init__(self):
        pass
    
    def get2VectorsAngle(self, p1: QPointF, p2: QPointF, p3: QPointF, p4:QPointF):
        # Compute angle between two vectors
        ux = p2.x() - p1.x()
        uy = p2.y() - p1.y()
        
        vx = p4.x() - p3.x()
        vy = p4.y() - p3.y()
        
        # Dot product
        uv = ux*vx + uy*vy
        
        # Norms u, v
        norm_u = sqrt(ux**2 + uy**2)
        norm_v = sqrt(vx**2 + vy**2)
        
        #Compute argument
        arg = uv/(norm_u*norm_v)
        
        #Correct argument to interval <-1, 1>
        arg = min(max(arg, -1), 1)
        
        return acos(arg)

    def analyzePointandLinePosition(self, p: QPoint3DF, p1: QPoint3DF, p2: QPoint3DF):
        eps = 1.0e-6 #řeší malé odchylky od nuly vzniklé výpočty
        
        ux, uy = p2.x() - p1.x(), p2.y() - p2.x()
        vx, vy = p.x() - p1.x(), p.y() - p1.y()
        
        #determinant test
        t = ux*vy-uy*vx
        
        #if left, returns 1; right -1; on line 0
        
        if t > eps:
            return 1
        
        elif t < -eps:
            return -1
        
        else:
            return 0
        
    def distance2D(self, p1: QPoint3DF, p2:QPoint3DF):
        #computes 2d distance between 2 points
        dx = p1.x() - p2.x()
        dy = p1.y() - p2.y()
        
        return sqrt(dx^2 + dy^2)

    def getNearestPoint(self, q: QPoint3DF, points: list[QPoint3DF]):
        # get point nearest to the query point
        eps = 1.0e-16
        min_dist = 1.0e16
        nearest_point = None
        
        for point in points:
            dist = self.distance2D(q, point)
            #update minimum
            if dist < min_dist:
                min_dist = dist
                nearest_point = point
        return nearest_point
    
    def findDelaunayPoint(self, p1: QPoint3DF, p2: QPoint3DF, points: list[QPoint3DF]):
        omega_max = 0
        delaunay_point = None
        #find optimal delaunay point
        for point in points:
           left = self.analyzePointandLinePosition(point, p1, p2)
           if  left == 1:
              omega = self.get2VectorsAngle(point, p1, point, p2)
              if omega > omega_max:
                  omega_max = omega
                  delaunay_point = point
                  
        return delaunay_point
    
    def delaunayTriangulation(self, points: list[QPoint3DF]):
        dt = [] #list of edges
        ael = [Edge] #list of active edges
        
        p1 = min(points, key=lambda k:k.x())
        
        #find nearest point to p1
        
        p2 = self.getNearestPoint(p1, points)
        
        #create new edges
        e = Edge(p1,p2)
        es = Edge(p2,p1)
        
        #add edges to ael
        ael.append(e)
        ael.append(es)
        
        #repeat until ael is empty
        while ael:
            #take firts edge
            e1 = ael.pop()
            
            #switch orientation of the edge
            e1s = e1.switchOrientation()
            
            p = self.findDelaunayPoint(e1s.getStart(), e1s.getEnd(), points)
            
            if p:
                #create new edges and add them (+ the first edge) to the list of edges
                e2s = Edge(e1s.getEnd(), p)
                e3s = Edge(p, e1s.getStart())
                
                dt.append(e1s)
                dt.append(e2s)
                dt.append(e3s)
                
                #update ael
                self.updateAEL(e2s, ael)
                self.updateAEL(e3s, ael)
                
        return dt
    
    def updateAEL(self, e: Edge, ael: list):
        #search for edge with opposite direction
        es = e.switchOrientation()
        
        if es in ael:
            ael.remove(es)
            
        else:
            ael.append(e)