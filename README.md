# CurveForge

Graphics-first mathematical curves for Python.

```python
from curveforge import ellipse, astroid, cycloid

ellipse(a=6, b=3).show()
astroid(a=5).save("astroid.png")
cycloid(r=2).show()
```

## Included curves

Circle, ellipse, parabola, hyperbola, astroid, cardioid, cycloid, epicycloid,
hypocycloid, rose curve, and lemniscate.

Each curve supports `.points()`, `.plot()`, `.show()`, `.save()`, and `.equation`.
PNG, SVG, and PDF exports are supported.

## Local installation

```powershell
python -m pip install -e .
```

## Tests

```powershell
python -m pip install -e ".[test]"
python -m pytest
```

## Build

```powershell
python -m pip install --upgrade build twine
python -m build
```

## TestPyPI

```powershell
python -m twine upload --repository testpypi dist/*
python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ curveforge
```

## PyPI

```powershell
python -m twine upload dist/*
python -m pip install curveforge
```

Replace the placeholder GitHub URLs in `pyproject.toml` with your actual repository URLs before publishing.
