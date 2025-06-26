from dataclasses import dataclass

@dataclass
class Box:
    cls: str
    x1: int 
    y1: int
    x2: int
    y2: int
    depth: float = 0.0

