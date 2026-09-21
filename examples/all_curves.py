from curveforge import (
    circle, ellipse, parabola, hyperbola, astroid, cardioid,
    cycloid, epicycloid, hypocycloid, rose, lemniscate,
)

curves = [
    circle(3), ellipse(5, 3), parabola(1), hyperbola(4, 2), astroid(4),
    cardioid(3), cycloid(1.5, arches=2), epicycloid(3, 1),
    hypocycloid(4, 1), rose(3, 5), lemniscate(4),
]

for curve in curves:
    curve.show()
