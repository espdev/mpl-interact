# -*- coding: utf-8 -*-

from typing import NamedTuple, Optional

from mpl_events import MplEventDispatcher, MplObject_Type
from mpl_events import mpl


class LocationCoords(NamedTuple):
    x: Optional[float]
    y: Optional[float]

    def __bool__(self):
        return self.x is not None and self.y is None

    @staticmethod
    def none_location():
        return LocationCoords(x=None, y=None)


class InteractorBase(MplEventDispatcher):
    """The base class for all interactors
    """

    def __init__(self, mpl_obj: MplObject_Type):
        super().__init__(mpl_obj)

        self._in_axes: Optional[mpl.Axes] = None
        self._data_coords = LocationCoords.none_location()
        self._canvas_coords = LocationCoords.none_location()

    @property
    def in_axes(self) -> mpl.Axes:
        """Returns an axes object under mouse cursor
        """
        return self._in_axes

    @property
    def data_coords(self) -> LocationCoords:
        return self._data_coords

    @property
    def canvas_coords(self) -> LocationCoords:
        return self._canvas_coords

    def update(self):
        """Updates and redraw canvas
        """
        self.figure.canvas.draw()

    def on_axes_enter(self, event: mpl.LocationEvent):
        self._in_axes = event.inaxes

    def on_axes_leave(self, event: mpl.LocationEvent):
        self._in_axes = None
        self._data_coords = LocationCoords.none_location()

    def on_figure_leave(self, event: mpl.LocationEvent):
        self._canvas_coords = LocationCoords.none_location()

    def on_mouse_move(self, event: mpl.MouseEvent):
        if self._in_axes:
            self._data_coords = LocationCoords(x=event.xdata, y=event.ydata)
        self._canvas_coords = LocationCoords(x=event.x, y=event.y)
