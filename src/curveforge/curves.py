from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np

_DEFAULT_SAMPLES = 1000
_VALID_FORMATS = {".png", ".svg", ".pdf"}


def _positive(name: str, value: float) -> float:
    value = float(value)
    if not np.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be a finite positive number")
    return value


def _integer(name: str, value: int, minimum: int = 2) -> int:
    if isinstance(value, bool) or int(value) != value or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return int(value)


class Curve(ABC):
    """Base class for all CurveForge curves."""

    name = "Curve"
    equation = ""

    @abstractmethod
    def _points(self, n: int) -> np.ndarray:
        raise NotImplementedError

    @abstractmethod
    def _parameter_range(self) -> tuple[float, float]:
        raise NotImplementedError

    def points(self, n: int = _DEFAULT_SAMPLES) -> np.ndarray:
        """Return sampled curve coordinates as an (N, 2) NumPy array."""
        n = _integer("n", n)
        points = np.asarray(self._points(n), dtype=float)
        if points.shape != (n, 2) or not np.isfinite(points).all():
            raise RuntimeError("Curve produced an invalid point array")
        return points

    def plot(
        self,
        ax: Optional[plt.Axes] = None,
        *,
        n: int = _DEFAULT_SAMPLES,
        show_equation: bool = True,
        grid: bool = True,
        title: Optional[str] = None,
        **plot_kwargs,
    ) -> plt.Axes:
        """Plot the curve and return the Matplotlib Axes."""
        if ax is None:
            _, ax = plt.subplots()
        points = self.points(n)
        options = {"linewidth": 2.0}
        options.update(plot_kwargs)
        ax.plot(points[:, 0], points[:, 1], **options)
        ax.set_aspect("equal", adjustable="box")
        ax.axhline(0, linewidth=0.7, alpha=0.35)
        ax.axvline(0, linewidth=0.7, alpha=0.35)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.grid(grid, alpha=0.25)
        ax.set_title(title or self.name)
        if show_equation:
            ax.text(
                0.02, 0.98, self.equation,
                transform=ax.transAxes,
                va="top",
                ha="left",
                fontsize=9,
                bbox={"boxstyle": "round,pad=0.3", "alpha": 0.10},
            )
        return ax

    def show(self, **kwargs) -> None:
        """Display the curve using Matplotlib."""
        self.plot(**kwargs)
        plt.show()

    def save(
        self,
        path: str | Path,
        *,
        n: int = _DEFAULT_SAMPLES,
        dpi: int = 300,
        show_equation: bool = True,
        grid: bool = True,
        title: Optional[str] = None,
        **plot_kwargs,
    ) -> Path:
        """Save the curve as PNG, SVG, or PDF and return the output Path."""
        output = Path(path)
        if output.suffix.lower() not in _VALID_FORMATS:
            raise ValueError("Output format must be .png, .svg, or .pdf")
        if isinstance(dpi, bool) or int(dpi) != dpi or dpi <= 0:
            raise ValueError("dpi must be a positive integer")
        output.parent.mkdir(parents=True, exist_ok=True)
        fig, ax = plt.subplots()
        self.plot(
            ax=ax, n=n, show_equation=show_equation,
            grid=grid, title=title, **plot_kwargs
        )
        fig.tight_layout()
        fig.savefig(
            output,
            dpi=int(dpi),
            format=output.suffix.lower()[1:],
            bbox_inches="tight",
        )
        plt.close(fig)
        return output


class Circle(Curve):
    name = "Circle"

    def __init__(self, r: float = 1):
        self.r = _positive("r", r)
        self.equation = f"x² + y² = {self.r:g}²"

    def _parameter_range(self):
        return 0.0, 2 * np.pi

    def _points(self, n):
        t = np.linspace(*self._parameter_range(), n)
        return np.column_stack((self.r * np.cos(t), self.r * np.sin(t)))


class Ellipse(Curve):
    name = "Ellipse"

    def __init__(self, a: float = 1, b: float = 1):
        self.a, self.b = _positive("a", a), _positive("b", b)
        self.equation = f"x²/{self.a:g}² + y²/{self.b:g}² = 1"

    def _parameter_range(self):
        return 0.0, 2 * np.pi

    def _points(self, n):
        t = np.linspace(*self._parameter_range(), n)
        return np.column_stack((self.a * np.cos(t), self.b * np.sin(t)))


class Parabola(Curve):
    name = "Parabola"

    def __init__(self, p: float = 1):
        self.p = _positive("p", p)
        self.equation = f"x = {self.p:g}t², y = 2({self.p:g})t"

    def _parameter_range(self):
        return -4.0, 4.0

    def _points(self, n):
        t = np.linspace(*self._parameter_range(), n)
        return np.column_stack((self.p * t**2, 2 * self.p * t))


class Hyperbola(Curve):
    name = "Hyperbola"

    def __init__(self, a: float = 1, b: float = 1):
        self.a, self.b = _positive("a", a), _positive("b", b)
        self.equation = f"x²/{self.a:g}² - y²/{self.b:g}² = 1"

    def _parameter_range(self):
        return -2.0, 2.0

    def _points(self, n):
        # Two branches, returned as one continuous N x 2 array.
        left_n = n // 2
        right_n = n - left_n
        t_left = np.linspace(*self._parameter_range(), max(2, left_n))
        t_right = np.linspace(*self._parameter_range(), max(2, right_n))
        xl = self.a * np.cosh(t_left)
        yl = self.b * np.sinh(t_left)
        xr = self.a * np.cosh(t_right)
        yr = self.b * np.sinh(t_right)
        left = np.column_stack((-xl[::-1], yl[::-1]))[:left_n]
        right = np.column_stack((xr, yr))[:right_n]
        return np.vstack((left, right))


