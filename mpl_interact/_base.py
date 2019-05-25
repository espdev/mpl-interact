# -*- coding: utf-8 -*-

import enum
import collections
from typing import NamedTuple, Optional

from mpl_events import MplEventDispatcher, MplObject_Type


class LocationCoords(NamedTuple):
    x: Optional[float]
    y: Optional[float]

    def __bool__(self):
        return self.x is not None and self.y is None

    @staticmethod
    def none_location():
        return LocationCoords(x=None, y=None)


class MouseButton(enum.Enum):
    """
    """
    ANY = 0
    LEFT = 1
    WHEEL = 2
    RIGHT = 3


class AxisType(enum.Enum):
    """
    """
    X = 'x'
    Y = 'y'
    ALL = 'xy'


class KeyModifier(enum.Flag):
    """
    """
    NO = 0
    CTRL = 2
    ALT = 4


class Key(NamedTuple):
    """
    """
    key: str
    modifier: KeyModifier


class InteractorBase(MplEventDispatcher):
    """The base class for all interactors
    """

    def __init__(self, mpl_obj: MplObject_Type):
        super().__init__(mpl_obj, connect=True)

    def update(self):
        """Updates and redraw canvas
        """
        self.figure.canvas.draw()

    @staticmethod
    def parse_key(key: str) -> Key:
        """Parses key string that comes from mpl KeyEvent
        """
        modifiers = collections.OrderedDict([
            ('ctrl+alt+', KeyModifier.CTRL | KeyModifier.ALT),
            ('ctrl+', KeyModifier.CTRL),
            ('alt+', KeyModifier.ALT),
            ('_none', KeyModifier.NO),
        ])

        modifier = '_none'

        for m in modifiers:
            if m in key:
                key = key.replace(m, '')
                modifier = m
                break

        return Key(key=key, modifier=modifiers[modifier])
