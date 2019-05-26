# -*- coding: utf-8 -*-

import enum
import collections
from typing import NamedTuple, Optional, Union, Collection

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
    MIDDLE = 2
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
    key: Optional[str]
    modifier: KeyModifier

    def __bool__(self) -> bool:
        return bool(self.key)

    def has_modifier(self) -> bool:
        return self.modifier != KeyModifier.NO


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
        if not key:
            return Key(key=None, modifier=KeyModifier.NO)

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

    def check_key(self, key: Union[str, Key], key_set: Collection[str],
                  modifier: Optional[KeyModifier] = None):
        """Checks the key for given set of keys and optionally modifier
        """
        if not isinstance(key, Key):
            key = self.parse_key(key)
        if not key:
            return False

        k_ok = key.key in key_set
        m_ok = True if modifier is None else key.modifier == modifier

        return k_ok and m_ok
