# -*- coding: utf-8 -*-

from typing import Optional, Dict

from matplotlib import pyplot as plt
from mpl_events.mpl import Figure

from .base import InteractorBase
from .zoom import MouseWheelScrollZoomInteractor
from .drag import MouseDragInteractor
from .state import AxesLimitsResetInteractor


def interact(figure: Optional[Figure] = None, *,
             zoom: bool = True,
             drag: bool = True,
             reset: bool = True) -> Dict[str, InteractorBase]:
    """Enables interactors for the figure
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

    if zoom:
        interactors['zoom'] = MouseWheelScrollZoomInteractor(figure)
    if drag:
        interactors['drag'] = MouseDragInteractor(figure)
    if reset:
        interactors['reset'] = AxesLimitsResetInteractor(figure)

    return interactors
