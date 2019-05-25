# -*- coding: utf-8 -*-

import math

from mpl_events import mpl, MplObject_Type

from ._base import InteractorBase


class ZoomInteractor(InteractorBase):
    """The interactor for zooming data

    The interactor scales data on axes via mouse wheel scrolling with anchor in
    current mouse cursor position. In this way you scale what you are looking at.

    """

    def __init__(self, mpl_obj: MplObject_Type):
        super().__init__(mpl_obj)
        self._wheel_zoom_step = 0.2
        self._wheel_zoom_inversion = False

    @property
    def wheel_zoom_step(self) -> float:
        return self._wheel_zoom_step

    @wheel_zoom_step.setter
    def wheel_zoom_step(self, value: float):
        if value > 0:
            self._wheel_zoom_step = value
        else:
            raise ValueError('Zoom step value must be greater than zero')

    @property
    def wheel_zoom_inversion(self) -> bool:
        return self._wheel_zoom_inversion

    @wheel_zoom_inversion.setter
    def wheel_zoom_inversion(self, value: bool):
        self._wheel_zoom_inversion = value

    def on_mouse_wheel_scroll(self, event: mpl.MouseEvent):
        axes: mpl.Axes = event.inaxes
        if axes and axes.in_axes(event) and axes.can_zoom():
            self._zoom(event)
            self.update()

    def _zoom(self, event: mpl.MouseEvent):
        axes = event.inaxes

        anchor_x = event.xdata
        anchor_y = event.ydata

        xmin, xmax = axes.get_xlim()
        ymin, ymax = axes.get_ylim()

        if self.wheel_zoom_inversion:
            step = -event.step
        else:
            step = event.step

        zoom_step = self._wheel_zoom_step * step

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
