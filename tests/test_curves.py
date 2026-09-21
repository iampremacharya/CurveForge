import matplotlib
matplotlib.use("Agg")

import numpy as np
import pytest

from curveforge import *

@pytest.mark.parametrize("curve", [
    circle(2), ellipse(3, 2), parabola(2), hyperbola(3, 2), astroid(2),
    cardioid(2), cycloid(2), epicycloid(3, 1), hypocycloid(3, 1),
    rose(2, 3), lemniscate(2),
])
def test_points(curve):
    points = curve.points(401)
    assert points.shape == (401, 2)
    assert np.isfinite(points).all()
    assert curve.equation

def test_circle_geometry():
    points = circle(5).points(1001)
    assert np.allclose(np.hypot(points[:, 0], points[:, 1]), 5)

def test_ellipse_extrema():
    points = ellipse(6, 3).points(1001)
    assert np.isclose(points[:, 0].max(), 6)
    assert np.isclose(points[:, 1].max(), 3)

def test_cycloid_endpoints():
    points = cycloid(2).points(1001)
    assert np.allclose(points[0], [0, 0])
    assert np.allclose(points[-1], [4 * np.pi, 0])

def test_validation():
    with pytest.raises(ValueError): circle(0)
    with pytest.raises(ValueError): ellipse(-1, 2)
    with pytest.raises(ValueError): cycloid(1, 0)
    with pytest.raises(ValueError): hypocycloid(1, 1)
    with pytest.raises(ValueError): rose(1, 0)

def test_exports(tmp_path):
    for extension in (".png", ".svg", ".pdf"):
        path = circle().save(tmp_path / f"circle{extension}", n=100)
        assert path.exists() and path.stat().st_size > 0

def test_plot_returns_axes():
    ax = circle().plot(n=50)
    assert ax.get_xlabel() == "x"
    assert ax.get_ylabel() == "y"
