# -*- coding: utf-8 -*-

import enum
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


class MouseButton(enum.IntEnum):
    LEFT = 1
    RIGHT = 2
    WHEEL = 3


class InteractorBase(MplEventDispatcher):
    """The base class for all interactors
    """

    def __init__(self, mpl_obj: MplObject_Type):
        super().__init__(mpl_obj, connect=True)

    def update(self):
        """Updates and redraw canvas
        """
        self.figure.canvas.draw()
