# -*- coding: utf-8 -*-

"""
Module provides interacotors for zooming data on an axes

"""

import abc
from typing import Optional

from matplotlib.transforms import IdentityTransform

from mpl_events import mpl, MplObject_Type

from .base import InteractorBase, AxisType, KeyModifier


class AxesZoomable(abc.ABC):
    """Axes zoomable interface
    """

    @abc.abstractmethod
    def begin(self, event: mpl.LocationEvent):
        pass

    @abc.abstractmethod
    def end(self, event: mpl.LocationEvent):
        pass

    @abc.abstractmethod
    def zoom(self, event: mpl.LocationEvent, step: float, axis: AxisType = AxisType.ALL) -> bool:
        """This method should implement zoom functionality
        """
        pass


class MouseAnchorAxesZoomer(AxesZoomable):
    """Zooming axes according to mouse cursor position

    Performs zoom with anchor in current mouse cursor position.
    In this way you scale what you are looking at.
    """

    def begin(self, event: mpl.LocationEvent):
        pass

    def end(self, event: mpl.LocationEvent):
        pass

    def zoom(self, event: mpl.LocationEvent, step: float, axis: AxisType = AxisType.ALL) -> bool:
        axes: mpl.Axes = event.inaxes

        if not axes or not axes.in_axes(event) or not axes.can_zoom():
            return False

        xanchor = event.xdata
        yanchor = event.ydata

        xmin, xmax = axes.get_xlim()
        ymin, ymax = axes.get_ylim()

        xtransform = axes.xaxis.get_transform()
        ytransform = axes.yaxis.get_transform()

        if axis == AxisType.X:
            xmin, xmax = self._recalc_axis_limits(ymin, ymax, xanchor, step, xtransform)
        elif axis == AxisType.Y:
            ymin, ymax = self._recalc_axis_limits(ymin, ymax, yanchor, step, ytransform)
        elif axis == AxisType.ALL:
            xmin, xmax = self._recalc_axis_limits(xmin, xmax, xanchor, step, xtransform)
            ymin, ymax = self._recalc_axis_limits(ymin, ymax, yanchor, step, ytransform)

        axes.set_xlim(xmin, xmax)
        axes.set_ylim(ymin, ymax)

        return True

    @staticmethod
    def _recalc_axis_limits(lim_min, lim_max, anchor, zoom_step, transform):
        if not isinstance(transform, IdentityTransform):
            lim_min, lim_max, anchor = transform.transform([lim_min, lim_max, anchor]).tolist()

        anchor = lim_min if anchor < lim_min else anchor
        anchor = lim_max if anchor > lim_max else anchor

        ra = abs(lim_min - anchor)
        rb = abs(lim_max - anchor)

        lim_min = lim_min + ra * zoom_step
        lim_max = lim_max - rb * zoom_step

        if lim_min > lim_max:
            lim_min, lim_max = lim_max, lim_min

        if not isinstance(transform, IdentityTransform):
            lim_min, lim_max = transform.inverted().transform([lim_min, lim_max]).tolist()

        return lim_min, lim_max


class ZoomInteractorBase(InteractorBase):
    """The base interactor for zooming data on an axes
    """

    def __init__(self, mpl_obj: MplObject_Type, zoomer: Optional[AxesZoomable] = None):
        super().__init__(mpl_obj)

        self._step = 0.2

        if not zoomer:
            zoomer = MouseAnchorAxesZoomer()
        self._zoomer = zoomer

    @property
    def zoomer(self) -> AxesZoomable:
        return self._zoomer

    @property
    def step(self) -> float:
        return self._step

    @step.setter
    def step(self, value: float):
        if value > 0:
            self._step = value
        else:
            raise ValueError('Zoom step value must be greater than zero')


class MouseWheelScrollZoomInteractor(ZoomInteractorBase):
    """The mouse wheel scroll interactor for zooming data on axes
    """

    x_axis_keys = {'x', 'X'}
    y_axis_keys = {'y', 'Y'}

    def __init__(self, mpl_obj: MplObject_Type, zoomer: Optional[AxesZoomable] = None):
        super().__init__(mpl_obj, zoomer)

        self._inversion = True

    @property
    def inversion(self) -> bool:
        return self._inversion

    @inversion.setter
    def inversion(self, value: bool):
        self._inversion = value

    def on_mouse_wheel_scroll(self, event: mpl.MouseEvent):
        step = self.step * event.step
        step = -step if self.inversion else step

        key = self.parse_key(event.key)

        if self.check_key(key, self.x_axis_keys, KeyModifier.NO):
            axis = AxisType.X
        elif self.check_key(key, self.y_axis_keys, KeyModifier.NO):
            axis = AxisType.Y
        else:
            axis = AxisType.ALL

        if self.zoomer.zoom(event, step, axis):
            self.update()


class KeyZoomInteractor(ZoomInteractorBase):
    """Keyboard based zoom interactor
    """

    disable_default_handlers = True

    zoom_plus_keys = {'p', '=', '+'}
    zoom_minus_keys = {'m', '-'}
    x_modifier = KeyModifier.CTRL
    y_modifier = KeyModifier.ALT

    def on_key_press(self, event: mpl.KeyEvent):
        key = self.parse_key(event.key)

        if not key or key.modifier == KeyModifier.CTRL | KeyModifier.ALT:
            return

        if self.check_key(key, self.zoom_plus_keys):
            step = self.step
        elif self.check_key(key, self.zoom_minus_keys):
            step = -self.step
        else:
            return

        axis = AxisType.ALL

        if key.modifier == self.x_modifier:
            axis = AxisType.X
        elif key.modifier == self.y_modifier:
            axis = AxisType.Y

        if self.zoomer.zoom(event, step, axis):
            self.update()
