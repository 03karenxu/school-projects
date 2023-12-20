#!/usr/bin/env python

import random as rd
from typing import IO, NamedTuple
from enum import Enum

#NAMEDTUPLES & ENUM
class ShapeKind(str, Enum):
    """Supported shape kinds"""
    CIRCLE = 0
    RECTANGLE = 1
    ELLIPSE = 2

    def __str__(self) -> str:
        return f'{self.value}'
    
class Irange(NamedTuple):
    """A simple integer range with minimum and maximum values"""
    imin: int
    imax: int

    def __str__(self) -> str:
        return f'{self.imin},{self.imax}'

class Frange(NamedTuple):
    """A simple float range with minimum and maximum values"""
    fmin: float
    fmax: float

    def __str__(self) -> str:
        return f'{self.fmin},{self.fmax}'


class Extent(NamedTuple):
    """Extent definition based on width and height ranges"""
    width: Irange
    height: Irange

    def __str__(self) -> str:
        return f'({self.width},{self.height})'
    
class ColorRange(NamedTuple):
    """RGB color definition based on integer ranges"""
    red: Irange
    green: Irange
    blue: Irange
    opacity: Frange

    def __str__(self) -> str:
        return f'({self.red},{self.green},{self.blue})'

 # STATIC FUNCTIONS
def gen_int(r: Irange) -> int:
    """Generates a random integer"""
    return rd.randint(r.imin, r.imax)

def gen_float(r: Frange) -> float:
    """Generates a random float"""
    return rd.uniform(r.fmin, r.fmax)

#CLASSES
class PyArtConfig:
    """PyArtConfig class"""
    def __init__(self,
                 sha: Irange = Irange(0,2),
                 x: Irange = Irange(50, 500),
                 y: Irange = Irange(50, 500),
                 rad: Irange = Irange(10, 100),
                 rx: Irange = Irange(50, 500),
                 ry: Irange = Irange(50, 500),
                 w: Irange = Irange(10, 100),
                 h: Irange = Irange(10, 100),
                 r: Irange = Irange(0, 255),
                 g: Irange = Irange(0, 255),
                 b: Irange = Irange(0, 255),
                 op: Frange = Frange(0.0, 1.0)) -> None:
        self.sha: Irange = sha
        self.x: Irange = x
        self.y: Irange = y
        self.rad: Irange = rad
        self.rx: Irange = rx
        self.ry: Irange = ry
        self.w: Irange = w
        self.h: Irange = h
        self.r: Irange = r
        self.g: Irange = g
        self.b: Irange = b
        self.op: Frange = op

class RandomShape:
    """RandomShape class"""
    def __init__(self, config: PyArtConfig) -> None:
        self.sha: int = gen_int(config.sha)
        self.x: int = gen_int(config.x)
        self.y: int = gen_int(config.y)
        self.rad: int = gen_int(config.rad)
        self.rx: int = gen_int(config.rx)
        self.ry: int = gen_int(config.ry)
        self.w: int = gen_int(config.w)
        self.h: int = gen_int(config.h)
        self.r: int = gen_int(config.r)
        self.g: int = gen_int(config.g)
        self.b: int = gen_int(config.b)
        self.op: float = gen_float(config.op)
        
    def __str__(self) -> str:
        if (self.sha == 0):
            l1: str = f'Shape: Circle, x: {self.x}, y: {self.y}, rad: {self.rad}, '
            l2: str = f'color: ({self.r}, {self.g}, {self.b}, {self.op})\n'
            return l1+l2
        
        elif (self.sha != 2):
            l1: str = f'Shape: Rectangle, x: {self.x}, y: {self.y}, width: {self.w}, '
            l2: str = f'height: {self.h}, color: ({self.r}, {self.g}, {self.b}, {self.op})\n'
            return l1+l2
        
        else:
            l1: str = f'Shape: Circle, x: {self.x}, y: {self.y}, x-rad: {self.rx}, y-rad: {self.ry}, '
            l2: str = f'color: ({self.r}, {self.g}, {self.b}, {self.op})\n'
            return l1+l2
    
    def as_Part2_line(self, count: int) -> str:
        if (count == 0):
            l1: str = f'CNT SHA   X   Y RAD  RX  RY   W   H   R   G   B  OP\n'
            l2: str = f'{count: >3} {self.sha:>3} {self.x: >3} {self.y: >3} {self.rad: >3} '
            l3: str = f'{self.rx: >3} {self.ry: >3} {self.w: >3} {self.h: >3} {self.r: >3} {self.g: >3} {self.b: >3} {self.op: >3.1f}'
            return l1+l2+l3
        else:
            l2: str = f'{count: >3} {self.sha:>3} {self.x: >3} {self.y: >3} {self.rad: >3} '
            l3: str = f'{self.rx: >3} {self.ry: >3} {self.w: >3} {self.h: >3} {self.r: >3} {self.g: >3} {self.b: >3} {self.op: >3.1f}'
            return l2+l3            
        
    def as_svg(self) -> str:
        ts: str = "      "
        if (self.sha == 0):
            l1: str = f'<circle cx="{self.x}" cy="{self.y}" r="{self.rad}" '
            l2: str = f'fill="rgb({self.r}, {self.g}, {self.b})" fill-opacity="{self.op}"></circle>'
            return f'{ts}{l1+l2}\n'
        
        elif (self.sha != 2):
            l1: str = f'<rect x="{self.x}" y="{self.y}" width="{self.w}" height="{self.h}"'
            l2: str = f'fill="rgb({self.r}, {self.g}, {self.b})" fill-opacity="{self.op}"></rect>'
            return f"{ts}{l1+l2}\n"
        
        else:
            l1: str = f'<ellipse cx="{self.x}" cy="{self.y}" rx="{self.rx}" ry="{self.ry}" '
            l2: str = f'fill="rgb({self.r}, {self.g}, {self.b})" fill-opacity="{self.op}"></ellipse>'
            return f'{ts}{l1+l2}\n'    
    
def main() -> None:
    """main method"""
    c = PyArtConfig()
    for i in range (0,10):
        s = RandomShape(c)
        print(s.as_Part2_line(i))

if __name__ == "__main__":
    main()