class Astroid(Curve):
    name = "Astroid"

    def __init__(self, a: float = 1):
        self.a = _positive("a", a)
        self.equation = f"x = {self.a:g} cos³(t), y = {self.a:g} sin³(t)"

    def _parameter_range(self):
        return 0.0, 2 * np.pi

    def _points(self, n):
        t = np.linspace(*self._parameter_range(), n)
        return np.column_stack((self.a * np.cos(t)**3, self.a * np.sin(t)**3))


class Cardioid(Curve):
    name = "Cardioid"

    def __init__(self, a: float = 1):
        self.a = _positive("a", a)
        self.equation = f"r = {self.a:g}(1 + cos(t))"

    def _parameter_range(self):
        return 0.0, 2 * np.pi

    def _points(self, n):
        t = np.linspace(*self._parameter_range(), n)
        r = self.a * (1 + np.cos(t))
        return np.column_stack((r * np.cos(t), r * np.sin(t)))


class Cycloid(Curve):
    name = "Cycloid"

    def __init__(self, r: float = 1, arches: int = 1):
        self.r = _positive("r", r)
        self.arches = _integer("arches", arches, 1)
        self.equation = f"x = {self.r:g}(t - sin(t)), y = {self.r:g}(1 - cos(t))"

    def _parameter_range(self):
        return 0.0, 2 * np.pi * self.arches

    def _points(self, n):
        t = np.linspace(*self._parameter_range(), n)
        return np.column_stack((
            self.r * (t - np.sin(t)),
            self.r * (1 - np.cos(t)),
        ))


class Epicycloid(Curve):
    name = "Epicycloid"

    def __init__(self, R: float = 2, r: float = 1):
        self.R, self.r = _positive("R", R), _positive("r", r)
        self.equation = (
            f"x = (R+r)cos(t)-r cos((R+r)t/r), "
            f"y = (R+r)sin(t)-r sin((R+r)t/r)"
        )

    def _parameter_range(self):
        return 0.0, 2 * np.pi

    def _points(self, n):
        t = np.linspace(*self._parameter_range(), n)
        q = (self.R + self.r) / self.r
        return np.column_stack((
            (self.R + self.r) * np.cos(t) - self.r * np.cos(q * t),
            (self.R + self.r) * np.sin(t) - self.r * np.sin(q * t),
        ))


class Hypocycloid(Curve):
    name = "Hypocycloid"

    def __init__(self, R: float = 3, r: float = 1):
        self.R, self.r = _positive("R", R), _positive("r", r)
        if self.R <= self.r:
            raise ValueError("R must be greater than r for a hypocycloid")
        self.equation = (
            f"x = (R-r)cos(t)+r cos((R-r)t/r), "
            f"y = (R-r)sin(t)-r sin((R-r)t/r)"
        )

    def _parameter_range(self):
        return 0.0, 2 * np.pi

    def _points(self, n):
        t = np.linspace(*self._parameter_range(), n)
        q = (self.R - self.r) / self.r
        return np.column_stack((
            (self.R - self.r) * np.cos(t) + self.r * np.cos(q * t),
            (self.R - self.r) * np.sin(t) - self.r * np.sin(q * t),
        ))


class Rose(Curve):
    name = "Rose Curve"

    def __init__(self, a: float = 1, k: float = 3):
        self.a = _positive("a", a)
        self.k = float(k)
        if not np.isfinite(self.k) or self.k == 0:
            raise ValueError("k must be finite and non-zero")
        self.equation = f"r = {self.a:g} cos({self.k:g}t)"

    def _parameter_range(self):
        if self.k.is_integer() and int(abs(self.k)) % 2 == 0:
            return 0.0, np.pi
        return 0.0, 2 * np.pi

    def _points(self, n):
        t = np.linspace(*self._parameter_range(), n)
        r = self.a * np.cos(self.k * t)
        return np.column_stack((r * np.cos(t), r * np.sin(t)))


class Lemniscate(Curve):
    name = "Lemniscate"

    def __init__(self, a: float = 1):
        self.a = _positive("a", a)
        self.equation = f"x = {self.a:g}cos(t)/(1+sin²(t)), y = {self.a:g}sin(t)cos(t)/(1+sin²(t))"

    def _parameter_range(self):
        return 0.0, 2 * np.pi

    def _points(self, n):
        t = np.linspace(*self._parameter_range(), n)
        denominator = 1 + np.sin(t)**2
        return np.column_stack((
            self.a * np.cos(t) / denominator,
            self.a * np.sin(t) * np.cos(t) / denominator,
        ))


def circle(r=1): return Circle(r)
def ellipse(a=1, b=1): return Ellipse(a, b)
def parabola(p=1): return Parabola(p)
def hyperbola(a=1, b=1): return Hyperbola(a, b)
def astroid(a=1): return Astroid(a)
def cardioid(a=1): return Cardioid(a)
def cycloid(r=1, arches=1): return Cycloid(r, arches)
def epicycloid(R=2, r=1): return Epicycloid(R, r)
def hypocycloid(R=3, r=1): return Hypocycloid(R, r)
def rose(a=1, k=3): return Rose(a, k)
def lemniscate(a=1): return Lemniscate(a)
