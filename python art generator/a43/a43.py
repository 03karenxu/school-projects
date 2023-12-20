#!/usr/bin/env python
import random as rd
from enum import Enum
from typing import IO, List, NamedTuple

# ENUMS AND TUPLES -- Data Classes
class Color(NamedTuple):
    red: int
    green: int
    blue: int
    opacity: float
    
    def __str__(self) -> str:
        return f'({self.red}, {self.green}, {self.blue})'
    
class Coordinate(NamedTuple):
    x: int
    y: int
    
    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

class Dimensions(NamedTuple):
    width: int
    height: int
    
    def __str__(self) -> str:
        return '({self.width}, {self.height})'
    
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


# DOMAIN CLASSES
class PyArtConfig:
    """Input configuration to guide the art style (e.g., fall
    colours pointilistic) to be applied to random shapes"""
    def __init__(self,
                 sha: Irange = Irange(0,1),
                 x: Irange = Irange(0, 1000),
                 y: Irange = Irange(0, 1000),
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
                    
class SvgCanvas:
    """SvgCanvas class"""
    def __init__(self, c: Dimensions, f: IO[str]) -> None:
        self.c: Dimensions = c
        self.f: IO[str] = f
            
    def openSVGcanvas(self, t:int) -> None:
        """openSVGcanvas method"""
        ts: str = "   " * t
        self.writeHTMLcomment(t, "Define SVG drawing box")
        self.f.write(f'{ts}<svg width="{self.c[0]}" height="{self.c[1]}">\n')
    
    def closeSVGcanvas(self, t: int) -> None:
        """closeSVGcanvas method"""
        ts: str = "   " * t
        self.f.write(f"{ts}</svg>\n")
        self.f.write(f"</body>\n")
        self.f.write(f"</html>\n")
        
    def writeHTMLcomment(self, t: int, com: str) -> None:
        """writeHTMLcomment method"""
        ts: str = "   " * t
        self.f.write(f"{ts}<!--{com}-->\n")      

class HtmlDocument:
    """An HTML document that allows appending SVG content"""
    TAB: str = "   "  # HTML indentation tab (default: three spaces)

    def __init__(self, file_name: str, win_title: str) -> None:
        self.win_title: str = win_title
        self.__tabs: int = 0
        self.__file: IO = open(file_name, "w")
        self.__write_head()

    def increase_indent(self) -> None:
        """Increases the number of tab characters used for indentation"""
        self.__tabs += 1

    def decrease_indent(self) -> None:
        """Decreases the number of tab characters used for indentation"""
        self.__tabs -= 1

    def append(self, content: str) -> None:
        """Appends the given HTML content to this document"""
        ts: str = HtmlDocument.TAB * self.__tabs
        self.__file.write(f'{ts}{content}\n')

    def __write_head(self) -> None:
        """Appends the HTML preamble to this document"""
        self.append('<html>')
        self.append('<head>')
        self.increase_indent()
        self.append(f'<title>{self.win_title}</title>')
        self.decrease_indent()
        self.append('</head>')
        self.append('<body>')

    def __write_comment(self, comment: str) -> None:
        """Appends an HTML comment to this document"""
        self.append(f'<!--{comment}-->')

    # more methods needed here
    
    def writeHTMLline(self, t: int, line: str) -> None:
        """writeLineHTML method"""
        ts = "   " * t
        self.__file.write(f"{ts}{line}\n")

    def genArt(self, t: int) -> None:
        """genART method"""
        for c in self.body:
            self.f.write(c.as_svg(t))    

class RandomShape:
    """A shape that can take the form of any type of supported shape"""
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
        if (self.sha == 0):
            l1: str = f'<circle cx="{self.x}" cy="{self.y}" r="{self.rad}" '
            l2: str = f'fill="rgb({self.r}, {self.g}, {self.b})" fill-opacity="{self.op}"></circle>'
            return f'{l1+l2}\n'
        
        elif (self.sha != 2):
            l1: str = f'<rect x="{self.x}" y="{self.y}" width="{self.w}" height="{self.h}"'
            l2: str = f'fill="rgb({self.r}, {self.g}, {self.b})" fill-opacity="{self.op}"></rect>'
            return f"{l1+l2}\n"
        
        else:
            l1: str = f'<ellipse cx="{self.x}" cy="{self.y}" rx="{self.rx}" ry="{self.ry}" '
            l2: str = f'fill="rgb({self.r}, {self.g}, {self.b})" fill-opacity="{self.op}"></ellipse>'
            return f'{l1+l2}\n'

class CircleShape:
    """A circle shape representing an SVG circle element"""
    ccnt: int = 0  # counting number of circles being constructed

    @classmethod
    def get_circle_count(cls) -> int:
        return CircleShape.ccnt

    def __init__(self, rs: RandomShape) -> None:
        """Initializes a circle"""
        self.sha: int = 0
        self.ctx: int = rs.rpt[0]
        self.cty: int = rs.rpt[1]
        self.rad: int = rs.rad
        self.red: int = rs.col[0]
        self.gre: int = rs.col[1]
        self.blu: int = rs.col[2]
        self.op: float = rs.col[3]

    def as_svg(self) -> str:
        """Produces the SVG code representing this shape"""
        return f'<circle cx="{self.ctx}" cy="{self.cty}" r="{self.rad}" ' \
               f'fill="rgb({self.red},{self.gre},{self.blu})" ' \
               f'fill-opacity="{self.op}"></circle>'

    def __str__(self) -> str:
        """String representation of this shape"""
        return f'\nGenerated random circle\n' \
               f'shape = {self.sha}\n' \
               f'radius = {self.rad}\n' \
               f'(centerx, centery) = ({self.ctx},{self.cty})\n' \
               f'(red, green, blue) = ({self.red},{self.gre},{self.blu})\n' \
               f'opacity = {self.op:.1f}\n'
        
class RectangleShape:
    """A rectangle shape that can be drawn as an SVG rect element"""
    def __init__(self, c: Coordinate, d: Dimensions, col: Color) -> None:
        self.cx: int = c[0]
        self.cy: int = c[1]
        self.width: int = d[0]
        self.height: int = d[1]
        self.red: int = col[0]
        self.green: int = col[1]
        self.blue: int = col[2]
        self.op: float = col[3]
        
    def as_svg(self, t: int) -> str:
        """as_svg method"""
        ts: str = "   " * t
        line1: str = f'<rect x="{self.cx}" y="{self.cy}" width="{self.width}" height = "{self.height}"'
        line2: str = f'fill="rgb({self.red}, {self.green}, {self.blue})" fill-opacity="{self.op}"></rect>'
        return f"{ts}{line1+line2}"
    
def writeFile(fnam: str, title: str, width: int, height: int, amount: int, config: PyArtConfig) -> None:
    """writes the output html file"""
    f: IO[str] = open(fnam, "w")
    doc: HtmlDocument = HtmlDocument(fnam, title)
    doc.writeHTMLline(1, f'<svg width="{width}" height="{height}">\n')
    for i in range(0,amount):
        s: RandomShape= RandomShape(config)
        line:str = s.as_svg()
        doc.writeHTMLline(2, line)
    doc.writeHTMLline(1, f"</svg>\n")
    doc.writeHTMLline(0, f"</body>\n")
    doc.writeHTMLline(0, f"</html>\n")
    f.close()
    
def main() -> None:
    """Generate at least three HTML documents with different art styles"""
    
    c1 = PyArtConfig()
    c2 = PyArtConfig(Irange(0,0),
                     Irange(0, 1000),
                     Irange(0, 1000),
                     Irange(0, 200),
                     Irange(5, 500),
                     Irange(5, 500),
                     Irange(10, 100),
                     Irange(10, 100),
                     Irange(0, 100),
                     Irange(0, 0),
                     Irange(50, 100),
                     Frange(0.0, 0.1))
    c3 = PyArtConfig(Irange(1,1),
                     Irange(0, 1000),
                     Irange(0, 1000),
                     Irange(100, 200),
                     Irange(5, 500),
                     Irange(5, 500),
                     Irange(10, 50),
                     Irange(10, 50),
                     Irange(100, 225),
                     Irange(100, 225),
                     Irange(100, 225),
                     Frange(0.0, 0.5))
    writeFile("a431.html", "My Art 1", 1000, 500, 200, c1)
    writeFile("a432.html", "My Art 2", 1000, 500, 200, c2)
    writeFile("a433.html", "My Art 3", 1000, 500, 5000, c3)
    
main()
