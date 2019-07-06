# -*- coding: utf-8 -*-

import enum
from typing import Optional, Dict

from matplotlib import pyplot as plt
from mpl_events.mpl import Figure

from .base import InteractorBase
from .zoom import MouseWheelScrollZoomInteractor
from .drag import MouseDragInteractor
from .state import AxesLimitsResetInteractor


class Actions(enum.Flag):
    """Interaction action flags
    """

    ZOOM = enum.auto()
    DRAG = enum.auto()
    RESET = enum.auto()

    ALL = ZOOM | DRAG | RESET


def interact(figure: Optional[Figure] = None,
             actions: Actions = Actions.ALL) -> Dict[Actions, InteractorBase]:
    """Enables interactors for the figure

    Supports interaction actions:

    * zoom
    * drag
    * reset axes
    """
    if not figure:
        figure = plt.gcf()

    if not hasattr(interact, 'interactors'):
        interact.interactors = {}

    if figure in interact.interactors:
        for interactor in interact.interactors[figure].values():
            interactor.mpl_disconnect()
        del interact.interactors[figure]

    interactors = interact.interactors.setdefault(figure, {})

    if Actions.ZOOM in actions:
        interactors[Actions.ZOOM] = MouseWheelScrollZoomInteractor(figure)
    if Actions.DRAG in actions:
        interactors[Actions.DRAG] = MouseDragInteractor(figure)
    if Actions.RESET in actions:
        interactors[Actions.RESET] = AxesLimitsResetInteractor(figure)

    return interactors
