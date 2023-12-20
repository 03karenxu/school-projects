
class Scene:
    def __init__(self):
        self.near = None
        self.left = None
        self.right = None
        self.bottom = None
        self.top = None
        self.res_x = None
        self.res_y = None
        self.spheres = []
        self.lights = []
        self.background = None
        self.ambient = None
        self.output = None
        
    def __str__(self):
        spheres_str = "[" + ", ".join(str(sphere) for sphere in self.spheres) + "]"
        lights_str = "[" + ", ".join(str(light) for light in self.lights) + "]"        
        return (
            f"Scene(near={self.near}\n left={self.left}\n right={self.right}\n "
            f"bottom={self.bottom}\ntop={self.top}\nres_x={self.res_x}\nres_y={self.res_y}\n"
            f"spheres={spheres_str}\nlights={lights_str}\nbackground={self.background}\n"
            f"ambient={self.ambient}\noutput={self.output}\n)"
        )

    