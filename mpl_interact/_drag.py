# -*- coding: utf-8 -*-

import abc
from typing import Optional

from mpl_events import MplObject_Type, mpl

from ._base import InteractorBase, MouseButton


class AxesDraggable(abc.ABC):
    """Axes draggable interface
    """

    def begin(self, event: mpl.LocationEvent):
        pass

    def end(self, event: mpl.LocationEvent):
        pass

    def drag(self, event: mpl.LocationEvent) -> bool:
        pass


class AxesMousePanDragger(AxesDraggable):
    """Axes dragging pan-based implementation
    """

    def __init__(self):
        self._axes: Optional[mpl.Axes] = None

    def begin(self, event: mpl.MouseEvent):
        if event.button != MouseButton.LEFT:
            return

        axes = event.inaxes

        if axes and axes.in_axes(event) and axes.can_pan():
            axes.start_pan(event.x, event.y, event.button)
            self._axes = axes

    def end(self, event: mpl.MouseEvent):
        if self._axes:
            self._axes.end_pan()
            self._axes = None

    def drag(self, event: mpl.MouseEvent) -> bool:
        if self._axes:
            self._axes.drag_pan(1, event.key, event.x, event.y)
            return True
        return False


class DragInteractor(InteractorBase):
    """Drags data on axes by mouse
    """

    def __init__(self, mpl_obj: MplObject_Type, dragger: Optional[AxesDraggable] = None):
        super().__init__(mpl_obj)

        if not dragger:
            dragger = AxesMousePanDragger()
        self._dragger = dragger

    def on_mouse_button_press(self, event: mpl.MouseEvent):
        self._dragger.begin(event)

    def on_mouse_button_release(self, event: mpl.MouseEvent):
        self._dragger.end(event)

    def on_mouse_move(self, event: mpl.MouseEvent):
        if self._dragger.drag(event):
            self.update()
