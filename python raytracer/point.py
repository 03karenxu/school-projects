import numpy as np

class Point:
    def __init__(self,position,sphere):
        self.position = position
        self.sphere = sphere
    
    def __str__(self):
        return f"Point(position = {self.position}, sphere = {self.sphere.name})"