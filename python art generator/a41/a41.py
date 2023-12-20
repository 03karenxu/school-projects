#!/usr/bin/env python
"""Assignment 4 Part 1 Completed"""
print(__doc__)

from typing import IO, NamedTuple

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
    
#CLASSES
class CircleShape:
    """CircleShape class"""
    def __init__(self, cir: Coordinate, col: Color) -> None:
        self.cx: int = cir[0]
        self.cy: int = cir[1]
        self.rad: int = cir[2]
        self.red: int = col[0]
        self.green: int = col[1]
        self.blue: int = col[2]
        self.op: float = col[3]
        
    def as_svg(self, t: int) -> str:
        """as_svg method"""
        ts: str = "   " * t
        line1: str = f'<circle cx="{self.cx}" cy="{self.cy}" r="{self.rad}" '
        line2: str = f'fill="rgb({self.red}, {self.green}, {self.blue})" fill-opacity="{self.op}"></circle>'
        return f"{ts}{line1+line2}\n"
    
class RectangleShape:
    """RectangleShape class"""
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
        return f"{ts}{line1+line2}\n"

class HtmlDocument:
    """HtmlDocument class"""
    def __init__(self, header: str, body: list, f: IO[str]) -> None:
        self.header: str = header
        self.body: list = body
        self.f: IO[str] = f

    def writeHTMLline(self, t:int, line: str) -> None:
        """writeLineHTML method"""
        ts = "   " * t
        self.f.write(f"{ts}{line}\n")
        
    def writeHTMLHeader(self) -> None:
        """writeHeadHTML method"""
        self.writeHTMLline(0, "<html>")
        self.writeHTMLline(0, "<head>")
        self.writeHTMLline(1, f"<title>{self.header}</title>")
        self.writeHTMLline(0, "</head>")
        self.writeHTMLline(0, "<body>")
        
    def genArt(self, t: int) -> None:
        """genART method"""
        for c in self.body:
            self.f.write(c.as_svg(t))
        
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

#METHODS
def writeHTMLfile() -> None:
    """writeHTMLfile method"""
    fnam: str = "a41.html"
    f: IO[str] = open(fnam, "w")
    body: list = [CircleShape((50,50,50), (255,0,0,1.0)), CircleShape((150,50,50), (255,0,0,1.0)),
                  CircleShape((250,50,50), (255,0,0,1.0)), CircleShape((350,50,50), (255,0,0,1.0)),
                  CircleShape((450,50,50), (255,0,0,1.0)), CircleShape((50,250,50), (0,0,255,1.0)),
                  CircleShape((150,250,50), (0,0,255,1.0)), CircleShape((250,250,50), (0,0,255,1.0)),
                  CircleShape((350,250,50), (0,0,255,1.0)), CircleShape((450,250,50), (0,0,255,1.0))]
    doc: HtmlDocument = HtmlDocument("My Art", body, f)
    doc.writeHTMLHeader()
    svg: SvgCanvas = SvgCanvas((500,300), f)
    svg.openSVGcanvas(1)
    doc.genArt(2)
    svg.closeSVGcanvas(1)
    f.close()
    
def main() -> None:
    """main method"""
    
    writeHTMLfile()

if __name__ == "__main__":
    main()
