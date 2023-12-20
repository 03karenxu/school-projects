import numpy as np

class Light:
    def __init__(self, name, position, intensity):
        self.name = name
        self.position = position
        self.intensity = np.array(intensity)
        
    def __str__(self):
            return f"Light(name={self.name}, position={self.position}, intensity={self.intensity})"