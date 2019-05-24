# -*- coding: utf-8 -*-

from mpl_events import mpl
from ._base import InteractorBase


class AxesLimitsRestoreInteractor(InteractorBase):

    def restore_axes_limits(self, axes: mpl.Axes = None):
        """Restores limits for given axes

        If axes is not set will be used current axes (in_axes)
        """
        if not axes:
            axes = self.in_axes
        if not axes:
            return

        axes.relim()
        axes.set_xlim(auto=True)
        axes.set_ylim(auto=True)
        axes.autoscale_view(scalex=True, scaley=True)

        self.update()

    def on_mouse_button_press(self, event: mpl.MouseEvent):
        if event.dblclick:
            self.restore_axes_limits()
