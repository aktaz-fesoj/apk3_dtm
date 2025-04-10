from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtGui import QMouseEvent, QPaintEvent
from PyQt6.QtWidgets import *
from qpoint3df import *
from edge import *


class Draw(QWidget):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.points = list(QPoint3DF)
        self.dt = list(Edge)
        
    def mousePressEvent(self, e: QMouseEvent):
        #Get coordinates of q
        x = e.position().x()
        y = e.position().y()
        
        p = QPointF(x, y)
            
        self.points.append(p)
            
        #Repaint screen
        self.repaint()
        
        
    def paintEvent(self, e: QPaintEvent):
        #Create new graphic object
        qp = QPainter(self)
        
        #Set graphical attributes
        qp.setPen(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.yellow)
        
        r = 10
        #Draw building
        for point in self.points:
                qp.drawEllipse(int(point.x()-r), int(point.y()-r, r*2, r*2))
        
        #Set graphical attributes
        qp.setPen(Qt.GlobalColor.gray)
        
        #draw tringulation
        for edge in self.dt:
            qp.drawLine(edge.getStart(), edge.getEnd())
    
    def getPoints(self):
        # Returns input point
        return self.points
    
    def setDt(self, dt):
        #sets results, dt
        self.dt = dt
    
    def clearData(self):
        #Clear data
        self.points.clear()
        self.dt.clear()
        
        #Repaint screen
        self.repaint()
