CurveForge

Graphics-first mathematical curves for Python.

CurveForge is a Python library for generating, plotting, and exporting mathematical curves using NumPy and Matplotlib.

from curveforge import ellipse, astroid, cycloid

ellipse(a=6, b=3).show()
astroid(a=5).save("astroid.png")
cycloid(r=2).show()
Features
Simple mathematical API
NumPy-powered point generation
Matplotlib-powered graphics
Object-oriented curve classes
.points() for numerical coordinates
.plot() for plotting on an existing Matplotlib axes
.show() for displaying curves
.save() for PNG, SVG, and PDF export
.equation for the curve equation
Parameter validation
Equal-aspect mathematical plots
Included Curves

CurveForge currently includes:

Circle
Ellipse
Parabola
Hyperbola
Astroid
Cardioid
Cycloid
Epicycloid
Hypocycloid
Rose Curve
Lemniscate

Every curve provides:

curve.points()
curve.plot()
curve.show()
curve.save("curve.png")
curve.equation
Installation

Install the latest stable release from PyPI:

python -m pip install curveforge
Quick Start
Circle
from curveforge import circle

c = circle(r=5)

print(c.equation)
points = c.points()

c.show()
Ellipse
from curveforge import ellipse

ellipse(a=6, b=3).show()
Astroid
from curveforge import astroid

astroid(a=5).save("astroid.png")
Cycloid
from curveforge import cycloid

cycloid(r=2).show()
Export

CurveForge supports PNG, SVG, and PDF output.

from curveforge import circle

c = circle(r=5)

c.save("circle.png")
c.save("circle.svg")
c.save("circle.pdf")
Working with Points

.points() returns the numerical coordinates of the curve.

from curveforge import ellipse

points = ellipse(a=6, b=3).points()

print(points.shape)
print(points[:5])

The result is a NumPy array containing the curve's (x, y) coordinates.

Plotting

Use .plot() when you want to add a curve to an existing Matplotlib figure.

import matplotlib.pyplot as plt
from curveforge import circle, ellipse

circle(r=3).plot()
ellipse(a=6, b=2).plot()

plt.show()
Local Development

Clone the repository:

git clone https://github.com/iampremacharya/CurveForge.git
cd CurveForge

Create and activate a virtual environment:

python -m venv .venv

Windows PowerShell:

.\.venv\Scripts\Activate.ps1

Install CurveForge in editable mode:

python -m pip install -e .
Tests

Install the testing dependencies:

python -m pip install -e ".[test]"

Run the test suite:

python -m pytest
Build

Install the build tools:

python -m pip install --upgrade build twine

Build the source distribution and wheel:

python -m build

Check the generated distributions:

python -m twine check dist/*
TestPyPI

Upload a release to TestPyPI:

python -m twine upload --repository testpypi dist/*

For the CurveForge 1.0.2 release:

python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ curveforge==1.0.2
PyPI

Upload the final release to PyPI:

python -m twine upload dist/*

Install CurveForge from PyPI:

python -m pip install curveforge
Project

GitHub:

https://github.com/iampremacharya/CurveForge

License

CurveForge is released under the MIT License.

See LICENSE for the full license text.