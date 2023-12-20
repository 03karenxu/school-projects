import numpy as np

class Sphere:
    def __init__(self,name,center,scale,color,ka,kd,ks,kr,n):
        self.name = name
        self.center = np.array(center)
        self.scale = np.array(scale)
        self.color = np.array(color)
        self.ka = ka
        self.kd = kd
        self.ks = ks
        self.kr = kr
        self.n = n
        self.radius = np.mean(self.scale)

    
    def __str__(self):
            return f"Sphere(name={self.name}, center={self.center}, scale={self.scale}, color={self.color}, material={self.ka}{self.kd}{self.ks}{self.kr}{self.n})"
        