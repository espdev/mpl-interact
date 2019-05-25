# -*- coding: utf-8 -*-

import abc
import math
from typing import Optional

from mpl_events import mpl, MplObject_Type

from ._base import InteractorBase


class AxesZoomable(abc.ABC):
    """Axes zoomable interface
    """

    def zoom(self, event: mpl.MouseEvent, step: float, inversion: bool) -> bool:
        """This method should implement zooming
        """
        pass


class AxesMouseAnchorZoomer(AxesZoomable):
    """Zooming axes according to mouse cursor position

    Performs zoom with anchor in current mouse cursor position.
    In this way you scale what you are looking at.
    """

    def zoom(self, event: mpl.MouseEvent, step: float, inversion: bool) -> bool:
        axes: mpl.Axes = event.inaxes

        if not axes or not axes.in_axes(event) or not axes.can_zoom():
            return False

        anchor_x = event.xdata
        anchor_y = event.ydata

        xmin, xmax = axes.get_xlim()
        ymin, ymax = axes.get_ylim()

        wheel_step = -event.step if inversion else event.step
        zoom_step = wheel_step * step

        is_xlog = axes.get_xscale() == 'log'
        is_ylog = axes.get_yscale() == 'log'

        if event.key == 'x':
            xmin, xmax = self._recalc_axis_limits(xmin, xmax, anchor_x, zoom_step, is_xlog)
        elif event.key == 'y':
            ymin, ymax = self._recalc_axis_limits(ymin, ymax, anchor_y, zoom_step, is_ylog)
        else:
            xmin, xmax = self._recalc_axis_limits(xmin, xmax, anchor_x, zoom_step, is_xlog)
            ymin, ymax = self._recalc_axis_limits(ymin, ymax, anchor_y, zoom_step, is_ylog)

        axes.set_xlim(xmin, xmax)
        axes.set_ylim(ymin, ymax)

        return True

    @staticmethod
    def _recalc_axis_limits(lim_min, lim_max, anchor, zoom_step, is_log):
        if is_log:
            lim_min = math.log10(lim_min)
            lim_max = math.log10(lim_max)
            anchor = math.log10(anchor)

        anchor = lim_min if anchor < lim_min else anchor
        anchor = lim_max if anchor > lim_max else anchor

        ra = abs(lim_min - anchor)
        rb = abs(lim_max - anchor)

        lim_min = lim_min - ra * zoom_step
        lim_max = lim_max + rb * zoom_step

        if lim_min > lim_max:
            lim_min, lim_max = lim_max, lim_min

        if is_log:
            lim_min = pow(10.0, lim_min)
            lim_max = pow(10.0, lim_max)

        return lim_min, lim_max


class ZoomInteractor(InteractorBase):
    """The interactor for zooming data

    The interactor scales data on axes via mouse wheel scrolling with anchor in
    current mouse cursor position. In this way you scale what you are looking at.

    """

    def __init__(self, mpl_obj: MplObject_Type, zoomer: Optional[AxesZoomable] = None):
        super().__init__(mpl_obj)

        self._step = 0.2
        self._inversion = False

        if not zoomer:
            zoomer = AxesMouseAnchorZoomer()
        self._zoomer = zoomer

    @property
    def step(self) -> float:
        return self._step

    @step.setter
    def step(self, value: float):
        if value > 0:
            self._step = value
        else:
            raise ValueError('Zoom step value must be greater than zero')

    @property
    def inversion(self) -> bool:
        return self._inversion

    @inversion.setter
    def inversion(self, value: bool):
        self._inversion = value

    def on_mouse_wheel_scroll(self, event: mpl.MouseEvent):
        if self._zoomer.zoom(event, self.step, self.inversion):
            self.update()
