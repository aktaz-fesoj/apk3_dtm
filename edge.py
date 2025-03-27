from qpoint3df import *

class Edge:
    def __init__(self, p1:QPoint3DF, p2:QPoint3DF):
        self.start = p1
        self.end = p2
        
    def getStart(self):
        return self.start
    
    def getEnd(self):
        return self.end
    
    def switchOrientation(self):
        return Edge(self.end, self.start)
    
    
    
    