from __future__ import annotations

from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from matplotlib.axes import Axes

FloatArray = npt.NDArray[np.float64]
LineStyle = str | tuple[int, tuple[int, ...]]
AxisLimits = tuple[float | None, float | None]


@dataclass
class CurveLabelAnchor:
    x_anchor: float
    y_anchor: float
    x_text: float
    y_text: float
    label: str
    color: str


def apply_classic_bw_style(ax: Axes) -> None:
    """Apply a classic black-and-white technical style to an axis."""
    ax.set_facecolor("white")
    ax.grid(True, which="major", color="black", alpha=0.16, linestyle=":", linewidth=0.8)

    for spine in ax.spines.values():
        spine.set_color("black")
        spine.set_linewidth(1.0)

    ax.tick_params(colors="black", direction="in", length=5, width=0.9)


def annotate_curve_label(
    ax: Axes,
    x: npt.ArrayLike,
    y: npt.ArrayLike,
    label: str,
    color: str = "black",
    x_offset: float = 0.02,
    y_factor: float = 1.02,
) -> None:
    """Write a label near the peak of a curve."""
    x_arr = np.asarray(x, dtype=float)
    y_arr = np.asarray(y, dtype=float)

    peak_idx = int(np.argmax(y_arr))
    x_min, x_max = float(np.min(x_arr)), float(np.max(x_arr))
    x_span = x_max - x_min

    x_peak = float(x_arr[peak_idx])
    y_peak = float(y_arr[peak_idx])
    x_text = min(x_peak + x_offset * x_span, x_max - 0.02 * x_span)
    y_text = y_peak * y_factor

    ax.text(
        x_text,
        y_text,
        label,
        color=color,
        fontsize=10,
        ha="left",
        va="center",
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.7, pad=1.0),
    )


def plot_multiple_curves(
    x: npt.ArrayLike | list[npt.ArrayLike],
    curves: list[npt.ArrayLike],
    labels: list[str],
    title: str = "",
    xlabel: str = "x",
    ylabel: str = "y",
    annotate_on_curve: bool = True,
    xlim: tuple[float, float] | None = None,
    ylim: AxisLimits | None = None,
    figsize: tuple[float, float] = (11, 6),
) -> None:
    """Generic utility to plot multiple curves in the same figure."""
    y_arrays: list[FloatArray] = [np.asarray(y, dtype=float) for y in curves]

    if isinstance(x, list):
        x_arrays: list[FloatArray] = [np.asarray(x_i, dtype=float) for x_i in x]
        if len(x_arrays) != len(y_arrays):
            raise ValueError("When x is a list, it must have one x-array per curve.")
    else:
        x_arr: FloatArray = np.asarray(x, dtype=float)
        x_arrays = [x_arr for _ in y_arrays]

    line_styles: list[LineStyle] = ["-", "--", ":", "-.", (0, (7, 2, 1, 2))]
    line_widths: list[float] = [2.4, 2.0, 2.4, 2.0, 2.2]
    colors: list[str] = ["black", "dimgray", "black", "gray", "black"]
    markers: list[str] = ["o", "s", "^", "D", "v"]

    _, ax = plt.subplots(figsize=figsize, facecolor="white")
    apply_classic_bw_style(ax)

    anchors: list[CurveLabelAnchor] = []

    for i, (x_curve, y, label) in enumerate(zip(x_arrays, y_arrays, labels)):
        color = colors[i % len(colors)]
        ax.plot(
            x_curve,
            y,
            color=color,
            linestyle=line_styles[i % len(line_styles)],
            linewidth=line_widths[i % len(line_widths)],
            marker=markers[i % len(markers)],
            markevery=max(1, len(x_curve) // 12),
            markersize=4.5,
        )

        if annotate_on_curve:
            peak_idx = int(np.argmax(y))
            x_min, x_max = float(np.min(x_curve)), float(np.max(x_curve))
            x_span = x_max - x_min

            x_peak = float(x_curve[peak_idx])
            y_peak = float(y[peak_idx])

            anchors.append(
                CurveLabelAnchor(
                    x_anchor=x_peak,
                    y_anchor=y_peak,
                    x_text=min(x_peak + 0.02 * x_span, x_max - 0.02 * x_span),
                    y_text=y_peak * 1.06,
                    label=label,
                    color=color,
                )
            )

    if annotate_on_curve and anchors:
        y_anchor_values = [a.y_anchor for a in anchors]
        y_span = max(max(y_anchor_values) - min(y_anchor_values), 1.0)
        min_gap = 0.035 * y_span
        min_lift = 0.015 * y_span

        anchors.sort(key=lambda a: a.y_text)

        for anchor in anchors:
            anchor.y_text = max(anchor.y_text, anchor.y_anchor + min_lift)

        for i in range(1, len(anchors)):
            if anchors[i].y_text - anchors[i - 1].y_text < min_gap:
                anchors[i].y_text = anchors[i - 1].y_text + min_gap

        for anchor in anchors:
            ax.text(
                anchor.x_text,
                anchor.y_text,
                anchor.label,
                color=anchor.color,
                fontsize=10,
                ha="left",
                va="center",
                bbox=dict(facecolor="white", edgecolor="none", alpha=0.7, pad=1.0),
            )

    ax.set_title(title, color="black")
    ax.set_xlabel(xlabel, color="black")
    ax.set_ylabel(ylabel, color="black")

    if xlim is not None:
        ax.set_xlim(xlim)
    if ylim is not None:
        bottom, top = ylim
        ax.set_ylim(bottom=bottom, top=top)

    plt.tight_layout()
    plt.show()
